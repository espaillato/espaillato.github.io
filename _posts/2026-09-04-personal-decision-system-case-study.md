---
layout: post
title: "A Personal Decision System Built on Top of a Document Archive"
date: 2026-09-04
topic: "Personal systems"
cover: grid
---

The archive described in [an earlier post]({% post_url 2026-05-11-google-drive-file-archive-canonical-reorg %}) solved a filing problem. Documents had stable names, a small set of categories, and explicit rules for the cases that did not fit neatly. That made the archive easier to maintain and search, but it was still an archive: useful when I knew what to look for, less useful when the question was what deserved attention now.

I added a decision layer on top of it. Source documents stay in the archive. Short dashboards describe the current state of a few important areas. Deeper reference notes hold the supporting detail. Scheduled reviewers check both the facts and the recommendations, while a separate maintenance process keeps the underlying files organized and the summaries current.

This post describes that method as a sanitized case study. The personal data is not the reusable part. The reusable part is the shape of the system, the division of responsibility, and the rules that keep a concise summary from becoming either stale or enormous.

- [The problem the archive did not solve](#archive-limit)
- [The architecture](#architecture)
- [Why Markdown and Obsidian](#markdown-obsidian)
- [What belongs in a dashboard](#dashboard)
- [Keeping evidence separate from conclusions](#evidence)
- [Two maintenance loops](#maintenance-loops)
- [The review layer](#review-layer)
- [The unattended-run problem](#unattended-runs)
- [What has to be sanitized](#sanitization)
- [A reusable starter version](#starter-version)
- [What I would measure next](#measurement)
- [End state](#end-state)

---

## 0. The problem the archive did not solve {#archive-limit}

A well-organized archive answers retrieval questions: where is the latest statement, which document superseded the old one, what was the result of a prior appointment, when does an identification document expire. Those are valuable questions, but they begin with someone remembering to ask.

The more useful questions cut across documents:

- What has changed since the last review?
- Which open items have become time-sensitive?
- Does a recommendation still fit the current facts?
- Are two individually reasonable recommendations inconsistent when combined?
- What should I bring to the next conversation with a doctor, accountant, attorney, or institution?

Answering those directly from a large archive every time is possible, but inefficient. It repeats extraction work, produces long answers, and makes it difficult to distinguish a source fact from a current interpretation of that fact. The system needed a small current-state layer that could be read in minutes and checked against the evidence behind it.

The result is less a second archive than a set of maintained views over the first one.

## 1. The architecture {#architecture}

The system has three layers:

1. **Source archive.** Original statements, reports, forms, scans, exports, and correspondence. These remain the record of what actually happened.
2. **Living reference.** Short dashboards for current state and actions, plus linked reference notes for analysis, history, definitions, and calculations.
3. **Review loop.** Recurring maintenance and specialist reviews that keep the first two layers aligned and reconsider conclusions as circumstances or outside standards change.

The flow is intentionally one-way at the evidence boundary:

```
source documents -> extracted facts -> current dashboard -> review -> action or question
```

A review may correct an extracted fact after checking the source, but a polished dashboard does not become evidence merely because it is concise and confidently written. The source remains the source.

The archive in this case contains several hundred documents across a dozen broad categories. Only a subset needs a living dashboard. Most documents are point-in-time records that can be filed once and left alone. A tax return from several years ago does not need a monthly rewrite. A current financial allocation, medication list, renewal date, or unresolved estate-plan item might.

That distinction keeps the maintained surface small enough to be credible.

## 2. Why Markdown and Obsidian {#markdown-obsidian}

An early design decision was to store the Living Reference as Markdown and use Obsidian as its primary view.

Markdown keeps the underlying material portable. The notes are plain text, readable without a particular application, easy to version and search, and straightforward for scripts or review tools to process. If the viewing tool changes later, the information does not need to be extracted from a proprietary database first.

Plain text alone is not a particularly good daily interface, though. Obsidian adds the human-facing layer: navigation, backlinks, cross-note links, headings, tables, search, and a graph of how related information connects. A dashboard can link to its detailed history, a current action can link to the reasoning behind it, and a shared definition can support several notes without being copied into each one.

That combination matters because the system has two audiences. Automated processes need predictable, tool-friendly text. A person needs to move through the information naturally and understand why one item connects to another. Markdown serves the first requirement without obstructing the second; Obsidian makes the same files comfortable to use without taking ownership of them.

The design is therefore not “an Obsidian database.” It is a portable Markdown knowledge base with Obsidian as a particularly useful reader and navigator. The distinction is small until the day a tool changes, at which point it becomes the whole portability plan.

## 3. What belongs in a dashboard {#dashboard}

Each dashboard is meant to answer, quickly:

- What is the current state?
- What is driving the outcome?
- What needs action?
- What is missing or uncertain?
- When was this last checked?

Everything else has to justify its place.

The first versions accumulated chronological narratives, definitions, old decisions, and long explanations inside table cells. All of that was relevant, but relevance is not the same as usefulness on the main page. A dashboard that takes twenty minutes to read has stopped being a dashboard.

The working rule became: conclusions and current actions stay in the dashboard; evidence, derivations, and history move to linked reference notes. A line such as “confirm whether this account still matches the household allocation” belongs in the dashboard. The account history, allocation calculation, and reasoning behind the concern belong one link away.

The same rule applies to update logs. A log is useful evidence that a note is maintained, but an unlimited log makes every future read more expensive. Recent entries stay in the dashboard; older entries roll into a history note. Nothing is deleted, and the current page does not have to carry its entire biography around with it.

## 4. Keeping evidence separate from conclusions {#evidence}

Each current fact links back to a real source document when one exists. The link is not decorative. It makes the summary auditable and gives a professional the full context without requiring a second search through the archive.

The reference layer handles material that is useful but too large or too stable for the dashboard:

- multi-year numeric trends;
- detailed visit or transaction history;
- calculations and assumptions;
- definitions shared by more than one person or dashboard;
- the reasoning behind a recommendation;
- the full history of prior changes.

This separation also makes corrections less confusing. A source value, a calculated trend, and a recommendation are three different kinds of claim. When they live in different places, a correction to one does not silently rewrite the others.

There is a practical trust rule underneath this: a summary should say which sources were read and which visible sources were not. “Current through this date based on these documents” is a checkable statement. “Current” by itself is mostly optimism.

## 5. Two maintenance loops {#maintenance-loops}

The system separates mechanical maintenance from strategic review.

The **frequent maintenance loop** handles work with a mostly deterministic answer: naming and placement, missing links, stale metadata, malformed tables, a newer source document that has not been reflected in a dashboard, or an unresolved question waiting in a note. It runs often because the checks are comparatively cheap.

The **slower review loop** handles questions that require judgment: whether a financial strategy still matches its constraints, whether an estate plan still covers the risks it was designed for, whether a health priority should change, or whether a renewal rule has changed. Those reviews run less often and use a written domain mandate.

This division prevents the filing process from casually becoming a financial, legal, or medical reviewer merely because it noticed something while moving a file. It also prevents the specialist review from spending most of its time fixing filenames and broken links.

The two loops communicate through inline flags placed next to the relevant text. A person can leave a question or correction in a note. A maintenance pass can leave a question for a named reviewer. The marker remains until the named party resolves it, and duplicate checks prevent the same open issue from being added again on every run.

That mechanism is described in more detail in [the review-council post]({% post_url 2026-08-29-recurring-review-council-async-flag-protocol %}). The important point here is that the communication lives with the artifact, not only in a chat transcript or run report.

## 6. The review layer {#review-layer}

Each domain review has a written mandate: what it owns, which files it reads, what standards it applies, what it may change, and what it must never execute.

The reviewers are expected to do more than fact-check. They reconsider whether the current recommendation is still sensible given the full set of constraints. They also check the combined effect of several recommendations. Five reasonable changes can still add up to one unreasonable plan.

The output follows a simple contract:

- state the finding plainly;
- distinguish fact from inference;
- provide the reasoning and relevant numbers;
- identify what needs confirmation from a professional;
- update the dashboard and deeper reference note in their respective roles;
- never perform the real-world transaction or filing.

That last boundary matters. The system can prepare a better discussion with a professional and make omissions easier to spot. It does not place trades, change beneficiaries, submit government forms, prescribe treatment, or otherwise confuse analysis with authority.

An editorial reviewer has a different job. It does not make domain judgments. It keeps dashboards short, relocates historical narration, checks terminology and links, and makes sure a useful note has not gradually become a tome.

## 7. The unattended-run problem {#unattended-runs}

One operational issue appeared only when the reviews ran on a schedule. The frequent maintenance task sometimes needed the standards used by a specialist reviewer, but the review personas originally lived inside task-specific instructions that unattended runs could not reliably access because each reviewer runs in their own sandbox.

The first fallback was a short persona summary in a shared note. It kept the task from failing, but it created two versions of the standard: a full mandate for the specialist and a condensed one for everyone else. They could drift, and a shallow answer could look more complete than it was.

The fix was to externalize the review context into ordinary, versioned reference files that every relevant process can read. Each reviewer now has a mandate document, and the mechanics shared by all reviewers live in one shared protocol. Scheduled tasks point to those files instead of carrying private copies of the rules.

This is a small design change with a useful general lesson: if a recurring process depends on context, that context is part of the system's data. It should be stored somewhere accessible, reviewable, and versioned, not hidden inside the configuration of the one task that usually uses it.

## 8. What has to be sanitized {#sanitization}

Publishing the method is not the same as publishing a sample of the real system with a few names changed.

A safe case study removes or generalizes:

- names, account values, diagnoses, medications, document numbers, institutions, addresses, and exact dates tied to personal events;
- screenshots of dashboards, because combinations of harmless-looking fields can identify people;
- source links and file identifiers;
- folder names that reveal relationships, employers, providers, or legal structures;
- examples copied closely enough that the underlying event remains recognizable.

The sanitized version keeps the schema, rules, workflow, and failure modes. Example data should be synthetic from the start rather than redacted after the fact. Redaction is easy to get almost right, which is not a particularly reassuring privacy standard.

There is also a product boundary here. A reusable starter kit can operate entirely on a person's own storage and notes. A hosted service that ingests financial, health, identity, and legal documents takes on a much larger security and compliance problem.

## 9. A reusable starter version {#starter-version}

The smallest useful version does not need software beyond a file store and a note system. It needs a good template and a disciplined setup process.

I would package it as:

1. **A source-archive rulebook.** A small category list, a one-sentence placement test for each category, naming rules, a visible unsorted area, and explicit exceptions.
2. **A portable Markdown workspace.** Obsidian-ready notes and links, with no dependency on Obsidian-specific storage for the underlying content.
3. **A dashboard template.** Current status, drivers, actions, missing information, sources, and last-reviewed metadata.
4. **A reference-note template.** Analysis, calculations, history, and definitions linked from the dashboard.
5. **A reviewer mandate template.** Scope, required inputs, review procedure, authority boundaries, and output format.
6. **A shared review protocol.** How to handle inline questions, how to label uncertainty, how to check combined recommendations, and when to stop for human judgment.
7. **A privacy worksheet.** Where files live, what is allowed in summaries, what must remain only in source documents, and which actions are prohibited.
8. **A worked synthetic example.** Enough fake documents and dashboards to show the method without requiring anyone to inspect a stranger's bloodwork or tax return over breakfast.

The first implementation should be guided and local. A handful of pilots would show which rules generalize, where setup remains too dependent on the original archive, and whether the dashboards change decisions often enough to justify maintaining them.

## 10. What I would measure next {#measurement}

The system already measures its own activity reasonably well: files processed, notes updated, reviews completed, open markers found. Those are operational counts, not outcomes.

A productized method needs a smaller set of measures tied to usefulness:

- time from a new source document to an updated dashboard;
- age of the oldest unresolved action or question;
- number of decisions or professional conversations materially prepared by the system;
- number of stale or conflicting recommendations found during review;
- time spent maintaining the system versus time saved retrieving and reconstructing context;
- percentage of review runs that require manual repair;
- number of sensitive facts duplicated outside the source archive.

The last measure should remain close to zero. Convenience has a habit of volunteering other people's privacy as its first optimization.

## End state {#end-state}

- Original documents remain the evidence layer rather than being copied into a new database by default.
- Living Reference stays portable as Markdown, while Obsidian supplies navigation, backlinks, and a practical human interface.
- A small set of current dashboards answers what matters now and links back to the source.
- Detailed reasoning, calculations, and history sit one level deeper instead of inflating the dashboard.
- Mechanical maintenance and specialist judgment run on separate loops with separate authority.
- Review mandates and shared protocols live in accessible, versioned files, including for unattended runs.
- Inline flags keep questions attached to the relevant artifact until the named person or reviewer resolves them.
- The reusable package contains structure, rules, templates, and synthetic examples — none of the household data that proved the method on the first implementation.

The useful product here is not a pile of personal documents and not a chatbot pointed at a folder. It is a maintained path from evidence to a current summary, from that summary to a review, and from the review to a decision someone can inspect before acting. The documents will vary. The path does not have to.
