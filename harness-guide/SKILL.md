---
name: harness-guide
description: "Use when setting up or reviewing an agent harness for a project or machine (CLAUDE.md/AGENTS.md, skills, subagents, hooks, permissions, MCP servers, model and effort choice, memory), when agent results are unreliable and you need to decide what to change, or when the user asks for agent best practices. Applies the practices in references/best-practices.md and produces a concrete diff."
---

# Harness guide

The harness is everything around the model: instructions, skills, subagents, hooks, permissions, tools and MCP servers, memory, and how work is verified. This skill applies a set of practices distilled from ~150 talks and videos, 25 papers and Anthropic's own writing on coding agents (Jun to Nov 2026).

Read `references/best-practices.md` before acting. For the short list of rules that should apply in every session, see `templates/global-rules.md`.

## Inputs

- Scope: one repo, a whole machine (global config), or a team setup.
- Tools in use: Claude Code, Copilot, Devin, Codex, Cursor (several at once is common).
- The current config files, if any.

## Steps

1. **Inventory** what exists: instruction files, `.claude/` (settings, hooks, rules, skills, agents), `.mcp.json` or MCP configs, `.github/skills`, `.agents/skills`, CI checks.
2. **Score it against the checklist** at the end of `references/best-practices.md`. Mark each item done, missing or not applicable.
3. **Propose changes in priority order**, strongest leverage first:
   1. a way for the agent to verify its work (verify-work skill, feature map, test commands)
   2. hard rules as hooks and deny rules, not prose (verification-hooks skill)
   3. a short instruction file with only what the code does not say (agent-config-review skill)
   4. skills for repeated procedures; subagents only where clean context, parallelism or a cheaper model helps
   5. MCP servers only where they add something a CLI cannot, with pinned versions and least privilege
4. **Show the diff** and wait for approval before touching shared config.
5. **Verify**: run one typical task with the new setup and report what changed.

## Rules

- Do not add a rule, tool or MCP server without a reason tied to a failure or a measured need.
- Prefer portable formats (plain markdown, the open SKILL.md standard) when more than one tool is in use.
- Never put secrets in any config file; reference them by environment variable name.

## Output

Checklist score, prioritized change list with reasons, the diff, and the result of the verification run.
