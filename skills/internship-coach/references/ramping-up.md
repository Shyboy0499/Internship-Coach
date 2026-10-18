# Ramping Up: The First Weeks

How to get set up, learn a big codebase or an unfamiliar domain quickly, and fit into the team's rhythms — without leaning on your mentor for every step.

## Contents

1. What ramping up is for
2. Access and setup
3. Map the territory: people, systems, words
4. Learning a codebase
5. Learning a domain, dataset, or product
6. The team's rhythms: standups, meetings, chat, code review
7. The first small win
8. A 30-day ramp-up plan

---

## 1. What ramping up is for

Nobody expects real output in week one. The goal of the first few weeks is to become **useful and independent**: able to run things yourself, find answers without always asking, and know who owns what. Interns who invest here are quicker for the rest of the internship. Asking lots of questions is expected now — the habits that matter are writing the answers down and batching the non-urgent ones (see the mentor playbook).

## 2. Access and setup

- **Make a list of everything you need** — laptop, accounts, repositories, tools, VPN, data access, calendars, channels — and work through it on day one.
- **Flag missing access the same day.** It's a blocker you can't fix yourself, and approvals often take days.
- **Write down every setup step that wasn't in the docs** as you go. Fixing the setup guide is a perfect first contribution — it helps the next person and shows initiative.
- **Find out where to get help when something breaks** — IT helpdesk, security reporting, the team's on-call (see `when-something-breaks.md`).

## 3. Map the territory: people, systems, words

- **People:** who's on the team, what each person owns, who the experts are on each system, and who your mentor's manager is. Keep a short "who to ask about what" list.
- **Systems:** draw a rough map — the main components, how data flows between them, where your project fits. Ask your mentor to check it in a 1:1; correcting a diagram is one of the fastest ways for them to teach you.
- **Words:** keep a glossary of acronyms and team jargon. Look things up first; ask about the ones you can't find, in a batch.
- **Where things live:** docs, wikis, dashboards, tickets, design files, the team's chat channels.

## 4. Learning a codebase

Large codebases are learned by following paths through them, not by reading everything.

1. **Run it locally first.** Build it, run the tests, start the app. Everything else is easier once it runs.
2. **Trace one real request end to end** — from a button click or API call through to the database and back. Use the debugger or logging to follow it. One full path teaches more than a hundred files skimmed.
3. **Read the tests** for the area you'll work in; they show how the code is meant to behave.
4. **Use the history.** `git log` and `git blame` on the files you'll touch show why things are the way they are and who knows them best.
5. **Find the conventions:** naming, folder structure, error handling, how tests are written, the PR template, the contribution guide. Copy them.
6. **Make a tiny change and follow it all the way to production** — a docs fix or a small bug. It teaches the review, CI, and deploy process with almost no risk.
7. **Ask good orientation questions:** "Which parts are risky to touch?" "What's the history behind X?" "If you were new, which three files would you read first?"
8. **AI tools can explain unfamiliar code** — if your company's policy allows them on internal code. Check what they tell you against the code itself.

## 5. Learning a domain, dataset, or product

- **Use the product the way a customer would.** Sign up, go through the main flows, note what confuses you.
- **Read the last few reports, decks, or planning docs** your team produced — they show what matters and the vocabulary.
- **Find the metric definitions and data sources of truth** before analyzing anything. "Active user" or "revenue" often means something specific.
- **Shadow** a customer call, a support shift, or a planning meeting if you can.
- **Ask "why" about decisions,** not only "how": "Why did we build it this way?" teaches the domain faster than any doc.

## 6. The team's rhythms: standups, meetings, chat, code review

**Standup.** Keep it to about 30 seconds and make blockers impossible to miss:

```
Yesterday: [what you finished or moved forward — outcomes, not hours]
Today: [the one or two things you'll do]
Blockers: [none — or exactly what you need, and from whom]
```

"Still working on the ticket" tells the team nothing. "Got the export working for small reports; today I'm handling large ones; blocked on staging access — I've asked IT" tells them everything. Save detailed discussion for after standup.

**Meetings.** Take notes, say at least one useful thing (a question counts), and follow up afterwards on anything you didn't understand rather than staying silent. If you were given an action item, confirm it in writing.

**Chat.** Learn the team's norms: public channels for work questions (so others benefit), threads instead of new messages, a status when you're away, and the whole question in one message — never a bare "hi". Notice how fast people usually reply, and don't take a slow reply personally.

**Code review norms.** Find out how big pull requests usually are, who to ask for review, how long reviews normally take, and whether the team expects screenshots, tests, or a linked ticket. Then match it.

**Working hours.** Learn when people are online, especially across time zones, and make sure your questions land inside those hours.

## 7. The first small win

Aim to ship something small and real within your first week or two: a docs fix, a small bug, an extra test, a quick analysis someone asked for. It builds trust, teaches the end-to-end workflow, and gives you something concrete to mention in your first update. Ask your mentor: "Is there a small task I could take on this week to learn the workflow?"

## 8. A 30-day ramp-up plan

Adapt this with the intern's real role and project; share it with the mentor in the first week.

```
Week 1 — Set up and orient
[ ] Laptop, accounts, and access working (blockers flagged on day one)
[ ] Project runs locally / product used end to end / data sources found
[ ] First 1:1: success criteria, communication preferences, first milestone
[ ] Glossary, people map, and system sketch started
[ ] Small first task picked

Week 2 — First contribution
[ ] Small first task shipped through the full workflow
[ ] One request (or one metric) traced end to end
[ ] System sketch reviewed with mentor
[ ] Project plan drafted (see the task brief in delivering-work.md)

Weeks 3–4 — Real work
[ ] Project milestone 1 delivered, with an early check-in
[ ] Regular update rhythm established
[ ] First specific feedback asked for, and applied
[ ] Two or three coffee chats with people outside the immediate team
```
