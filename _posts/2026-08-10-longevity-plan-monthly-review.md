---
layout: post
title: "Turning a Health Chart Into an Actual Plan, and Keeping It Current"
date: 2026-08-10
---

Two earlier posts here cover getting health data collected ([synced automatically from a phone into a structured file]({% post_url 2026-08-06-health-connect-google-drive-sync-android %})) and getting it organized ([filed into a clean, current-state layer on top of a personal archive]({% post_url 2026-05-11-google-drive-file-archive-canonical-reorg %})). Neither of those, on its own, turns into anything you'd actually do differently. A well-organized chart is still just a chart. This is the piece that turns it into a plan, and keeps that plan from going stale the way every other health resolution eventually does.

- [What this actually is (and isn't)](#what-it-is)
- [The rule that makes it useful: strictly additive](#strictly-additive)
- [Structure: reasoning attached to every line, not just a task list](#structure)
- [The monthly review loop](#monthly-review)
- [A silent plan is a stale plan](#silent-is-stale)
- [End state](#end-state)

---

## 0. What this actually is (and isn't) {#what-it-is}

Call it a longevity plan, a healthspan plan, whatever — the actual content is a short, chart-derived list of labs, imaging, functional tests, and behavior changes worth raising at a doctor's visit, each one tied to a specific reason pulled from an actual chart rather than a general "things people over 50 should think about" list.

Two framing choices matter more than anything in the content itself:

**It's explicitly not a diagnosis or a treatment plan.** It's preparation material — the goal is a better-informed conversation at an appointment, not a replacement for one. That distinction has to survive being written down, or the document quietly turns into something it shouldn't be.

**It exists to coordinate across specialists who don't see each other's records.** A cardiologist, an endocrinologist, and a sleep clinic each get a narrow slice of the picture. Nobody except the person living in that body — and, now, this document — sees all three slices at once. That's the actual gap this fills.

---

## 1. The rule that makes it useful: strictly additive {#strictly-additive}

The single most important constraint on this document: it never duplicates what a standard checkup already covers. If a lab is already on the checklist for an upcoming visit, it doesn't also appear here — it stays exactly where it already lives, once.

This matters because the alternative failure mode is real and common: a "personalized" health document that's mostly generic filler ("eat more vegetables," "get enough sleep") dressed up with a name at the top. That kind of document earns zero trust after the second read, because none of it required knowing anything about the actual person. The value here is entirely in the opposite direction — every line exists *because* of something specific already in the chart, and there's a whole section at the bottom of the plan explicitly listing what the standard checklist already handles well, specifically so nothing gets duplicated by accident later.

Kept genuinely narrow, too — evidence-weighted, not aspirational. Longevity medicine has a wide range of tests and interventions with wildly different evidence quality behind them; this document leans hard toward the well-established, low-downside end of that range and skips the speculative end entirely.

---

## 2. Structure: reasoning attached to every line, not just a task list {#structure}

The plan has three categories — additive labs, imaging/functional tests, behavioral priorities — and every single item in all three carries its actual reasoning inline, not just a name. Not "ApoB," but *why* ApoB, given what the last lipid panel actually showed and what ApoB catches that a standard panel doesn't. Not "resistance training," but which specific gap in an otherwise-strong fitness picture it's addressing.

That's deliberate. A bare list of test names is something you could get from a search engine. A list where every item explains why it matters *for this specific chart* is something that only exists because someone actually read the chart.

The tracking half is a literal checklist — checkbox, status, and once something gets done at a real visit, it moves to a completed line with a date and a pointer to where the actual result landed. The plan is meant to visibly show progress over time, not sit as a static wish list that either gets fully ignored or fully forgotten about.

---

## 3. The monthly review loop {#monthly-review}

This is a separate, recurring task from the one that built the plan in the first place — a scheduled monthly pass, per person, that:

1. Reads the plan's current checklist.
2. Reads the chart notes the plan is derived from (the running summary, the lab-trend table, the wearable-trend table).
3. Checks whether anything on the checklist has since been actioned, and whether any new finding changes what should be prioritized.
4. Updates the plan in place — never a rewrite from scratch, just edits to what changed.
5. Logs a dated entry describing exactly what changed this pass.

The cost discipline here is the part worth calling out. A monthly review that re-extracts everything from source documents each time would be expensive and would duplicate work two other parts of this system already do (filing new documents, and a separate weekly audit that catches anything not yet summarized). So this review deliberately doesn't do that — it only reads the already-processed notes, and if it spots a source document newer than the plan's last update that hasn't been folded into those notes yet, it flags that as a gap for the other layer to pick up rather than doing the extraction itself. Cheap stays cheap by staying narrow about whose job is whose.

---

## 4. A silent plan is a stale plan {#silent-is-stale}

Even a review that finds nothing to change still writes a log entry — something like "reviewed, no changes, N items still open, nothing new shifts priorities." That's not busywork. A plan with no visible review history is indistinguishable from a plan nobody's actually checking anymore, and the entire point of a monthly cadence evaporates the moment "no news" and "no one looked" become the same thing on the page.

This is the same instinct as a rule from [the archive-reorg post]({% post_url 2026-05-11-google-drive-file-archive-canonical-reorg %}#living-notes-honest): a stale note is worse than no note, because it looks authoritative right up until it's wrong. Here it shows up as a habit instead of a check — silence gets logged, on purpose, so it reads as "confirmed current" instead of "abandoned."

---

## End state {#end-state}

- A short, chart-derived plan per person — labs, imaging, functional tests, behavior changes — every item carrying its own reasoning, not a generic checklist with a name on it.
- Strictly additive to standard care, with an explicit record of what's already covered elsewhere, so scope can't quietly creep.
- A visible progress tracker: checkboxes move to dated, linked completions instead of sitting untouched.
- A monthly review that stays cheap by only reading already-processed notes, handing off anything that needs real extraction to the layer built for that.
- A logged entry every single review, changes or not — the plan's own proof that it's still being watched.

The whole series so far is really one idea applied at increasing altitude: collect the data, organize the data, then actually use the data for something, and don't let any of those three stop happening quietly. This is the "actually use it" layer, and the monthly loop is what keeps it from becoming one more good intention that fades by March.
