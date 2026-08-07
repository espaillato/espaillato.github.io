---
layout: post
title: "Syncing Samsung Health Data to Google Drive via Android Health Connect"
date: 2026-08-06
---

Two people in my household wear Samsung devices and use Samsung Health. Samsung Health's own dashboard is fine for a quick glance, but it doesn't give you a portable, queryable, long-term record — and it's a dead end the moment you want to look at trends across months or years, or across more than one person's data at once.

This describes the Android app I built to fix that: it reads everything Health Connect exposes, aggregates it sensibly, and appends it to a per-person CSV file in Google Drive. No backend server, no third-party service, nothing but the phone and a Drive folder.

- [Why this exists: feeding a living reference, not just a backup](#why-this-exists)
- [Why Health Connect, not Samsung Health directly](#why-health-connect)
- [Architecture](#architecture)
- [Data model: daily aggregation and the sleep-day problem](#data-model)
- [Google Drive as the sync target (service account gotchas)](#drive-service-account)
- [The WorkManager scheduling bug that cost a day](#workmanager-bug)
- [Dedup, cursors, and retroactive permission grants](#dedup-and-cursors)
- [Android 14's second permission-rationale requirement](#android-14-manifest)
- [Running it on two sideloaded phones](#two-phones)
- [End state](#end-state)

---

## 0. Why this exists: feeding a living reference, not just a backup {#why-this-exists}

It would be fair to ask why any of this is worth building instead of just glancing at the Samsung Health app occasionally. The honest answer is that this isn't really a "backup" project — it's a *source data* project.

I keep a structured [personal document archive]({% post_url 2026-05-11-google-drive-file-archive-canonical-reorg %}), organized around a small set of life categories (Health among them), and within each category a `_Core` folder reserved for *living reference* documents — the kind meant to always reflect current understanding, not a single point-in-time snapshot. Historically, keeping something like a health overview genuinely current meant remembering to sit down and rewrite it by hand every few months, which is exactly the kind of maintenance that quietly stops happening.

The direction I'm working toward instead: have an AI model read the raw, structured data sitting in the archive and use it to both *analyze* (spot trends, flag things worth a second look) and *keep the `_Core` reference documents themselves up to date* — regenerated from real data instead of remembered impressions. That only works if there's real structured data to read in the first place. A phone's on-device health dashboard doesn't produce that; a folder of screenshots doesn't either. A clean, deduplicated, sensibly-aggregated CSV — landing in exactly the right place in that archive — does. That's what this app is actually for: not a health-tracking hobby project, but the data-collection layer underneath a larger system.

---

## 1. Why Health Connect, not Samsung Health directly {#why-health-connect}

Samsung Health has its own proprietary sensor pipeline for a handful of metrics, and reading those directly means special-casing Samsung's SDK. I didn't want that. The rule I settled on:

- If Health Connect exposes a metric through its normal permission model, read it.
- If it's noisy at native resolution (heart rate, speed, cadence...), aggregate it — don't drop it.
- If reading it requires bespoke, vendor-specific code outside Health Connect's own API, leave it out.

That one rule kept the scope honest. It also means the app works for *any* Health Connect source, not just Samsung Health — body-composition data (weight, body fat, etc.) written by a different app or a different manufacturer's scale comes through the exact same path.

---

## 2. Architecture {#architecture}

- **Android app** (Kotlin, single Activity + an app widget) — reads Health Connect via `androidx.health.connect:connect-client`, uploads via the Drive v3 API.
- **WorkManager** — a once-a-day background sync plus an on-demand "Sync Now" that runs whenever the app is opened.
- **Google Drive, service-account auth** — no OAuth login flow on-device, no user-facing Google sign-in. A service account key (JSON) is dropped into the app's private storage once, and the app authenticates headlessly from then on.
- **One CSV per person** in a shared Drive folder — `user1_health_sync.csv`, `user2_health_sync.csv`, dead simple to open in a spreadsheet or load with `pandas`.

The CSV schema is deliberately flat:

```
timestamp_utc,owner,metric,value,unit,source_record_id
```

`source_record_id` is the dedup key — more on that below.

---

## 3. Data model: daily aggregation and the sleep-day problem {#data-model}

Early on the app synced Health Connect's raw records verbatim. That's fine for a day or two, then steps and heart-rate data balloon into thousands of rows that no longer serve the actual goal: seeing trends over weeks, months, years.

The fix is a metric-by-metric aggregation policy:

- **Additive metrics** (steps, calories, distance, floors climbed...) → summed per day.
- **Dense sampled metrics** (heart rate, speed, cadence...) → daily min/avg/max, three rows a day instead of hundreds.
- **Point-in-time metrics** (weight, height, body fat, blood pressure...) → left as-is, unaggregated. There's exactly one meaningful value per reading; collapsing it into a "daily average" would just be lossy for no reason.

The one wrinkle worth calling out: **a calendar day is the wrong bucket for sleep.** Steps taken between midnight and midnight map cleanly onto "today." A sleep session that starts at 11pm and ends at 7am does not — bucketing it by calendar day either splits one sleep session across two days or arbitrarily assigns it to whichever day it started on, both of which corrupt night-over-night trend data.

The fix: sleep-related metrics use a **noon-to-noon "sleep day"** instead of a calendar day (`instant.minusHours(12)`, then take the date). Everything else stays on calendar-day boundaries. That means the app has two different, deliberately different, definitions of "day" running side by side — worth documenting loudly in the code, because it's exactly the kind of thing a future edit could quietly break.

That in turn creates a **completeness problem**: a calendar day is "done" at midnight, but a sleep day isn't "done" until noon the *next* day. A single query boundary can't correctly serve both. The app resolves this by separating two concerns that used to be conflated into one timestamp:

- **How far back does this query look?** — always as fresh as possible, up to "now."
- **Which aggregated buckets are safe to emit?** — a bucket only gets included once its boundary has actually passed (`isCompleteCalendarDay` / `isCompleteSleepDay`), regardless of how fresh the query itself was.

The sync cursor only ever advances to the latest point that's safe for *every* metric — never past a boundary that could still receive more data.

---

## 4. Google Drive as the sync target {#drive-service-account}

A service account is the right tool here: no user-facing login, no refresh-token dance on-device, just a JSON key file and a folder shared with the service account's email as Editor.

Two gotchas that cost real time:

**Service accounts have no storage quota of their own.** `files.create()` against a folder the service account only has *Editor* access to (not ownership) fails with `storageQuotaExceeded` — service accounts can create files only up to their own (zero) quota, full stop. The workaround is boring but reliable: pre-create the empty CSV files yourself, share the folder, and let the app only ever `files.update()` an existing file it never has to "create."

**Dedup has to be data-driven, not timestamp-driven.** Health Connect write sources can backfill *already-passed* timestamps — a source might not get write permission until well after it started collecting data, then dump hours of retroactive history the moment permission is granted. If the sync cursor had already advanced past that window, that backfilled data becomes permanently unreachable, since the cursor never looks backward. Two things fix this together: the cursor only advances when a sync actually finds *something* (an empty result never moves it forward), and every upload is deduped against a synthetic, deterministic `source_record_id` parsed out of the CSV's last column before anything gets appended. That combination means a manual "resync everything from scratch" is always safe to run — nothing above the file's high-water mark can duplicate.

---

## 5. The WorkManager scheduling bug that cost a day {#workmanager-bug}

This is the one worth writing down for anyone else scheduling periodic background work on Android.

The background sync used `PeriodicWorkRequestBuilder(1, DAYS, 1, HOURS)` — a one-day interval with a one-hour flex window, `setInitialDelay()` computed to land on a specific hour, `ExistingPeriodicWorkPolicy.UPDATE` on every app launch so re-opening the app would re-anchor the schedule if the target time ever changed.

On a real device, `dumpsys jobscheduler` showed the job's actual `Minimum latency` landing roughly **23 hours later** than the computed initial delay implied it should. Not random drift — the same offset, reproducible, on two separate phones.

The cause: **`setInitialDelay` on a periodic work request only shifts when the period *starts* — it does not let the first execution skip ahead within that period.** The first run still waits out `(interval − flex)` beyond the initial delay, exactly like every subsequent run does. With a 1-hour flex on a 24-hour interval, that's `initialDelay + 23h` for the very first execution — silently adding almost a full extra day before anything runs the first time.

Two separate fixes were needed:

1. **`ExistingPeriodicWorkPolicy.UPDATE` doesn't reliably re-anchor** an already-scheduled periodic work to a freshly computed initial delay — confirmed by changing the target hour and watching `UPDATE` leave the old cadence in place. Switched to `CANCEL_AND_REENQUEUE`, which fully removes and reinserts the WorkSpec instead of trying to patch it in place.
2. **Drop the flex window entirely.** Omitting it makes the effective flex equal to the full interval, so the first run fires right at the initial delay as intended — the OS still has the whole day to batch/optimize the job exactly as it would with any flex value.

Verified with `adb shell dumpsys jobscheduler`, comparing the job's reported `Minimum latency` against `adb shell date` on the actual device — not just reasoning about the API from documentation. The gap between "should work per the docs" and "what the real scheduler does" is exactly why that verification step existed at all.

---

## 6. Dedup, cursors, and retroactive permission grants {#dedup-and-cursors}

One more real bug, caught by actually using the app rather than reading the code: after granting Health Connect a *new* permission (a metric that wasn't being read before), the app's existing sync cursor was already ahead of that metric's entire history. From the cursor's point of view, that metric simply started existing the moment the permission was granted — everything Health Connect still retained from before that was silently unreachable.

The fix is a manual "Resync Full History" action: reset the cursor to null, re-run the sync. It's safe to hit at any time, for any reason, precisely because of the `source_record_id` dedup backstop described above — already-uploaded days get filtered out on the way to Drive, not duplicated.

---

## 7. Android 14's second permission-rationale requirement {#android-14-manifest}

Health Connect's permission screen needs an activity the OS can deep-link into for "why is this app asking for this" — but the manifest entry for that changed on Android 14, and the two requirements coexist rather than one replacing the other:

- Pre-Android-14: an activity-alias responding to `ACTION_SHOW_PERMISSIONS_RATIONALE`.
- Android 14+: a **second**, separate activity-alias, with the `VIEW_PERMISSION_USAGE` action, the `HEALTH_PERMISSIONS` category, and the `START_VIEW_PERMISSION_USAGE` permission.

Missing the second one doesn't throw an error — it just makes the permission screen flash open and immediately close, which is a genuinely confusing failure mode to debug from logs alone (`logcat` showed both activities created and destroyed within the same millisecond). Both aliases need to be declared side by side; there's no version-gating trick that lets you skip one.

---

## 8. Running it on two sideloaded phones {#two-phones}

No Play Store listing — this is a two-person household tool, sideloaded via a signed release build on each phone. A couple of things that mattered in practice:

- **Debug builds let you cheat; release builds don't.** Getting the Drive service-account key onto a debug build's private storage is a one-line `adb shell run-as ... cp`. Release builds aren't debuggable, so that's blocked outright — the real answer is an in-app "Import Key" flow using `ActivityResultContracts.OpenDocument()`, letting the user pick the downloaded key file from wherever it landed (Downloads, an email attachment) and having the app copy its bytes into its own storage via the returned `content://` URI.
- **The UI needed a real "did anything just happen" signal.** The first version only showed "data through: `<cutoff>`" — which barely moves day to day and gives zero feedback about whether a sync attempt just ran and failed versus never running at all. Splitting that into two separate fields — *last sync attempt* (wall-clock time, updates on success or failure) and *data through* (the actual cutoff) — made failures visible instead of silent.
- **Keep the primary action's position fixed.** The "Sync Now" button used to be positioned directly below the status text, so a longer error message would shove the button further down the screen between taps. Small thing, very annoying in practice — the fix is just reordering the layout so the button has a stable anchor and the status text flows *beneath* it.

---

## End state {#end-state}

- One Android app, two installs, one shared Drive folder.
- Roughly 30 Health Connect metrics read, aggregated where it matters, left alone where aggregation would lose information.
- Calendar-day and sleep-day boundaries handled as the genuinely different things they are.
- A background sync that actually lands when it's supposed to, verified against the real OS scheduler rather than assumed from the API surface.
- Zero servers, zero recurring cost, zero third-party services beyond Drive itself.
- Clean, structured data landing exactly where [the archive's Health category]({% post_url 2026-05-11-google-drive-file-archive-canonical-reorg %}) expects it — not the end goal by itself, but the raw material the living-reference layer actually needs to be worth building.

The most useful lesson wasn't any single line of code — it was how many of these bugs (the scheduling gap, the flash-closing permission screen, the unreachable backfilled history) were invisible from reading the code or the docs, and only showed up from actually running the thing on real devices and checking real system state (`dumpsys`, `logcat`, the actual Drive file contents) after the fact. Health/scheduling APIs in particular seem to have a wide gap between "what the documentation implies" and "what the OS actually does," and that gap doesn't announce itself.
