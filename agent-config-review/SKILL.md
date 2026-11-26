---
name: agent-config-review
description: "Use when a new model version comes out, when agent results get worse for no clear reason, or every few weeks on a repo's CLAUDE.md, AGENTS.md, rules and prompts. Removes what the code already says, old-model workarounds and contradictions, moves procedures to skills and hard rules to hooks, and keeps the file short."
---

# Agent config review

Instruction files grow by accretion and start hurting. In 2026 the Claude Code team and several Anthropic talks recommended re-auditing them at every model change: workarounds written for older models (CAPS, "think step by step", repeated warnings, rules that only mention a cost) make newer models overcautious. A study found larger AGENTS.md files did not improve task success.

## Inputs

- The repo's CLAUDE.md / AGENTS.md / `.claude/rules/` / `.github/copilot-instructions.md`, and skills if in scope.

## Steps

1. **Run the built-in audit first** if the tool has one (for example a prompt-audit command in Claude Code), then continue with the checks below.
2. **For each line, ask: would the agent find this by reading the repo?** Build commands in `package.json`, conventions visible in code, folder structure: delete. Keep what lives outside the code: decisions and their reasons, traps that bit before, environment quirks, who owns what.
3. **Remove old-model scaffolding**: ALL CAPS emphasis, "IMPORTANT/NEVER" stacks, "think hard", ritual verification steps the model now does, contradictory rules.
4. **Fix one-sided rules**: a rule that only says what to avoid gets both sides of the trade-off ("prefer X because Y; Z is fine when W").
5. **Move things to the right place**:
   - procedure used sometimes: a skill
   - rule for one folder: `.claude/rules/<area>.md` with `paths`
   - rule that must never be broken: a hook or deny rule (see correction-to-check)
6. **Keep it portable** if the team uses several tools (Claude Code, Copilot, Devin): plain markdown, one source file, others link or copy it.
7. **Measure**: line count before and after, and run one or two typical tasks to confirm nothing got worse.

## Rules

- Propose a diff; do not rewrite silently.
- Never delete a rule whose reason you do not understand. Ask.
- Target: CLAUDE.md under about 100 lines.

## Output

Before/after line count, the diff grouped by reason (redundant, outdated, moved to skill, moved to hook, rewritten), and questions for rules with unclear reasons.
