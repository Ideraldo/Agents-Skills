# skills

A collection of reusable [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) for Claude, built from real workflows and versioned here.

## Skills

| Skill | What it does |
|---|---|
| _coming soon_ | |

## Structure

Each skill is a folder with a `SKILL.md` (YAML frontmatter with `name` and `description`, followed by instructions), plus optional scripts or reference files:

```
skill-name/
  SKILL.md
  scripts/      (optional)
  references/   (optional)
```

Start a new one by copying [`_template`](_template/SKILL.md).

## Using these skills

- **Claude Code:** copy or symlink a skill folder into `~/.claude/skills/<skill-name>/`
- **Claude.ai:** zip the skill folder and upload it in your skills settings

## License

MIT
