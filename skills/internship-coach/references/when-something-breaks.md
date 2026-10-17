# When Something Breaks: Who to Tell, and How

Breaking something is a normal part of an internship. What matters is the next hour: who you tell, how fast, and what you avoid doing. The mentor isn't always the first call — security problems go to IT or security within minutes, broken equipment goes to the IT helpdesk, and broken team systems go to the mentor or the team's on-call.

## Contents

1. The first ten minutes
2. Who to contact first
3. Security incidents: report first, fix second
4. Broken or lost equipment
5. Shared or live systems
6. Data mistakes
7. Writing to IT or the helpdesk
8. Telling your mentor
9. Afterwards
10. Find these contacts in week one

---

## 1. The first ten minutes

1. **Stop making it worse.** Stop the script, don't re-run it, don't keep clicking. No frantic fixes on shared or live systems.
2. **Keep the evidence.** Screenshot error messages, keep the suspicious email, note the time.
3. **Work out what kind of problem it is** — the table below decides who you contact first.
4. **Tell the right people quickly** — within minutes for anything security-related, within the hour for everything else.
5. **Then fix it, with their go-ahead.**

Hiding a problem or quietly trying to fix it alone is the one move that turns an ordinary intern mistake into a serious one. IT and security teams handle these every day; an early, honest report is the most useful thing an intern can give them.

## 2. Who to contact first

| What happened | Contact first | Then | Why |
|---|---|---|---|
| Clicked a suspicious link, typed a password into a fake login page, opened a strange attachment | **IT security or the helpdesk** — use the official phishing-report button or security address | Mentor | Minutes matter: they can reset accounts and block the attacker before it spreads. |
| Leaked a password, API key, or token (pasted in chat, committed to git, shared publicly) | **Security and the owner of that system**, plus your mentor — all immediately | — | The secret has to be revoked and replaced; deleting the message or commit isn't enough. |
| Lost or stolen laptop, phone, or badge | **IT helpdesk or security** (building security for badges) | Mentor | They can lock or wipe the device remotely — but only if they know quickly. |
| Laptop broken, won't start, liquid spill, other hardware damage | **IT helpdesk** (open a ticket, or call if you're blocked) | Mentor, especially if a deadline or meeting is affected | IT repairs or swaps hardware; your mentor needs your plan. |
| Locked out, access missing, VPN or software not working | **IT helpdesk** | Mentor only if it's blocking your work | Access problems are IT's job; don't burn hours on them. |
| Broke something in a shared or live system (a deployment, database, website, shared dashboard) | **Mentor** — or the team's **on-call or incident channel** if your mentor doesn't answer within minutes | Follow the team's incident process | The team owns the system and knows how to roll it back; the IT helpdesk usually doesn't run team systems. |
| Deleted or corrupted shared files or data | **Mentor and the owner of the data** | IT, if a restore from backup is needed | Version history or backups often fix it, as long as nobody piles more changes on top first. |
| Customer or personal data sent to the wrong place, or anything that might be a privacy breach | **Mentor and the privacy or security team** — right away | — | Many organizations have legal deadlines for reporting data breaches. |
| Physical safety: injury, fire, electrical, lab hazard | **Emergency services or site safety** | Mentor, facilities | People before work, always. |

**Names vary:** IT, ICT, service desk, helpdesk, tech support, InfoSec, security operations; engineering teams often have an "on-call" person or an incident channel. If you're unsure who owns the problem, tell your mentor and ask, "Who should I report this to?" For anything that *might* be security-related, report it to IT or security even if you're not sure — they would much rather get a false alarm than a late report.

## 3. Security incidents: report first, fix second

- **Report immediately**, even if it seems minor or embarrassing, and even if your mentor is away. Use the official channel (a "report phishing" button, the security email, or the helpdesk phone) — never a reply to the suspicious message.
- **Don't investigate on your own.** Don't click the link again "to check" or forward the attachment to colleagues.
- **Follow IT's instructions:** usually change your password from a known-safe device, and sometimes disconnect from the network. Don't wipe or reset the device unless they tell you to — that destroys the evidence they need.
- **Leaked secrets** (passwords, keys, tokens) must be revoked and replaced by whoever owns them. Deleting the commit or message doesn't help: the history and copies remain.
- **Then tell your mentor** what happened and that IT or security already has it.

## 4. Broken or lost equipment

- **Open an IT ticket right away**, or call if you can't work at all.
- **Tell your mentor if it affects a deadline or meeting**, with your plan: a loaner laptop, another machine, or moving the demo.
- **Check what wasn't backed up** — and make pushing code and syncing files a daily habit, before it matters.
- **Lost or stolen device:** report it at once. Remote locking only helps if it happens quickly, so don't wait to see whether it turns up.

## 5. Shared or live systems

- **Stop.** Don't try more fixes on a live system on your own.
- **Tell your mentor immediately.** If they don't respond within minutes and users are affected, use the team's incident or on-call channel.
- **Say exactly what you did and when**, what you're seeing now, and anything you've touched since.
- **Let the owner decide** on rollback or repair. Offer to help, and write down the timeline while it's fresh.
- Many teams hold a **blameless review** ("post-mortem") afterwards. It's about improving the process, not punishing you — contribute honestly.

## 6. Data mistakes

- **Stop editing**, and note the time.
- **Look for version history, trash, or backups** — but on anything shared, ask before restoring, because a restore can wipe out other people's changes.
- **Tell your mentor and the data's owner.**
- **If customer or personal data was exposed,** treat it as a privacy incident: report it to your mentor and the security or privacy team straight away.

## 7. Writing to IT or the helpdesk

```
Subject: [Urgent / blocking] [one-line summary]

What happened: [plain description]
When: [time and time zone]
Device / account: [laptop model or asset tag, your username — never your password]
What I've done so far: [e.g. disconnected from Wi-Fi, changed my password]
Impact: [e.g. can't work at all; demo at 2pm; possible security issue]
How to reach me: [phone or chat]. My mentor is [name].
```

Attach screenshots of error messages, keep the ticket number, and never put a password in a ticket.

## 8. Telling your mentor

Use the "Owning a mistake" template in `templates.md`, and add who you've already contacted:

```
Heads-up: [what happened]. I've already reported it to [IT / security / on-call] (ticket [number]) and [what you've done so far].
Impact: [what's affected and for how long, as far as I know].
Next: [what happens now, and what you'll do to prevent it].
Is there anything else you'd like me to do?
```

## 9. Afterwards

- Do whatever IT or security asks, promptly.
- Write down what you'll do differently — test environments, backups, checking links before clicking.
- Close the loop: tell your mentor when it's resolved, and log it in your notebook if you keep one.

## 10. Find these contacts in week one

Before anything breaks, find out:

- how to reach the **IT helpdesk** (portal, chat, phone)
- how to **report phishing or a security issue**
- your team's **on-call person or incident channel**
- who **owns the systems and data** you work with

Write them in your notes or internship notebook, so you're not searching for them in a panic.
