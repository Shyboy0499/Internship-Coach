# Internship Coach

**An [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that turns Claude into your internship coach** — get ready for day one, work with your mentor without frustrating them, and finish with a return offer.

[![GitHub stars](https://img.shields.io/github/stars/Shyboy0499/Internship-Coach?style=social)](https://github.com/Shyboy0499/Internship-Coach/stargazers)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Interns aren't expected to know everything — that's the point of an internship. What wears mentors down is a handful of habits: going quiet when stuck, asking questions with no context, asking the same thing twice, hiding mistakes. Internship Coach helps Claude spot those habits as they happen and coach the better one, and it always hands the intern something concrete: a plan, a checklist, or a message ready to send. With your OK, it also keeps a short notebook, so it remembers your goals, your mentor's preferences, and your progress from week to week.

It works in Claude Code, the Claude apps, and the Agent SDK, as well as other agents that read Agent Skills.

## What it helps with

- **Meeting and exceeding expectations** — what every intern is expected to do, a "meets vs. stands out" self-check, and extra skills beyond the job description that make an intern stand out.
- **Preparing** — what to brush up on before day one, by role (software, data, ML, product, design, marketing, finance, hardware, research, and more).
- **Working with a mentor** — when and how to ask questions, getting unstuck, status updates, 1:1s, taking feedback, owning mistakes, handling too much or too little work, and making a remote internship work. Claude also spots common intern patterns (the silent struggler, the over-apologizer, the private perfectionist) and coaches the habit behind them.
- **Keeping track** — with your OK, Claude keeps a short internship notebook (goals, how your mentor likes to communicate, feedback, a work log) so it remembers between conversations, plus a weekly check-in that writes your work-log entry and your update to your mentor.
- **Drafting messages** — help requests, status updates, 1:1 agendas, delay warnings, apologies, feedback asks, PR descriptions.
- **Finishing strong** — midpoint self-review, final presentation, handoff doc, return-offer conversation, thank-yous, and turning the internship into resume bullets and interview stories.
- **Knowing when it isn't about pleasing the mentor** — harassment, unsafe or unethical requests, or unfair treatment get routed to the right people instead.

### Example prompts

- "I start my data science internship in 3 weeks. What should I learn first?"
- "I've been stuck on a bug for two days and I already asked my mentor once. What do I do?"
- "Help me write a message telling my manager I'm going to miss Friday's deadline."
- "My midpoint review is next week — can you help me write a self-review?"
- "What do interns who get return offers do differently? I want to stand out."
- "It's Friday — let's do my weekly check-in."
- "My internship just ended. Turn what I did into resume bullets."

## Install

### Claude desktop app (as a plugin)

Click **+** next to the chat box, choose **Add plugins…**, pick **Add marketplace from GitHub**, enter `Shyboy0499/Internship-Coach`, then install **internship-coach**.

### Claude Code (as a plugin)

```
/plugin marketplace add Shyboy0499/Internship-Coach
/plugin install internship-coach@internship-coach
```

### Any agent, with the skills CLI

Installs into Claude Code and other agents that read Agent Skills (such as Cursor and Codex):

```
npx skills add Shyboy0499/Internship-Coach
```

### Claude Code (as a plain skill folder)

Copy `skills/internship-coach` into `~/.claude/skills/` (just for you) or into `.claude/skills/` inside a project (for everyone working on that project).

### Claude apps (claude.ai, desktop, mobile)

Zip the skill folder:

```
cd skills && zip -r internship-coach.zip internship-coach
```

Then upload the zip in Claude's settings — see [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude) for the current steps. Code execution needs to be enabled for skills to work.

### Claude Agent SDK

Put the folder at `.claude/skills/internship-coach/` in your project, load project settings, and allow the `Skill` tool:

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    setting_sources=["project"],
    allowed_tools=["Skill", "Read"],
)
```

## Testing

The `evals/` folder holds test cases for Claude Code's built-in eval runner. Each case is a realistic intern request with checks on the answer, and the runner compares answers with and without the skill:

```
claude plugin eval .
```

Add `--model haiku` (or `sonnet`, `opus`) to check the skill works across models. The answers are graded by another model; `--judge-model sonnet` grades more reliably than the default.

## Repository layout

```
.github/
  workflows/star-history.yml  # redraws the star chart daily and on each new star
  scripts/star_history.py     # draws the chart from the repo's creation to today
.claude-plugin/
  plugin.json             # Claude Code plugin manifest
  marketplace.json        # lets this repo be added as a plugin marketplace
skills/
  internship-coach/
    SKILL.md              # entry point: when to use it and how to coach
    references/
      mentor-playbook.md  # working with a mentor, situation by situation
      templates.md        # ready-to-adapt messages and documents
      expectations.md     # what's expected of interns and how to stand out
      role-skills.md      # what to prepare and stand-out extras, by field
      timeline.md         # what to do before day one through the last week
      notebook.md         # the internship notebook and the weekly check-in
    LICENSE.txt           # license copy that travels with the skill folder
evals/                    # test cases for `claude plugin eval`
LICENSE
```

`SKILL.md` stays short and is loaded whenever the skill triggers. Claude reads the reference files only when a request needs them.

## Star History

<a href="https://github.com/Shyboy0499/Internship-Coach/stargazers">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Shyboy0499/Internship-Coach/star-history/star-history-dark.svg" />
   <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Shyboy0499/Internship-Coach/star-history/star-history-light.svg" />
   <img alt="Star history of Shyboy0499/Internship-Coach since December 2025" src="https://raw.githubusercontent.com/Shyboy0499/Internship-Coach/star-history/star-history-light.svg" />
 </picture>
</a>

The chart covers the repo's whole life, starting December 2025. A GitHub Action redraws it every day and whenever someone stars the repo.

<sub>Chart style adapted from [star-history.com](https://star-history.com) (MIT). Font: [xkcd Script](https://github.com/ipython/xkcd-font) by the ipython/xkcd-font contributors ([CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/)).</sub>

## License

[MIT](LICENSE) — free to use, share, and adapt.
