---
name: verification-hooks
description: "Use when setting up Claude Code hooks and permissions for a repo, when the agent keeps finishing with broken lint or tests, or when the user wants guardrails against destructive commands. Generates hooks that block with exit code 2 so the agent fixes problems itself, plus a baseline deny list, for .NET and Node/Angular projects."
---

# Verification hooks

Hooks turn "please run the tests" into something the agent cannot skip. The key detail, from Lydia Hallie's 2026 Claude Code best-practices talk: a hook must exit with code **2** to block and send its message back to Claude so it fixes the issue. Exit code 1 is treated as a non-blocking error and the task can still finish.

## Inputs

- Repo stack: .NET (dotnet CLI), Node/Angular (npm/pnpm), or both.
- What should be checked and when: format after edits, tests before finishing, block dangerous commands.

## Steps

1. **Pick the hooks** (templates in `templates/`):
   - `PostToolUse` on Edit/Write: format and lint only the changed file (`dotnet format --include`, `eslint --fix`). Fast, runs often.
   - `Stop`: run the tests for the touched area before the agent is allowed to finish. Exit 2 with the failing output if red.
   - `PreToolUse` on Bash: block destructive or out-of-scope commands (push to main, `rm -rf` outside the repo, production profiles, reading `.env`).
2. **Copy the scripts** to `.claude/hooks/` and merge `templates/settings.json` into `.claude/settings.json`. Make scripts executable.
3. **Add deny rules** in `permissions.deny` for anything irreversible. Deny rules are checked before any auto-approval, so they hold even in permissive modes.
4. **Test each hook**: trigger it on purpose (introduce a lint error, a failing test, a blocked command) and confirm the agent receives the message and the action is blocked.
5. **Commit `.claude/settings.json` and `.claude/hooks/`** so the whole team gets them. Personal tweaks go in `.claude/settings.local.json` (not committed).

## Rules

- Keep hooks fast: PostToolUse under a few seconds, scoped to changed files. Slow hooks get disabled.
- Hooks print the reason to stderr in one or two lines the agent can act on.
- A hook is a safety net, not a sandbox. For untrusted code, also run in a sandbox without network.

## Output

The files created, the settings diff, and the result of each test trigger.
