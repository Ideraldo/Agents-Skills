---
name: pr-babysit
description: "Use after opening a pull request, or when the user says 'watch this PR', 'get it green' or 'handle the review comments'. Monitors CI and review comments, fixes what it can, replies to each comment with what changed, and stops when the PR is green and every thread is answered, or when a human decision is needed."
---

# PR babysit

The work after opening a PR (waiting for CI, fixing flaky failures, answering comments) is repetitive and easy to hand to an agent. Pattern from the Claude Code team's "the work after you open a PR" and Lucas Montano's 2026 workflow.

## Inputs

- PR link or number, and access through the `gh` CLI (or the platform's CLI/API).

## Steps

1. **Read the state**: CI checks (`gh pr checks`), review threads (`gh pr view --comments`, or the API for line comments), merge conflicts.
2. **CI red**: open the failing job log, find the first real error, reproduce locally, fix, push. If a test is flaky (passes on rerun with no change), say so in the PR instead of adding retries or skips.
3. **Review comments**: for each unresolved thread:
   - clear request: make the change, push, reply with what changed and the commit
   - question: answer from the code, with file:line
   - disagreement or design choice: do not decide; reply that it needs the author, and list it for the human
4. **Conflicts**: rebase or merge from the base branch only if the conflicts are mechanical; otherwise stop and report.
5. **Loop** with a wait between checks (or a scheduled check) until green and all threads answered. Max 5 rounds.
6. **Final report** to the human.

## Rules

- Never force-push over someone else's commits, never merge the PR, never resolve a thread opened by a human reviewer unless they asked.
- Every reply on the PR says what changed and links the commit. No vague "fixed".
- Keep fixes inside the PR's scope; new problems found go into a list, not into this PR.

## Output

| Item | Status | Action taken | Needs human? |

Ends with: green and ready for human approval, or blocked on <what>.
