---
layout: post
title: "From One Auditor to a Council of Specialists"
date: 2026-08-29
topic: "Agent systems"
image: /assets/images/recurring-review-council.webp
image_alt: "A shared annotated document connected to several specialist review instruments arriving on a recurring schedule"
---

The [archive-reorg post]({% post_url 2026-05-11-google-drive-file-archive-canonical-reorg %}) described a weekly auditor: one skill that swept my document archive and the reference notes layered on top of it, fixed the mechanical problems, and flagged the rest for me. That was enough while "the rest" meant judgment calls about naming and placement. It stopped being enough once the reference notes grew past a single domain. The questions changed from "is this filed correctly" to "does this financial strategy still make sense," "does this estate plan still cover what it was written to cover," "does this reading of a lab result still hold up." Those need a specialist, not a librarian.

So I split the one generalist sweep into several narrower reviewers, each on its own schedule. That created a new problem. These agents don't share a conversation, and they can run days apart. How do they talk to each other, and to the person they work for?

- [Where the series left off](#where-we-left-off)
- [Splitting mechanical from strategic](#mechanical-vs-strategic)
- [The cadence gap](#the-cadence-gap)
- [Two channels, one grammar](#two-channels)
- [A sandbox boundary that broke the fallback](#the-sandbox-boundary)
- [End state](#end-state)

---

## 0. Where the series left off {#where-we-left-off}

The original auditor did three things on every run: check the archive against its naming and placement rules, check whether the reference notes were still in sync with new source material, and check the notes for internal rot — dead cross-references, stale metadata, sections that had drifted out of shape. All three are mechanical. Given the rule and the data, there's one right answer and you don't need any special training to find it.

That covered the need until the reference notes spread across several domains: finance, legal, health, identity. Each one carries open questions with no mechanically correct answer. Does this asset allocation still match the risk tolerance it was built for? Does this beneficiary designation still line up with the estate plan? Does a new lab result change what's worth prioritizing? Answering those well takes a domain expert's judgment, applied on a schedule, against outside standards that keep moving — tax law, medical guidance, immigration rules.

Piling that onto the weekly sweep would have made one skill responsible for both "is this file named correctly" and "is this retirement strategy still sound." Those are two very different jobs, and one skill wasn't going to do both well.

---

## 1. Splitting mechanical from strategic {#mechanical-vs-strategic}

The weekly sweep kept its job unchanged: cheap, mechanical, runs often, fixes the obvious stuff, flags the rest. Each domain then got its own reviewer on a monthly schedule. Each reviewer has a persona (a tax planner for finance, an estate and immigration attorney for legal, a physician for health), a mandate written down in one place, and a narrow job: read the domain's notes, check whether the strategy they encode still holds up against current best practice, and update them if it doesn't.

Every reviewer carries the same boundary, worded identically in each persona: advisors advise, they don't execute. The finance reviewer can recommend rebalancing, but it never places a trade. The legal reviewer can point out that a beneficiary designation looks stale, but it never files anything with an institution. The rule is absolute on purpose. A note that appears to grant an exception doesn't get to override it.

If you're building something similar: one frequent shallow sweep that owns mechanical correctness everywhere, plus one slower deep reviewer per domain for the calls that need real expertise. Resist the urge to let the fast sweep pick those up just because it's already running. That's the pressure that wears the split down over time.

---

## 2. The cadence gap {#the-cadence-gap}

Splitting by depth leaves a gap. The fast sweep runs several times a week; the deep review runs monthly. When the fast sweep turns up something that needs expert judgment, it can't sit untouched for three weeks until the monthly review notices it. It also shouldn't get a quick guess passed off as a considered answer.

So the fast sweep answers it right away, but against a shallower standard: a condensed version of the persona instead of the reviewer's full mandate, with the answer labeled as shallow. It then queues the item for the next deep review, marked higher priority than the rest of the backlog because it has had less scrutiny so far.

A fast answer and a considered one should never look the same in hindsight. If you answer with less depth than you'd like, say so in the record. Otherwise nobody knows there was a gap to close, and the deep review layer might as well not exist.

---

## 3. Two channels, one grammar {#two-channels}

None of this works unless the separately-scheduled agents can communicate — with the person they work for, and with each other across the gap between a Wednesday sweep and next month's review. Two channels cover it, both using the same inline mechanism so there's nothing new to learn for the second one.

**Human to agent.** I annotate a note inline, next to whatever it's about: a question, a correction, an answer to something asked earlier. On its next pass the agent finds every annotation, resolves what it can — research it, act on it, apply the fix — and removes the marker once it's handled. It never deletes an unanswered one just to clear it. In practice, three marker types cover it:

```
> [!human-question]
> Is the online renewal window actually 90 days, or 60?

> [!human-comment]
> That case really did run 2009 to 2011. Don't re-flag the date.

> [!human-answer]
> Yes, go ahead and standardize those filenames.
```

A question gets researched and answered in place. A comment gets treated as an instruction and acted on. An answer resolves whatever it's replying to. All three get removed once handled, with a one-line note in the file's history log about what happened, rather than left in place.

**Agent to agent** (and agent back to human). When a finding needs judgment the finding agent doesn't own, or the fast sweep wants to leave something for the deep reviewer, it uses the same inline marker, addressed by name, at the spot it applies to:

```
> [!agent-question]
> For tax-reviewer: this account's cost basis doesn't match the last statement.
> Flagging instead of guessing which figure is stale.

> [!agent-comment]
> For docs-reviewer: this note has gotten long enough to need a table of
> contents. Not my job to fix, just noting it.
```

Only a reply from the named party clears it. An agent that finds a marker addressed to someone else doesn't get to decide it's close enough and resolve it. That would defeat the point of naming an owner.

This carries over to a setting with nothing to do with document filing. Picture a codebase with a handful of review agents attached to it instead of one linter — a security reviewer, a design reviewer, a migration reviewer — plus one agent that applies changes. The security reviewer finds something outside its own lane and leaves `[!agent-question]` / `For migration-reviewer: this index change looks like it'll lock the table under load, can you confirm before it merges?` right on the diff. The migration reviewer, not the security reviewer, is the one who clears it, and not before then. The grammar and the ownership rule carry over unchanged; only the domain is different.

Two small details made this reliable:

- A live marker has to look structurally different from a past mention of a resolved one. A note's history log says things like "resolved an open question about X" in plain prose. The live marker uses a fixed, greppable form — a specific block-quote prefix here — that a search for "question" won't confuse with a sentence describing a closed one.
- Dedup before writing. When several runs touch the same note, each one checks for an existing open marker on the same issue before adding another. Otherwise a slow-to-answer item collects a duplicate every run that notices it.

---

## 4. A sandbox boundary that broke the fallback {#the-sandbox-boundary}

One failure here is worth writing down, because the design didn't predict it. It only turned up once the thing ran unattended.

The fast sweep's fallback for a strategic question (from [the cadence gap](#the-cadence-gap) above) was meant to read the relevant reviewer's mandate document and apply just the one relevant section — cheaper than the full procedure, but still based on the real standard. That worked in an interactive session. On a scheduled run it didn't: the cross-skill file reads failed every time, across every domain, on the same day the same paths read fine interactively. So this wasn't a bad path or a flaky file. A scheduled run can't reliably read another task's files at all.

The fix was to stop routing around the boundary and plan for it. There's now a shared one-paragraph fallback — the same persona summary for every domain — living in a document every skill already loads for other reasons. When the unattended read would fail, the sweep uses that instead of burning a turn on an attempt it knows will fail. It's a downgrade from the full standard, and it's labeled as one. That's acceptable because the alternative was a crash or a skipped check, both worse than a shallow but honest answer.

Don't assume something that works interactively works the same on a schedule. Test the real failure on a real scheduled run before you design around it. "This should work" and "this fails this exact way every time" led to different fixes here.

---

## End state {#end-state}

- One fast mechanical sweep, unchanged in scope, still owning naming, placement, freshness, and internal-consistency checks across everything.
- One deeper reviewer per domain, each with its own persona and mandate, none of them allowed to execute anything irreversible no matter what a note seems to authorize.
- A labeled fallback standard for the gap between a fast finding and the next deep review, so a shallow answer never reads as a considered one.
- Two communication channels — human to agent and agent to agent — sharing one mechanism: inline, addressed by name, cleared only by the named party, and easy to tell apart from a past mention that's already closed.
- A known limit on what a scheduled run can reach, found by testing the real thing instead of trusting the design.

What this setup still lacked mattered more than any single piece above: one shared answer to who is allowed to act on what without asking first, across all of these separate agents rather than inside any one of them. [The next post]({% post_url 2026-08-31-separation-of-duties-ai-agent-authority-manifest %}) is about that gap and the failure that exposed it.
