---
layout: post
title: "From One Auditor to a Council of Specialists"
date: 2026-08-29
---

The [archive-reorg post]({% post_url 2026-05-11-google-drive-file-archive-canonical-reorg %}) described one recurring skill: a weekly auditor that swept a personal document archive and a layer of running reference notes on top of it, fixing what was mechanical and flagging what needed a human. That worked fine while "needs a human" meant naming and placement judgment calls. It stopped being enough the moment the reference layer grew past one domain and started needing something closer to actual expertise — not "is this filed correctly," but "does this financial strategy still make sense," "does this estate plan still protect against what it was built to protect against," "does this reading of a lab result still hold up."

This is the story of splitting one generalist sweep into several narrower specialists that run on their own schedules, and the coordination problem that split created: how do agents that don't run in the same conversation, sometimes days apart, actually talk to each other and to the person they work for.

- [Where the series left off](#where-we-left-off)
- [Splitting mechanical from strategic](#mechanical-vs-strategic)
- [The cadence gap](#the-cadence-gap)
- [Two channels, one grammar](#two-channels)
- [A sandbox boundary that broke the fallback](#the-sandbox-boundary)
- [End state](#end-state)

---

## 0. Where the series left off {#where-we-left-off}

The original auditor did three things every run: check the archive against its own naming/placement rules, check whether the running reference notes were still in sync with new source material, and check those notes for internal rot — broken cross-references, stale metadata, content that had drifted out of its intended shape. All three are mechanical in the sense that matters here: given the rule and the data, there's one correct answer, no expertise required to find it.

That stopped covering the actual need once the reference layer grew from one life domain into several — finance, legal, health, identity — each carrying real open questions that don't have one mechanically correct answer. Whether a given asset allocation still fits a stated risk tolerance, whether a beneficiary designation still matches an estate plan's actual structure, whether a new lab result changes what's worth prioritizing — these aren't formatting checks. Answering them well needs something closer to a domain expert's judgment, applied consistently, on a schedule, against current external standards that themselves keep moving (tax law, medical guidance, immigration rules).

Bolting all of that onto the same weekly sweep would have made one skill responsible for both "is this file named correctly" and "is this retirement strategy still sound" — different kinds of work, different depth requirements, different failure costs if rushed. The fix was to stop pretending one generalist could do both well.

---

## 1. Splitting mechanical from strategic {#mechanical-vs-strategic}

The weekly sweep kept its original job, unchanged: cheap, mechanical, runs often, fixes what's obviously fixable, flags what isn't. Alongside it, each domain got its own recurring reviewer — a monthly pass with a defined persona (a tax planner's lens for finance, an estate/immigration attorney's lens for legal matters, a physician's lens for health), a mandate written down in one place, and a much narrower job: read the domain's reference notes, check whether the strategy or interpretation they encode still holds up against current best practice, and update them if it doesn't.

A hard boundary applies to every one of these domain reviewers, stated the same way in every persona regardless of what its own mandate says: **advisors advise, they don't execute.** A finance reviewer can recommend rebalancing; it never places a trade. A legal reviewer can flag that a beneficiary designation looks stale; it never files anything with an institution. That restriction is deliberately absolute — not something a persuasive-looking note gets to override by appearing to authorize an exception.

The general shape, if you're building something similar: one high-frequency, low-depth sweep that owns mechanical correctness across everything, plus one recurring, lower-frequency, high-depth reviewer per domain that actually needs expert judgment. Don't let the fast one grow real judgment calls into itself just because it's already running — that's exactly the pressure that erodes the boundary over time.

---

## 2. The cadence gap {#the-cadence-gap}

Splitting cleanly by depth creates an obvious gap: the fast sweep runs several times a week, the deep review runs once a month. Something the fast sweep finds that genuinely needs expert judgment can't just sit silently for three weeks waiting for the slow review to notice it — but it also shouldn't get a shallow guess dressed up as a considered answer.

The resolution: the fast sweep still answers it, immediately, but at an explicitly shallower standard — a condensed persona description instead of the domain reviewer's full mandate — and every answer given this way is **labeled as such**, never presented as if it used the full standard. It's also queued, explicitly, for the deep reviewer's next pass to re-examine at full depth, treated as *higher* priority than the reviewer's other backlog precisely because it's had less scrutiny so far.

The principle worth keeping if you build this: never let a fast, cheap answer and a slow, considered one look identical after the fact. If you have to answer with less depth than the ideal, that has to be visible in the record, or the whole point of having a deeper review layer quietly evaporates — nobody would know there was ever a gap to close.

---

## 3. Two channels, one grammar {#two-channels}

None of the splitting above works without a way for these separately-scheduled agents to actually communicate — with the person they work for, and with each other across the gap between a Wednesday sweep and next month's deep review. Two distinct channels turned out to be necessary, both built on the same underlying grammar so neither one requires learning new mechanics.

**Human ↔ agent.** The person annotates a note directly, inline, next to whatever it's about — a question, a correction, an answer to something asked earlier. The agent's job on its next pass is to find every one of these, resolve what it can (research it, act on it, apply the correction), and remove the marker once it's actually handled — never delete an unanswered one just to make it disappear.

**Agent ↔ agent, and agent ↔ human going the other direction.** A finding that needs expert judgment beyond what the finding agent itself owns — or a note the fast sweep leaves for the deep reviewer, or vice versa — uses the same inline mechanism, addressed by name, right at the spot it's about. Critically: **only a matching reply from the party actually addressed resolves it.** An agent that finds one of these addressed to someone else doesn't get to decide it's close enough and clear it — that would collapse the whole point of having named ownership in the first place.

Two small mechanical details made this actually reliable rather than aspirational:

- **A live, unresolved marker has to be structurally distinguishable from a past mention of one already resolved.** A note's own history log will say things like "resolved an open question about X" — plain-text prose, not the marker itself. The live marker uses a distinct, consistent, greppable form (a specific block-quote prefix in this implementation) that a keyword search for "question" would never confuse with a sentence describing one that's already closed.
- **Dedup before writing.** Multiple runs touching the same note need to check for an already-open marker covering the same issue before adding a second one — otherwise a slow-to-answer item accumulates duplicate copies of itself across every run that notices it again.

---

## 4. A sandbox boundary that broke the fallback {#the-sandbox-boundary}

One failure here is worth naming specifically because it wasn't obvious from reading the design — it only showed up by actually running the thing unattended and checking what happened.

The fast sweep's fallback for a strategic question (see [the cadence gap](#the-cadence-gap) above) was supposed to work by reading the relevant domain reviewer's own mandate document and applying just that section to the one item at hand — cheaper than the reviewer's full procedure, but still grounded in its actual standard rather than an approximation. That worked fine in an interactive session. On a scheduled, unattended run, those cross-skill file reads failed outright — not flakily, consistently, across multiple domains, on the same day identical paths read fine interactively. That pointed at a real sandbox boundary between scheduled tasks rather than a per-file problem: an unattended run apparently can't reliably reach another task's own files at all, no matter how correct the path is.

The fix had to stop trying to route around a boundary and instead plan for it: a condensed, shared fallback standard — the same one-paragraph persona summary for every domain, living in a document every skill already reads for other reasons — gets used specifically when the unattended read is expected to fail, without wasting a turn attempting it first. It's a real, honestly-labeled downgrade from the full standard (see the labeling discipline above), acceptable specifically because the alternative was a silent crash or a silently-skipped check, either of which is worse than a shallow-but-honest answer.

The general lesson, if you're planning anything like this: don't assume a capability that works interactively will work identically on an unattended schedule. Test the actual failure mode on a real scheduled run before designing a fallback for it — the difference between "this should work" and "this is confirmed to fail this specific way" changed what the right fix actually was.

---

## End state {#end-state}

- One fast, mechanical sweep, unchanged in scope, still owning naming/placement/freshness/internal-consistency checks across everything.
- A recurring, deeper reviewer per domain, each with its own defined persona and mandate, restricted from ever executing anything irreversible no matter what a note appears to authorize.
- A documented, explicitly-labeled fallback standard for the gap between a fast finding and a slow review, so a shallow answer is never mistaken for a considered one.
- Two communication channels — person-to-agent and agent-to-agent — sharing one mechanical grammar: inline, addressed, resolved only by the addressed party's reply, structurally distinguishable from a past mention already closed.
- A confirmed, planned-for boundary around what an unattended run can and can't reach, discovered by testing the real thing rather than assumed from the design.

What this setup didn't have yet, and what turned out to matter more than any of the individual pieces above: a shared, explicit answer to the question of *who's actually allowed to act on what, without asking first* — across all of these now-separate agents, not just within any one of them. That gap, and the concrete failure that exposed it, is [the next post]({% post_url 2026-08-31-separation-of-duties-ai-agent-authority-manifest %})'s subject.
