# skills

A collection of reusable [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) for Claude, built from real workflows and versioned here.

## Skills

| Skill | What it does |
|---|---|
| [`resume-for-job`](resume-for-job/SKILL.md) | Picks which of your resume versions to send for a job posting, suggests safe tailoring, and flags gaps. Works from an audited fact inventory so nothing gets exaggerated. |
| [`sql-queries`](sql-queries/SKILL.md) | Two-stage T-SQL helper for SQL Server: agrees on what to fetch before writing any SQL, handles JSON columns, and wraps every UPDATE in a reviewable transaction. Includes a setup guide for schema files and JSON examples. |
| [`service-flow-map`](service-flow-map/SKILL.md) | Maps a microservice system into versioned JSON and an interactive visual that animates a data flow from a UI click to the last database write. Orchestrator plus sub-agents, script-first to save tokens. |

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
