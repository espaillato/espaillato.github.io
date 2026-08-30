---
layout: post
title: "Separation of Duties for AI Agents: What Makes Parallel Agents an Actual Team"
date: 2026-08-31
---

[The previous post]({% post_url 2026-08-29-recurring-review-council-async-flag-protocol %}) described splitting one generalist sweep into several narrower agents, each with a defined scope, talking to each other through a shared inline-flag protocol. That solved coordination — agents could now leave each other messages across a scheduling gap without a human relaying them. It didn't solve a quieter problem underneath it: running several agents in parallel isn't the same thing as those agents actually functioning as separate, accountable specialists. Without something more explicit, they collapse right back into one undifferentiated authority that happens to be running in more than one process.

This post is about the concrete failure that exposed that gap, and the authority model built to close it — written to be taken and adapted directly, since the pattern isn't specific to a personal document system at all.

- [The bug that exposed it](#the-bug)
- [What actually makes it a team](#what-makes-a-team)
- [A concrete authority model: AUTO / FLAG / NEVER](#auto-flag-never)
- [Where the boundary line actually goes](#the-boundary-line)
- [Verification has to run both directions](#verification-both-directions)
- [The rule about the rules](#precedent-confirmation)
- [Generalizing past one project](#generalizing)
- [End state](#end-state)

---

## 0. The bug that exposed it {#the-bug}

A large sweep needed to cover more ground than fit comfortably in one pass, so the work got split across several parallel subagents, each handed a slice of the checklist and told, in short form, to apply the rules and report back. One of those rules had real teeth: certain findings weren't allowed to just sit in a report — they had to also get written as a standing, addressable marker at the exact spot they applied to, so the next run (or the person themselves) would actually see them without having to go dig through old chat output.

That requirement existed clearly in the source instructions. It did not survive being handed to the subagents. Each one was told, in effect, "list findings you'd normally flag for a human, in your report" — a reasonable-sounding paraphrase that quietly dropped the second half of the actual rule: *also write it as a standing marker.* The subagents did real, correct work otherwise. The reports were accurate. The markers simply never got written, because the instruction that would have produced them got compressed away somewhere between "what the rule actually says" and "what got typed into the delegation."

Nobody decided to skip that step. It just didn't make it through a summarization boundary that nothing was watching.

---

## 1. What actually makes it a team {#what-makes-a-team}

The tempting read of that bug is "the subagents made a mistake." The more useful read is that nothing about the setup had actually divided responsibility in the first place — it had only divided *labor*. Three processes ran instead of one, but the authority governing what any of them could do, and what they were obligated to do, was still one undifferentiated blob, re-derived from scratch (and re-compressed, lossily) every time it got handed off.

That's the actual distinction worth sitting with: **parallelism multiplies copies of the same undifferentiated authority. It doesn't divide responsibility.** A team, in any meaningful sense, requires that a given class of decision has a specific owner, that delegating a task doesn't strip the obligations attached to it, and that resolving something is gated to whoever actually owns it rather than to whoever gets there first. Without that, running five agents instead of one just means five chances for the same class of mistake, not five narrower areas of accountability.

Concretely, this points at one specific, boring-sounding fix: **the complete obligation has to travel with the delegation, verbatim, every time — not a summary of it, not a paraphrase, not a pointer to where it's documented elsewhere.** A reference to "follow the rules in the shared document" is not the same thing as restating the rule inline in the actual instructions the subagent receives. The first one survives compression badly. The second one doesn't have anywhere to lose the requirement, because there's no summarization step between the rule and the instruction — they're the same text.

---

## 2. A concrete authority model: AUTO / FLAG / NEVER {#auto-flag-never}

The fix took the shape of a three-tier authority manifest, restated inline in full at the top of every delegation rather than referenced by name:

**AUTO — proceed without asking, report what happened.** Reserved for genuinely mechanical actions: no judgment call, no ambiguity, the same input always produces the same correct output. Formatting fixes, applying an already-documented convention, moving something within a boundary that was never in question.

**FLAG — stop, write the question at the exact spot it applies to, take no action until it's answered.** Reserved for anything that requires judgment: a classification that could reasonably go more than one way, a change that would alter what something appears to mean, anything that would need inventing a new standing rule not already written down anywhere. Writing the flag *is* the action here — there's no version of this tier where the agent also quietly does the thing "just in case," even if its own confidence is high.

**NEVER — a short, absolute list, no exceptions regardless of how good the reasoning sounds in the moment.** This tier exists specifically to survive a persuasive-looking edge case. It should be short enough to memorize and specific enough that nothing in it requires judgment to apply.

The part that actually fixes the bug from above: every subagent dispatch now has to restate this manifest — the specific AUTO/FLAG boundary for *that task* — as literal text in its own instructions, not as a citation. Pointing an agent at a shared document by name is exactly the failure mode that already happened once; the fix isn't "trust the reference more," it's "don't rely on a reference surviving a compression step at all."

---

## 3. Where the boundary line actually goes {#the-boundary-line}

An authority model is only as good as where its lines actually sit, and the first version of this system had the line drawn too conservatively to be usable day to day. The original rule was blunt: anything already in its intended place, moved anywhere at all, always required asking first — safe, but it meant routine internal reorganization (splitting a folder into subfolders, renaming a container once its contents outgrew the old name) generated exactly as many questions as a genuinely ambiguous reclassification. A rule that asks constantly gets its answers rubber-stamped eventually, which defeats the point of asking at all.

The fix was a narrower, still-safe distinction: restructuring *within* an already-correct top-level boundary is AUTO — nothing about a subfolder split or a rename changes what category something fundamentally belongs to. Moving something *across* that top-level boundary is FLAG — that's an actual reclassification judgment call, not a tidy-up, no matter how confident the proposed new placement looks. The two moves can look superficially similar (both are "moving a file") but they're answering completely different questions, and only one of them needs a human in the loop.

If you're drawing this line for your own system: the test isn't "did anything move." It's "does this change what category of thing something fundamentally is, once the move completes." A rename that changes apparent ownership or purpose is a reclassification even if the file never left its folder. A restructure that keeps everything inside the same top-level boundary isn't, even if every file in it got renamed and re-nested in the process.

---

## 4. Verification has to run both directions {#verification-both-directions}

Once FLAG items are mandatory, it's tempting to treat "did every ambiguous item get its flag written" as the whole verification story. It's half of it. The other half is checking the AUTO side: for every action a subagent reported as routine, confirm after the fact that it actually stayed inside the boundary it was authorized for, not just that it got reported as if it had.

This direction is arguably the more dangerous one to skip, precisely because it's less visible. A missing flag looks incomplete — there's a gap where a human would expect an answer and doesn't see one, so it tends to get noticed. An action executed *and* reported as routine, when it actually crossed a boundary that should have required asking first, looks exactly like every other correctly-handled item in the report. Nothing about it signals "check me." The only way to catch it is to independently re-derive, after the fact, whether the boundary actually held — not to trust the report's own characterization of what it did.

Concretely: before folding a subagent's work into a final record, re-check every move it labeled routine against the same rule it was supposed to be following, using the actual before-and-after state, not the subagent's summary of the before-and-after state. If something crossed a boundary it shouldn't have, that's not a line item to quietly correct in the log — it's a finding to surface on its own, because the action has already happened and can't just be un-executed by fixing the report.

---

## 5. The rule about the rules {#precedent-confirmation}

One more edge case deserves its own explicit rule, because it's the one most likely to feel like an exception worth making: what happens when, mid-task, an agent surfaces a plausible-sounding *new* standing rule — not a one-off decision about one file, but something that would quietly become "how this is always handled" from then on, if nobody objected.

The answer has to be the same regardless of how solid the reasoning seems in the moment: a new standing rule is never adopted unilaterally, by any agent, no matter how confident its derivation. It goes through the same confirmation gate as any other judgment call — proposed, reviewed, and only written into the shared rulebook once a human has actually signed off — and only then does it become real policy that future runs can rely on. The reasoning: a one-off mistake affects one file. An unconfirmed rule that quietly becomes precedent affects every future decision that pattern-matches against it, silently, for as long as nobody notices it was never actually approved.

This sits at the same seriousness tier as the rule against permanent, unreviewed deletion — both are really about the same thing: not letting a single pass's judgment become permanent, hard-to-reverse state without a deliberate checkpoint in between.

---

## 6. Generalizing past one project {#generalizing}

None of the above is specific to managing a personal archive. The same shape applies directly to a software team putting multiple review agents around a shared codebase: a design-review agent, a security-review agent, a correctness-review agent, each commenting asynchronously on a change without waiting on each other, and one designated executor agent that actually applies changes based on what accumulates.

The part worth taking seriously if you're building that for real: wiring several agents up to comment on the same artifact is the easy part, and it's increasingly commoditized — plenty of tooling already does async multi-agent review reasonably well. The hard design question is the same one this post has been circling the whole way through: **what exactly is the executor authorized to apply on its own, versus what needs an explicit human confirmation gate first — and what independently verifies, after the fact, that the executor actually stayed inside that boundary, rather than just trusting its own account of what it did?**

That second question is the one that's easy to skip, because a system that only checks "did the reviewers leave comments" looks like it's working right up until an executor quietly acts past its actual authority and reports it as routine. Get the authority manifest explicit, get it restated at the point of every delegation instead of referenced, and get verification checking both directions — and separate agents actually start behaving like a team with real, accountable boundaries, instead of one undifferentiated authority that happens to be running in parallel.

---

## End state {#end-state}

- A named failure — a delegation paraphrase silently dropping a hard requirement — traced to its actual root cause: authority and obligation weren't explicit, so they didn't survive being handed off.
- A three-tier authority manifest (AUTO / FLAG / NEVER), restated as literal text in every delegation rather than referenced by name, closing the exact gap that caused the original failure.
- A boundary line narrow enough to be usable day to day: restructuring within an already-correct scope is routine, crossing that scope's actual boundary is a judgment call, regardless of how similar the two moves look on the surface.
- Verification checking both directions — confirming ambiguous items got flagged, *and* confirming routine-labeled actions actually stayed in bounds — since the second failure mode hides better than the first.
- A standing rule about standing rules: a new one never gets adopted mid-task on an agent's own judgment, no matter how good it sounds, until it's actually been confirmed.

The throughline across both of these posts: more agents only helps if something explicit stops them from quietly behaving like one. That something isn't a scheduler, and it isn't a chat channel between them — [both of those already existed]({% post_url 2026-08-29-recurring-review-council-async-flag-protocol %}#two-channels) before this problem showed up. It's an authority contract, stated in full at every handoff, checked in both directions afterward, and it's the same underlying idea whether the "team" in question is reviewing tax documents or reviewing a pull request.
