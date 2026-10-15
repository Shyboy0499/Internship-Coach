# Internship Coach

An [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that helps interns succeed: prepare the right skills for their role, work with their mentor without frustrating them, and finish strong.

Mentors rarely get upset because an intern doesn't know something — interns aren't supposed to. They get frustrated by habits like going silent when stuck, asking questions with no context, repeating questions, or hiding mistakes. This skill teaches Claude to coach interns out of those habits and to hand them concrete help: plans, checklists, and messages ready to send.

## What it helps with

- **Meeting and exceeding expectations** — what every intern is expected to do, a "meets vs. stands out" self-check, and extra skills beyond the job description that make an intern stand out.
- **Preparing** — what to brush up on before day one, by role (software, data, ML, product, design, marketing, finance, hardware, research, and more).
- **Working with a mentor** — when and how to ask questions, getting unstuck, status updates, 1:1s, taking feedback, owning mistakes, handling too much or too little work.
- **Drafting messages** — help requests, status updates, 1:1 agendas, delay warnings, apologies, feedback asks, PR descriptions.
- **Finishing strong** — midpoint self-review, final presentation, handoff doc, return-offer conversation, thank-yous.
- **Knowing when it isn't about pleasing the mentor** — harassment, unsafe or unethical requests, or unfair treatment get routed to the right people instead.

### Example prompts

- "I start my data science internship in 3 weeks. What should I learn first?"
- "I've been stuck on a bug for two days and I already asked my mentor once. What do I do?"
- "Help me write a message telling my manager I'm going to miss Friday's deadline."
- "My midpoint review is next week — can you help me write a self-review?"
- "What do interns who get return offers do differently? I want to stand out."

## Install

### Claude Code (as a plugin)

```
/plugin marketplace add Shyboy0499/internship-coach
/plugin install internship-coach@internship-coach
```

### Claude Code (as a plain skill folder)

Copy `skills/internship-coach` into `~/.claude/skills/` (just for you) or into `.claude/skills/` inside a project (for everyone working on that project).

### Claude apps (claude.ai, desktop, mobile)

Zip the skill folder:

```
cd skills && zip -r internship-coach.zip internship-coach
```

Then in Claude, open **Settings → Capabilities**, find **Skills**, and upload the zip. Code execution needs to be enabled for skills to work.

### Claude Agent SDK

Put the folder at `.claude/skills/internship-coach/` in your project, load project settings, and allow the `Skill` tool:

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    setting_sources=["project"],
    allowed_tools=["Skill", "Read"],
)
```

## Repository layout

```
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
```

`SKILL.md` stays short and is loaded whenever the skill triggers. Claude reads the reference files only when a request needs them.
