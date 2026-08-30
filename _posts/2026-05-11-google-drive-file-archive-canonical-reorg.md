---
layout: post
title: "What Actually Fixed a Decade of Google Drive Sprawl"
date: 2026-05-11
---

A shared household Google Drive accumulates documents for years before anyone treats it as a system rather than a dumping ground. Mine had two dozen top-level folders, several of them near-duplicates: a typo'd second category next to the real one, two folders that meant almost the same thing under different names, plus a scattering of one-off folders sitting at the same level as major life categories. No convention for whose document something was, whether it was shared, or whether it was a stable reference or a one-time record.

This is the story of fixing that: how the first approach failed at the part that mattered most, and what it produced along the way that made the second approach work.

- [The starting mess](#starting-mess)
- [Attempt one: a scripted, rules-based pipeline](#attempt-one)
- [Where the script hit its ceiling](#the-ceiling)
- [What actually worked: two skills, one rulebook](#what-worked)
- [How the filer actually reads a file](#reading-a-file)
- [The automation boundary: when to just do it vs. when to ask](#automation-boundary)
- [Keeping the living notes honest, not just the archive](#living-notes-honest)
- [Inside the philosophy document](#the-philosophy-doc)
- [What carried over from the first attempt](#the-lesson)
- [The living-reference layer](#living-reference)
- [End state](#end-state)

---

## 0. The starting mess {#starting-mess}

A read-only audit script walked the archive and produced a blunt table: folder name, subfolder count, file count. The top of that table told the story — near-duplicate category names differing only by a typo or a synonym, several folders with a handful of files each that existed only because something needed somewhere to go at the time, and nothing anywhere indicating whose document it was or whether it was shared.

None of that is unusual. It's what any shared drive looks like after years of "just put it somewhere for now," and it doesn't sort itself out.

---

## 1. Attempt one: a scripted, rules-based pipeline {#attempt-one}

The first pass was straightforward automation: a Python pipeline against the Drive API that classified files with an ordered list of `(category, [keywords])` rules, deduplicated exact-content matches by hash with a deterministic scoring function to auto-pick a "winner," repointed shortcuts instead of leaving them dangling, and — critically — split into a **read-only planning phase** and a **separate, explicitly-scoped apply phase**, so nothing with write access ever ran until the proposed classification had been reviewed as plain CSV data first.

Some of that held up well and is worth keeping regardless of what does the classifying:

- **A small, closed list of top-level categories**, instead of letting new ones spring up ad hoc.
- **A consistent internal shape per category** — a subfolder per person, a `_Joint` folder for shared documents, a `_Core` folder for reference material, a `General` catch-all, plus an explicit `Unsorted` bucket so "not yet categorized" is a visible state instead of a silent one.
- **Dedup by content hash, not filename**, with duplicates quarantined rather than deleted outright — a script should never get to unilaterally decide a real record is disposable.
- **Plan, then apply, as genuinely separate phases.** This is what turned a real failure into a non-event: an actual apply run against roughly 500 planned moves left about 90 failing outright with a 403 `insufficient authentication scopes` error, because the cached token had been minted under the planning phase's narrower, read-only scope. Because the plan itself was just reviewable data and every apply attempt was logged, that failure was just a log line to go fix — not a mess to clean up.

---

## 2. Where the script hit its ceiling {#the-ceiling}

What the script couldn't do was hold a reason, only a keyword. Real placement rules look like "if it proves who you are, it belongs here regardless of who issued it," or "if a doctor would care about it, it belongs in Health," or "this abbreviation looks like it belongs in one category but is excluded because of how a particular process works." Those are judgment calls rather than string matches, and each one eventually showed up as a misfile that had to be caught by hand and turned into another keyword-list exception, in a rule list that only grew.

That ceiling is why the first project's main output was a document, not a script. Writing down every "if X, then Y, because Z" rule in prose, in one place, as the reasoning rather than a keyword fragment, was worth more than the code that tried to enforce it. Calling the pipeline a failure isn't quite fair — it did the dedup, the shortcut hygiene, and the plan/apply safety rails correctly, and those still hold. But as a classifier it plateaued well below what the archive needed, and the document it forced into existence outlasted it.

---

## 3. What actually worked: two skills, one rulebook {#what-worked}

The fix replaced the keyword list with something that can actually *read*: two narrow, purpose-built Claude skills sitting on top of the archive, both anchored to the same reasoning document instead of a hard-coded rule table.

- **A filer**, triggered by anything that looks like filing work — a specific file pointed at, a batch of downloads to sort, someone just asking "where does this go?" It reads a file's actual content, decides what it is, and derives the correct name and location from the rulebook.
- **An auditor**, triggered by review requests ("are my files organized?", "anything out of place?") and also run proactively on a weekly schedule regardless of whether anyone asks. It sweeps the archive for naming/placement/duplicate violations and classifies each finding into "fix it automatically," "hand off to the filer," or "ask the user" — never all the way to silent judgment calls.

Both skills open with the same requirement: read the rulebook first, every run, and refuse to proceed if it's missing. Never fall back to memory or convention. That constraint carries a lot of weight. It's the difference between a rule document a person consults now and then and one an agent reloads fresh every session, which matters because an agent has no memory of last week's edge-case decision unless something outside it holds that decision in writing.

---

## 4. How the filer actually reads a file {#reading-a-file}

This is where "an agent instead of a script" turns from an abstract upgrade into a concrete one.

Identifying a document means reading it, and real-world scans are messy. The filer's fallback chain handles that rather than giving up:

1. Extract embedded text directly, when the file has any.
2. If that comes back empty — a scanned, image-only PDF — run OCR against just the first couple of pages. Deliberately not the whole document: identifying what something is and who it's about doesn't need every page, and burning that cost on the full file for every scan adds up fast.
3. If the OCR text itself comes back garbled — which happens more with some scripts and fonts than others — fall back one level further and actually look at the extracted page image directly instead of trusting the unreliable text. A slightly-rotated or mirrored scanner export gets corrected before that final look, rather than just accepted as unreadable.

Only when nothing can be extracted — an encrypted file, an unreadable scan even after all of that — does it stop and ask instead of guessing. That three-tier fallback, ending in "look at the page before giving up," is not something a keyword-matching script could approximate.

From there the naming itself follows the rulebook directly: a date prefix (only if a date can actually be confidently determined from the content — never invented), a descriptive body specific enough to identify the document without opening it, consistent handling of acronyms and institution names, the original extension preserved.

---

## 5. The automation boundary: when to just do it vs. when to ask {#automation-boundary}

Where a file currently sits changes how much autonomy the filer has, and the reason is simple: a file's current location is itself information. Something in an inbox-style holding folder isn't a deliberate choice yet, so the filer renames and moves it outright, no confirmation, and only stops to ask if the content can't be identified at all.

A file already inside a real category folder is different. Someone put it there on purpose, even if the name is wrong, so moving it always gets proposed and confirmed rather than applied silently. Even a same-folder rename gets a check first: does the new name change what the file appears to be about — who it belongs to, what type of document it is, what it's for? A pure formatting fix (casing, spacing, date format) goes through without asking. Anything that shifts apparent ownership or purpose comes back as a proposal with the reasoning attached, because that name might have been chosen deliberately, and guessing wrong is worse than asking.

The same instinct shows up in the auditor's own triage: fix silently only when it's mechanical and reasoning-free, hand off anything content-dependent to the filer, and ask the user for anything that requires guessing intent — including a flat rule to never silently repoint a broken cross-reference, never invent a missing piece of metadata, and never reorder or merge content without a human confirming the guess first.

---

## 6. Keeping the living notes honest, not just the archive {#living-notes-honest}

The archive isn't the only thing that can drift — a parallel set of running reference notes (a per-topic, always-current summary, separate from the point-in-time source documents backing it) has two independent ways of rotting, and the auditor checks both, deliberately treating them as unrelated failure modes rather than one:

**Freshness against the source archive.** When a new document lands in a category that a note is meant to summarize, that note should get updated as part of filing it — but if that sync step gets skipped, the note quietly falls behind whatever the archive itself now shows. The check is simple: compare the newest relevant source file's date against what the note's own metadata claims it reflects. Deliberately *not* re-extracting anything to check this — that's real, costly work, and the freshness check is meant to stay a cheap weekly sweep that just flags what's behind, handing the actual re-sync off separately.

**Internal consistency, independent of the archive.** A note can be perfectly in sync with the archive and still be quietly broken, because these are notes a person edits directly, by hand, not exclusively through the filing skill. So the auditor separately checks: cross-references between notes that no longer resolve to anything (a rename or deletion elsewhere silently orphaned the link), metadata that says a note was last touched on one date while its own content log shows a later edit, section ordering drifting back toward an older layout after a manual edit, reference notes nothing links to anymore, and markdown tables where a row's been hand-edited into having the wrong number of columns. There's also a specific content-drift heuristic — a "snapshot, not encyclopedia" principle, where general explanatory content that belongs in a shared reference note has crept back into a note that's supposed to hold only person-specific facts. That one's explicitly a heuristic to flag for review, not something to silently move on its own judgment.

One category of note gets a dedicated secondary sync path of its own, because it's structurally different from a narrative summary: a running numeric-trend table, wide format, one column added per new data point, tracked separately from the main note it's linked from. Keeping that kind of table honest needs its own small set of hard rules, learned the hard way rather than assumed upfront: standardize a new entry's label against what's already in the table before adding it as a new row — the same underlying measurement legitimately shows up under different names across different sources, and silently merging two rows that turn out not to be the same thing is worse than a harmless duplicate row flagged for a human to reconcile later. Guard explicitly against transposed or misread digits when transcribing a number by hand. And when a single source file happens to bundle more than one date's worth of readings together, double-check which figure belongs to which date rather than assuming page order lines up with chronological order — a real, named failure mode, not a hypothetical one.

A few operational choices behind this layer are worth calling out on their own, because they're the kind of thing that only becomes obvious after building it, not before:

- **A stale note is worse than no note**, because it looks authoritative right up until it's wrong. Every note tracks exactly which source files were actually read to produce it — and, just as importantly, which visible-but-unread files were skipped — so "trust this" is always checkable against a concrete list, not just an implicit claim.
- **Data sensitivity, residency, and access control are worth deciding deliberately, up front, rather than defaulting into.** A note-taking layer like this tends to outlive its first storage/sync choice, and a later change to that setup can silently move where sensitive content actually lives and who/what can reach it. Whoever's building this should settle that policy for their own situation before the notes exist, not after.
- **There's no API for "edit this note in place" the way there is for moving a Drive file.** An agent can read source material and draft an updated note, but landing that draft still needs a live local connection to wherever the notes live, or a manual step through the archive's version history. Automating the extraction and the drafting is most of the value, but it's worth being clear about where the automation stops instead of implying the whole loop closes itself.
- **Plain links back to the source document, not an embedded copy.** Slightly more friction to open a source file from a note, in exchange for zero extra sync infrastructure and something that works identically from any device. A small tradeoff, made deliberately rather than defaulted into.

---

## 7. Inside the philosophy document {#the-philosophy-doc}

Stripped of anything specific to my own household, the rulebook's shape is worth describing on its own, because the *shape* is the reusable part — and the top-level category list specifically is worth sharing close to verbatim. Landing on a *stable* category boundary is the hardest part of this whole exercise, harder than any of the automation built on top of it, and it's also the most reusable across households: what a document *is about* generalizes; the specifics of any one archive don't.

The rule that matters more than any individual category name: **every category gets a one-line test, not just a label.** "Finance" as a bare word invites endless debate about where a mortgage statement goes; "if it affects net worth, cash flow, or taxes" settles it in one read, for that document and every future one like it.

| Category | Placement test |
|---|---|
| Identity | Proves who you are — belongs here regardless of who issued it. |
| Immigration | Affects where you're legally allowed to live. |
| Health | Something a doctor would care about. |
| Insurance (non-health) | Limits financial damage from an adverse event. |
| Legal | Creates or modifies a binding obligation or authority. |
| Finance | Affects net worth, cash flow, or taxes. |
| Home | Changes when you move. |
| Work | Matters only because of where you're employed. |
| Family | The organizing axis is a specific person (non-primary family member), not a topic — see the override rule below. |
| Personal | Losing it is annoying, not dangerous. |
| Individual | About you as a person, outside of work or family. |
| Unsorted | Explicitly "not yet categorized" — a real bucket, not a place things drift by default. |

A few things about that list generalize past any one household. It's short on purpose — a dozen or so buckets is few enough to hold in your head, which matters more than being exhaustive, since an `Unsorted` escape hatch means it never *needs* to be exhaustive. Every row is a test, not a topic — "what would someone searching for this actually assume it's filed under" beats "what's this document about" as the question to design each row around. And a couple of categories exist specifically to prevent a subtler failure than plain sprawl: **Individual** exists because "about you, but not work and not family" is a real, recurring bucket that otherwise silently collapses into an ever-vaguer "Personal," and **Family** deliberately overrides every other category for a defined set of people, because *who* a document is about occasionally needs to outrank *what* it's about — worth deciding once, explicitly, rather than re-litigating per document.

- **A subfolder-pattern table**, separate from the category table — person-based, joint, by-institution, by-year, by-asset, by-project, or a staging/inbox pattern for anything not yet triaged — because *what* a document is about and *how* it should be sliced within its category are genuinely different questions.
- **Explicit naming conventions**: a consistent case style, dates always prefixed and always in a sortable numeric form, acronyms handled consistently, every file required to have a real extension.
- **Small, explicit exception tables** — a handful of institution names canonicalized to one spelling instead of drifting across variants, and a short list of terms that look like typos but are actually correct and should never get "corrected" or flagged.
- **An override rule for a specific subset of people** whose documents get filed by *who* rather than by *topic*, regardless of what category the document would otherwise match.
- **A conflict-resolution priority ladder** for the genuinely ambiguous cases, plus a fallback heuristic ("who would actually go looking for this document?") for the ones the ladder still doesn't resolve.
- **An explicit philosophy on shortcuts**: pointers only, never primary storage, never allowed to point at a folder, and — learned the hard way — certain sync-client-managed link files should never be touched directly by an automated process at all, because doing so corrupts the sync state rather than just misfiling something.

It ends with a line that's stuck with me past this one project: *clever systems decay, obvious systems persist.* The entire document is built around that — every rule is written to be re-derivable by a tired human (or a fresh agent with no memory of the last conversation) glancing at it cold, not just executable by whatever wrote it originally.

---

## 8. What carried over from the first attempt {#the-lesson}

It's easy to write off the first attempt once the second one works better. But the discipline the script enforced — plan before you apply, quarantine before you delete, log every action, never let the thing doing the classifying also hold write access — still matters with an agent in the classifier's place. An agent making placement judgment calls needs those guardrails as much as a keyword matcher did, probably more. The ask-vs-auto boundary above is the same instinct pointed at a different kind of decision-maker.

The reasoning document that made the second approach work came directly out of the first attempt's constraint: a keyword list forces you to write "why does this belong here" as an explicit rule, one category at a time. Without that constraint, the document might never have gotten written.

---

## 9. The living-reference layer {#living-reference}

Most of what lives in a personal archive is a point-in-time record — filed once, correct forever, never meant to change. A smaller category of document is meant to stay current instead. The running reference notes described above are that category — a summary meant to be trusted as accurate *today*.

Keeping something like that current used to mean remembering to sit down and manually re-edit it every few months, which is exactly the kind of maintenance that quietly stops happening. Now an agent reads whatever new, structured source material lands in a relevant category and folds it into the note that summarizes it, the same way it's already reading the archive's own rulebook to decide where things belong. That needs real structured data to read, which is what [the Health Connect → Drive sync project]({% post_url 2026-08-06-health-connect-google-drive-sync-android %}) exists to produce: clean, structured, machine-readable source data landing in exactly the right place in this same archive, rather than one more pile of point-in-time records nothing goes back and reads again.

Building this inside Google Drive, rather than some other cloud store used as dumb storage, has a payoff that's easy to miss: the same organized archive ends up queryable three ways, because Drive is a first-class data source for Google's own AI tooling. The Living Reference notes are one interface — curated, narrow, current-state summaries with links back to source. The archive itself is a second: Gemini can be pointed at that same Drive and asked open-ended questions across the whole corpus, with no separate indexing pipeline or export step to maintain. Drive's own search and folder browsing is a third, for when a file just needs to be found by hand. None of the three needed extra infrastructure once the archive was clean, and the work that went into cleaning the data is what makes all three trustworthy.

---

## End state {#end-state}

- A small, closed set of top-level categories with a consistent internal shape, carried over unchanged from the first attempt because that part was right from the start.
- Placement and naming decided by something that can actually read a document — text extraction, falling back to OCR, falling back to just looking at the page — not match a keyword against a filename.
- A sharp automation boundary: act freely on genuinely unfiled material and purely cosmetic fixes, always propose and confirm anything that could change what a file appears to mean.
- A weekly audit that checks the archive's naming and placement *and* a separate layer of running reference notes for two independent kinds of drift — falling behind new source material, and rotting internally from hand-edits — rather than assuming "in sync" and "internally consistent" are the same thing.
- A `_Core`/reference layer maintained less by remembering to revisit it and more by an agent reading real source material on an ongoing basis, with hard-won rules against the specific failure modes (mismatched labels, transposed digits, misattributed dates) that actually showed up.
- Three independent ways to ask the same archive a question — curated reference notes, open-ended natural-language search across the whole corpus, and plain file browsing — none of which needed separate infrastructure, because the underlying data was clean.
- A reasoning document that turned out to be the actual deliverable of the "failed" first attempt, not the classifier it was built to be.
