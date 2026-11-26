---
name: correction-to-check
description: "Use whenever the user corrects an agent's output, repeats a review comment, or says 'don't do X again'. Turns the correction into the strongest enforceable mechanism (lint rule, analyzer, architecture test, hook, deny rule) instead of another line in CLAUDE.md, and logs it so repeated mistakes can be mined later."
---

# Correction to check

Every correction is a missing rule. Text rules in CLAUDE.md or AGENTS.md are soft and get forgotten; checks that fail the build do not. This skill decides where a correction should live and writes it there.

Based on: Lauren Tan (SpaceXAI, "All Code Is Slop (Except Mine)"), Anthropic's Rust migration post, Tessl and LinkedIn talks (AI Engineer 2026), and the Claude Code team's advice to never fix a mistake only in the chat.

## Inputs

- The correction: what the agent did, what it should have done, and where (files, PR comment, chat).
- The repo's tooling: linters, analyzers, test framework, CI, `.claude/settings.json` hooks.

## Steps

1. **Restate the correction as a rule** in one sentence, with an example of wrong and right.
2. **Pick the strongest place it can live**, top to bottom, and stop at the first that works:

   | Level | Use when | Examples |
   |---|---|---|
   | Type / compiler | The wrong state can be made unrepresentable | value object instead of `decimal`, enum instead of string, `required` |
   | Lint / analyzer rule | A pattern in code can be detected | ESLint custom rule, Roslyn analyzer, `.editorconfig` severity, banned API list |
   | Architecture test | It is about layers or dependencies | NetArchTest / ArchUnitNET, dependency-cruiser |
   | Unit / contract test | It is about behavior | test that fails on the old behavior |
   | Hook | It is about what the agent does (commands, files) | PreToolUse hook that blocks, exit code 2 |
   | Deny rule / permission | It must never happen | deny `git push origin main`, deny reading `.env` |
   | CLAUDE.md / skill line | Judgment that no tool can check | "prefer X when Y" with the reason |

3. **Write it.** Produce the actual rule, test or hook, not a description. Run it once against the current code to show it catches the bad case and passes the good one.
4. **Log it.** Append one line to `docs/agent-corrections.md`:
   `YYYY-MM-DD | <rule> | <level chosen> | <file of the check> | <source: chat/PR#>`
5. **Look for repeats.** If the log has 2 or more entries with the same theme, propose consolidating them into one stronger check.

## Rules

- Prefer a check over text every time a tool can detect the problem.
- A hook that should make the agent fix something must exit with code **2** (blocks and sends stderr back to the agent). Exit 1 only warns and the task still counts as done.
- When a text rule is the only option, include the reason and both sides of the trade-off. Rules that only say "never" or only mention a cost make newer models overly cautious.
- Do not add a rule that duplicates what the code or an existing check already says.
- Show the diff and wait for approval before changing shared config (CI, analyzers, settings).

## Output

1. The rule in one sentence.
2. Level chosen and why the stronger ones did not fit.
3. The diff.
4. Proof it works: command and output on a bad and a good example.
5. The log line added.
