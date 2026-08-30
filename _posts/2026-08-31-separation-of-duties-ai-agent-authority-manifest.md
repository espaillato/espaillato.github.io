---
layout: post
title: "Separation of Duties: Making Parallel Agents Behave Like a Team"
date: 2026-08-31
---

[The previous post]({% post_url 2026-08-29-recurring-review-council-async-flag-protocol %}) split one generalist sweep into several narrower agents, each with its own scope, talking to each other through a shared inline-flag protocol. That solved coordination: agents could leave each other messages across a scheduling gap without me relaying them. It didn't solve the problem underneath. Running several agents in parallel is not the same as having several accountable specialists. Without something more explicit, they collapse back into one authority that happens to run in more than one process.

This post is about the failure that made that obvious, and the authority model I built to fix it. The pattern isn't specific to a document archive, so it's written to lift and adapt.

- [The bug that exposed it](#the-bug)
- [What makes it a team](#what-makes-a-team)
- [A concrete authority model: AUTO / FLAG / NEVER](#auto-flag-never)
- [Where the boundary line goes](#the-boundary-line)
- [Verification has to run both directions](#verification-both-directions)
- [The rule about the rules](#precedent-confirmation)
- [Generalizing past one project](#generalizing)
- [End state](#end-state)

---

## 0. The bug that exposed it {#the-bug}

A large sweep had more to cover than fit in one pass, so the work got split across several parallel subagents. Each one got a slice of the checklist and a short instruction: apply the rules, report back. One rule mattered more than the others. Certain findings couldn't just sit in a report; they also had to be written as a standing marker at the spot they applied to, so the next run — or I — would see them without digging through old chat logs.

That rule was clear in the source instructions. It didn't survive the handoff. Each subagent was told, in effect, "list the findings you'd flag for a human in your report." Reasonable-sounding, and it dropped the second half of the rule: also write the marker. The subagents did good work otherwise and the reports were accurate. The markers just never got written, because the instruction that would have produced them got summarized away between the rulebook and the delegation.

Nobody chose to skip the step. It fell through a summarization gap that nothing was checking.

---

## 1. What makes it a team {#what-makes-a-team}

The easy reading of that bug is that the subagents slipped up. The more useful reading is that the setup never divided responsibility in the first place. It divided labor. Three processes ran instead of one, but the authority over what each could do and had to do was still a single blob, re-derived and re-summarized on every handoff.

That's the distinction that matters: parallelism makes copies of one undivided authority. It doesn't split responsibility. A team needs each class of decision to have an owner, needs a delegated task to carry its obligations with it, and needs a finding to be cleared by its owner rather than by whoever reaches it first. Without that, five agents instead of one is five shots at the same mistake, not five narrower areas of accountability.

The fix is unglamorous: the full obligation travels with the delegation, word for word, every time. Not a summary, not a paraphrase, not a pointer to a document. "Follow the rules in the shared doc" is not the same as restating the rule in the subagent's instructions. The first survives summarization badly. The second has nowhere to lose the requirement, because the rule and the instruction are the same text.

---

## 2. A concrete authority model: AUTO / FLAG / NEVER {#auto-flag-never}

The fix is a three-tier authority manifest, written out in full at the top of every delegation instead of referenced by name.

**AUTO — do it without asking, then report what you did.** For mechanical actions only: no judgment, no ambiguity, same input always gives the same right output. Formatting fixes, applying a documented convention, moving something within a boundary that was never in doubt.

**FLAG — stop, write the question at the spot it applies to, and do nothing else until it's answered.** For anything that needs judgment: a classification that could go more than one way, a change that alters what something appears to mean, anything that would require a new standing rule. Writing the flag is the action. There's no version of this tier where the agent also does the thing "just in case," however confident it is.

**NEVER — a short, absolute list, no exceptions no matter how good the reasoning sounds at the time.** This tier exists to survive a persuasive edge case. Keep it short enough to memorize and specific enough that applying it needs no judgment.

The part that fixes the bug: every subagent dispatch restates this manifest — the specific AUTO/FLAG line for that task — as literal text in its own instructions, not a citation. Pointing an agent at a shared document by name is the exact thing that failed once already. The fix isn't to trust the reference more. It's to not depend on a reference surviving summarization at all.

---

## 3. Where the boundary line goes {#the-boundary-line}

An authority model is only as good as where it draws its lines, and the first version drew this one too conservatively to live with. The original rule was blunt: anything already in its intended place needed a confirmation before it moved, anywhere. Safe, but it meant routine reorganizing — splitting a folder into subfolders, renaming a folder once its contents outgrew the name — raised as many questions as a genuinely ambiguous reclassification. Ask about everything and the answers turn into rubber stamps, which defeats the point of asking.

The fix was a narrower line that's still safe. Restructuring within a top-level category that's already correct is AUTO; a subfolder split or a rename doesn't change what category something belongs to. Moving something across a top-level boundary is FLAG; that's a reclassification, not a tidy-up, however good the new spot looks. Both are "moving a file," but they answer different questions, and only one needs me in the loop.

The test isn't "did something move." It's "after this move, is it a fundamentally different category of thing." A rename that changes apparent ownership or purpose is a reclassification even if the file never leaves its folder. A restructure that stays inside the same top-level category isn't, even if every file in it got renamed and re-nested.

---

## 4. Verification has to run both directions {#verification-both-directions}

Once FLAG items are required, it's easy to treat "did every ambiguous item get a flag" as the whole verification job. It's half. The other half is the AUTO side: for every action a subagent called routine, check afterward that it actually stayed inside its authorized boundary, not just that the report said so.

Skipping this half is the more dangerous choice, because the failure is invisible. A missing flag looks incomplete — there's a gap where an answer should be, and someone notices. An action that was carried out and reported as routine, but actually crossed a line that needed a confirmation, looks like every other handled item in the report. Nothing about it says "check me." The only way to catch it is to re-derive, independently, whether the boundary held — not to take the report's word for it.

In practice: before folding a subagent's work into the record, re-check every move it labeled routine against the rule it was following, using the real before-and-after state rather than the subagent's summary of it. If something crossed a line it shouldn't have, that's not a quiet fix in the log. It's a finding on its own, because the action already happened and editing the report doesn't undo it.

---

## 5. The rule about the rules {#precedent-confirmation}

One more case needs its own rule, because it's the one most likely to feel like a fair exception: mid-task, an agent proposes a plausible new standing rule — not a decision about one file, but something that would become "how we always do this" if nobody pushed back.

The answer is the same however solid the reasoning looks: no agent adopts a new standing rule on its own. It goes through the same gate as any other judgment call — proposed, reviewed, written into the rulebook only after a human has signed off — and only then do future runs rely on it. A one-off mistake affects one file. An unapproved rule that becomes precedent affects every future decision that matches it, for as long as it takes someone to notice it was never approved.

This sits at the same level as the rule against permanent deletion without review. Both are about the same thing: not letting one pass's judgment turn into permanent, hard-to-reverse state without a checkpoint.

---

## 6. Generalizing past one project {#generalizing}

None of this is specific to a document archive. The same shape fits a software team putting several review agents around a shared codebase: a design reviewer, a security reviewer, a correctness reviewer, each commenting on a change without waiting on the others, plus one executor agent that applies changes based on what comes back.

Wiring several agents to comment on the same artifact is the easy part, and the tooling for it is getting commoditized; plenty of it does async multi-agent review well enough. The hard question is the one this post keeps circling: what is the executor allowed to apply on its own, what needs a human confirmation first, and what checks afterward — independently — that the executor stayed inside that line rather than trusting its own account of what it did?

That last part is easy to skip. A system that only checks "did the reviewers comment" looks fine right up until an executor acts past its authority and files it as routine. Make the authority manifest explicit, restate it at every delegation instead of linking to it, and verify in both directions. Then the agents start behaving like a team with real boundaries instead of one authority running in parallel.

---

## End state {#end-state}

- A specific failure — a paraphrased delegation dropping a hard requirement — traced back to its cause: authority and obligation weren't written down, so they didn't survive the handoff.
- A three-tier authority manifest (AUTO / FLAG / NEVER), restated in full at every delegation instead of referenced by name, closing the gap that caused the failure.
- A boundary narrow enough to live with: restructuring inside a correct scope is routine, crossing the scope boundary is a judgment call, however similar the two moves look.
- Verification in both directions — that ambiguous items got flagged, and that routine-labeled actions stayed in bounds — since the second failure hides better than the first.
- A rule about rules: no new standing rule gets adopted mid-task on an agent's judgment until a human has confirmed it.

The throughline across both posts: more agents only helps if something explicit keeps them from acting like one. That something isn't a scheduler, and it isn't a chat channel — [both of those already existed]({% post_url 2026-08-29-recurring-review-council-async-flag-protocol %}#two-channels) before this problem showed up. It's an authority contract, stated in full at every handoff and checked both ways afterward, and the idea is the same whether the team is reviewing tax documents or a pull request.
