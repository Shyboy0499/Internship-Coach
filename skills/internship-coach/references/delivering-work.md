# Delivering a Task End to End

The unwritten rule of internships: when a mentor asks for X, they mean **X, finished** — understood, built, tested, shown, documented, handed over, and announced. A working function is maybe half the job. Mentors rarely say the rest out loud because, to them, it's obvious. This file is how to make it obvious to the intern too.

## Contents

1. What "done" means to a mentor
2. Decode the request
3. Questions to ask before building
4. The delivery plan
5. Definition of done, by type of work
6. Testing beyond the happy path
7. The demo
8. Getting reviewed
9. Closing the loop
10. The task brief (what to hand the intern)

---

## 1. What "done" means to a mentor

When a mentor says "Can you add X?", they're picturing the whole lifecycle:

| Stage | What it means |
|---|---|
| **Understood** | You know why it's wanted, who will use it, and what done looks like. |
| **Built** | It works, and it fits the existing patterns and conventions. |
| **Tested** | Happy path, edge cases, and failure cases — with automated tests where the team writes them. |
| **Verified for real** | Tried in realistic conditions (staging, real-sized data), not just on your laptop. |
| **Shown** | A short demo, screenshots, or a recording, so the mentor sees it work without running it. |
| **Documented** | Docs, README, comments, and a clear PR or handoff description, wherever someone would look. |
| **Reviewed and shipped** | Through the team's process: review comments resolved, merged, deployed or published. |
| **Announced and closed** | Ticket updated, mentor (and team) told, follow-ups written down. |

**Scale it to the task.** A one-line fix needs a test and a clear PR, not a demo meeting. A feature customers will touch needs all of it. Rule of thumb: the more people will see or depend on the work, the more of the list applies. When unsure, ask: "How would you like to see this when it's done?"

## 2. Decode the request

Every request has three layers:

- **Stated** — what they literally said: "Add a CSV export button to the orders page."
- **Implied** — what anyone on the team would assume: it matches the existing UI, handles big and empty reports, respects permissions, has tests, doesn't break anything.
- **Purpose** — why they want it: "Customers keep asking" or "Finance needs it for month-end." The purpose decides the trade-offs, so find it.

Rewrite the request in your own words as: **Goal · Who uses it · Done looks like · Constraints · Out of scope.**

Watch for small words that hide decisions:

- **"Quick" / "simple" / "just"** — they expect small scope. If it turns out bigger, say so early, with options.
- **"Look into" / "investigate"** — they want an answer and a recommendation, not a list of things you looked at.
- **"Clean up" / "improve"** — ask what "better" means and how they'll judge it.
- **"When you get a chance"** — still ask for a rough date and how it ranks against your other work.

**Implied requirements to check, by type of work:**

- **Code:** edge cases and invalid input, error messages, performance at real data sizes, permissions and security, backward compatibility, logging, config or feature flags, tests, docs; for UI also loading, empty, and error states, accessibility, and small screens.
- **Data analysis:** the decision it feeds, the source of truth, time range, metric definitions, sanity checks, reproducibility, confidence and caveats.
- **Design:** user flows, every state (empty, loading, error), the design system, accessibility, and a handoff engineers can build from.
- **Docs, research, reports:** audience, length, format, sources, and who reviews it before it goes out.

## 3. Questions to ask before building

Pick the few that matter, ask them **in one message**, and include your proposed answer to each so the mentor can just say "yes":

- What's this for, and who will use it?
- What does done look like — what will you check when you look at it?
- When do you need it, and how does it rank against my other work?
- Is there an existing example or pattern I should follow?
- What's out of scope for now?
- How would you like to see it — a demo, screenshots, the PR?
- Who else should review it?

```
Thanks! Quick check before I start, so I build the right thing:
- Goal: [the task in your own words, including why]
- I'm assuming [A], [B], and [C]; tell me if any of those are wrong.
- Out of scope unless you say otherwise: [X]
- Plan: rough version to show you by [day], finished and tested by [day].
```

## 4. The delivery plan

1. **Understand** — repeat the task back; read the related code, docs, or past work; find something similar to copy patterns from.
2. **Plan** — for anything bigger than a day or two, share a five-line plan and get a thumbs-up first.
3. **Build a thin slice end to end** — get the simplest version working all the way through (data to screen, query to chart) before polishing any one part.
4. **Check in early, at about 20–30%** — show the rough version: "Is this the right direction?" It's the cheapest moment to change course; finding out at 100% is the expensive way.
5. **Harden** — edge cases, tests, error handling, performance, cleanup.
6. **Verify** — run the full test suite, try it in realistic conditions, self-review your work with fresh eyes, and tick off the definition of done.
7. **Demo and review** — a short demo, a clear PR or handoff description, then address feedback.
8. **Ship and close the loop** — merge, deploy, or publish; update the ticket; tell your mentor; write down follow-ups.

**Estimating:** give a range, not a single number. Roughly double your first guess for unfamiliar work, and remember that testing, review, and polish often take 30–50% of the total — interns who budget only for "writing the code" are the ones who miss dates.

## 5. Definition of done, by type of work

Turn the relevant list into a checklist for the specific task, and leave out what doesn't apply.

**Code feature**
- [ ] Works for the main use case and the agreed edge cases
- [ ] Follows the existing patterns and style; linters pass
- [ ] Tests added or updated; the full suite passes locally and in CI
- [ ] Tried in a realistic environment (staging, real-sized data)
- [ ] Errors handled with helpful messages; nothing sensitive logged
- [ ] Docs, README, or comments updated where someone would look
- [ ] Small, self-reviewed PR with a clear description and screenshots or a short recording
- [ ] Review feedback addressed; merged; deployed or released per the team's process
- [ ] Ticket updated, mentor told, follow-ups written down

**Bug fix** — everything above, plus:
- [ ] Reproduced first, ideally as a failing test
- [ ] Root cause found, not just the symptom patched
- [ ] Checked whether the same bug exists elsewhere
- [ ] PR explains what caused it and how the fix prevents it

**Data analysis**
- [ ] Leads with the answer, then the evidence and a recommendation
- [ ] Metric definitions and time range stated
- [ ] Sanity checks done (row counts, totals match a known source, no duplicates)
- [ ] Caveats and confidence stated honestly
- [ ] Queries or notebook saved where the team can rerun them
- [ ] Charts have takeaway titles ("Sign-ups fell 18% after the pricing change"), not just labels
- [ ] Numbers double-checked by someone before they go to a wider audience

**Design**
- [ ] Every state covered: empty, loading, error, success
- [ ] Built from the design system; accessibility checked
- [ ] Clickable prototype or walkthrough
- [ ] Specs and assets ready for engineers
- [ ] Critique gathered before polishing

**Docs, research, or a report**
- [ ] Audience and purpose clear in the first paragraph
- [ ] Sources cited
- [ ] Reviewed by a peer
- [ ] Saved where people will find it, and a summary shared

## 6. Testing beyond the happy path

Run through these and note which apply — what you tested belongs in the PR and the demo:

- **Sizes:** empty, one item, many, very large
- **Input:** invalid, missing, duplicated, special characters and non-English text
- **Time:** time zones, dates at month or year boundaries, daylight-saving changes
- **People:** who should *not* be able to see or do this?
- **Failure:** network errors, timeouts, a dependency that's down
- **Compatibility:** existing data, old clients, other features that use the same code
- **Undo:** can it be rolled back or turned off if something goes wrong?

## 7. The demo

Two to five minutes:

1. **Context** — the problem, in one sentence.
2. **Show it** — the main flow, live or recorded.
3. **One edge case** — show that something hard is handled.
4. **What you tested**, and anything not done yet or known to be limited.
5. **Ask** — "Anything you'd want changed before I ship it?"

Rehearse once, have test data ready, and keep a recording or screenshots as a backup in case the live version breaks. On async or remote teams, a 60-second screen recording in the PR or team channel does the same job.

## 8. Getting reviewed

Code review, design critique, and edits on a document all work the same way: the reviewer is helping you ship something better, and how you respond is part of what they judge.

- **Make it easy to review.** Keep the change small, review it yourself first, explain what and why in the description, and point reviewers at the parts you're unsure about.
- **Respond to every comment** — a fix, a short reason you disagree, or a question. Don't leave comments silently unanswered.
- **Assume good intent.** Terse comments are usually just busy people. Never reply defensively; "Good catch, fixed" goes a long way.
- **If you disagree, explain once, briefly, with your reasoning** — then go with the reviewer's call on their team's code, or ask your mentor to settle it.
- **Ask when a comment is unclear:** "Do you mean X or Y?" beats guessing and getting it wrong twice.
- **Learn the pattern.** If the same kind of comment comes up twice, add it to your own pre-review checklist so it doesn't come up a third time.
- **Say when it's ready again** — re-request review, or post "addressed all comments" — rather than waiting for the reviewer to notice.

## 9. Closing the loop

- Update the ticket or tracker and link the PR or document.
- Message your mentor: what shipped, where it lives, how it was tested, and anything left.
- Log it in your work log or notebook — it becomes resume bullets later.
- Turn follow-ups into tickets, not mental notes.
- A week later, check it's being used and working. ("Checked the logs: 40 exports this week, no errors.") Few interns do this, and mentors notice.

## 10. The task brief (what to hand the intern)

When an intern brings a request from their mentor, turn it into this brief, tailored to their actual task, followed by a ready-to-send repeat-back message (section 3).

```
Task brief: [short name]

Goal, in my words: [one or two sentences, including why]
Who uses it: [...]
Stated requirements: [what the mentor actually said]
Unstated expectations: [the implied requirements that apply to this task]
Questions for [mentor], with my proposed answers: [3–5, only the ones that matter]
Plan and check-ins: [steps, with an early check-in at ~20–30% and dates]
Definition of done: [the checklist for this task]
Demo plan: [what to show, which edge case, what was tested]
Risks and unknowns: [what could make this take longer, and what you'll do about it]
```

Keep it proportional: for a small task, the brief is five lines and the definition of done is three checkboxes.
