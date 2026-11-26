# skills

A collection of reusable [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) for Claude, built from real workflows and versioned here.

## Skills

| Skill | What it does |
|---|---|
| [`resume-for-job`](resume-for-job/SKILL.md) | Picks which of your resume versions to send for a job posting, suggests safe tailoring, and flags gaps. Works from an audited fact inventory so nothing gets exaggerated. |
| [`sql-queries`](sql-queries/SKILL.md) | Two-stage T-SQL helper for SQL Server: agrees on what to fetch before writing any SQL, handles JSON columns, and wraps every UPDATE in a reviewable transaction. Includes a setup guide for schema files and JSON examples. |
| [`service-flow-map`](service-flow-map/SKILL.md) | Maps a microservice system into versioned JSON and an interactive visual that animates a data flow from a UI click to the last database write. Orchestrator plus sub-agents, script-first to save tokens. |

### Agentic coding workflow

Built from a review of ~150 talks and videos, 25 papers and Anthropic's own writing on coding agents (Jun to Nov 2026). The common thread: generating code is cheap; what matters is that the agent proves its work and that every correction becomes an automatic check.

| Skill | What it does |
|---|---|
| [`verify-work`](verify-work/SKILL.md) | Runs the real system and checks every acceptance criterion, including what must not change, returning an evidence table. No evidence, no "done". |
| [`correction-to-check`](correction-to-check/SKILL.md) | Turns each correction you give an agent into the strongest enforceable form (type, lint/analyzer, architecture test, hook, deny rule) instead of another CLAUDE.md line, and logs it. |
| [`spec-interview`](spec-interview/SKILL.md) | The agent interviews you with multiple-choice questions until it can write a short SPEC.md with testable acceptance criteria. Fits SDD and BMAD flows. |
| [`skeptical-reviewer`](skeptical-reviewer/SKILL.md) | Independent review passes in clean contexts, keeps only findings that survive, flags human-only zones. Prepares a PR for human review; never approves. |
| [`version-upgrade`](version-upgrade/SKILL.md) | Runtime, framework and dependency upgrades (.NET, Angular, Node, packages): official breaking changes first, reviewable steps, differential checks against a frozen baseline, lessons file. |
| [`legacy-spec-extraction`](legacy-spec-extraction/SKILL.md) | Extracts a language-agnostic functional spec from existing code, with file:line per rule and the implicit behavior agents usually miss. |
| [`legacy-test-backfill`](legacy-test-backfill/SKILL.md) | Characterization and property tests for legacy code, with an anti-cheat checklist so tests can't pass by touching production code or weakening asserts. |
| [`api-change-impact`](api-change-impact/SKILL.md) | Finds every consumer of an endpoint, DTO or event across repos and classifies a change as safe, risky or breaking, with a rollout plan. |
| [`explain-in-html`](explain-in-html/SKILL.md) | One self-contained HTML page explaining one module or flow: diagram, annotated excerpts, gotchas. |
| [`verification-hooks`](verification-hooks/SKILL.md) | Claude Code hooks and deny rules for .NET and Node/Angular repos. Hooks exit with code 2 so the agent has to fix problems. Templates included and tested. |
| [`quality-ratchet`](quality-ratchet/SKILL.md) | CI gate where no PR may make a metric worse (coverage, warnings, file size...). The baseline only moves toward better. Script included. |
| [`pr-babysit`](pr-babysit/SKILL.md) | Watches a PR until CI is green and every review thread is answered, escalating design decisions to a human. |
| [`friction-log`](friction-log/SKILL.md) | The agent logs what slowed it down; a weekly triage turns repeated friction into docs, scripts, checks or skills. |
| [`agent-config-review`](agent-config-review/SKILL.md) | Re-audits CLAUDE.md / AGENTS.md at each model change: removes what the code says, old-model workarounds and contradictions. |
| [`agent-instructions-audit`](agent-instructions-audit/SKILL.md) | Security check of a third-party repo, skill, plugin or MCP config for instructions aimed at agents (prompt injection, exfiltration, persistence). |
| [`skill-audit`](skill-audit/SKILL.md) | Lints skills (trigger, size, portability, secrets) with a bundled script, plus optional with/without tests to cut what the model already knows. |

## Agents

Subagents for Claude Code, in [`agents/`](agents/). Use them when a task needs a clean context, parallel runs or a cheaper model. Copy to `~/.claude/agents/` or a repo's `.claude/agents/`.

| Agent | What it does |
|---|---|
| [`skeptical-reviewer`](agents/skeptical-reviewer.md) | Read-only reviewer for one focused pass (correctness, security, blast radius). Used by the skeptical-reviewer skill. |
| [`verifier`](agents/verifier.md) | Checks a finished change against its criteria by running the system, without the implementer's context. Reports, never fixes. |
| [`code-explorer`](agents/code-explorer.md) | Answers "where / how / who calls" in large codebases on a cheaper model, returning conclusions with file:line instead of dumps. |
| [`git-archaeologist`](agents/git-archaeologist.md) | Reads git history (blame, reverts, linked PRs) to explain why code is the way it is before you change it. |

## Structure

Each skill is a folder with a `SKILL.md` (YAML frontmatter with `name` and `description`, followed by instructions), plus optional scripts or reference files:

```
skill-name/
  SKILL.md
  scripts/      (optional)
  references/   (optional)
  templates/    (optional)
```

Check skills before committing: `python3 skill-audit/scripts/lint_skills.py .`

Start a new one by copying [`_template`](_template/SKILL.md).

## Using these skills

- **Claude Code:** copy or symlink a skill folder into `~/.claude/skills/<skill-name>/`
- **Claude.ai:** zip the skill folder and upload it in your skills settings
- **Other agents (Copilot, Devin, Codex):** the SKILL.md files are plain markdown; point the tool's instructions file at the ones you need

## License

MIT
