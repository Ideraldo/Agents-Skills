---
name: spec-interview
description: "Use before implementing a feature, story or bug fix whose requirements are fuzzy, or when the user says 'interview me', 'let's write a spec', or starts an SDD/BMAD flow. Asks focused multiple-choice questions until it can write a SPEC.md with acceptance criteria, edge cases and what must not change, then hands off to implementation in a fresh session."
---

# Spec interview

The agent interviews the human, not the other way around. The output is a short SPEC.md whose acceptance criteria a human approved, because that is where specs pay off: studies in 2026 found most spec files get one commit and are rarely read in full, while human-approved acceptance criteria tied to tests are what improve results.

## Inputs

- The request, ticket or story, plus any linked material.
- The relevant code area (read it before asking, so questions are specific).

## Steps

1. **Read first.** Skim the code and docs the change touches. Never ask what the code already answers.
2. **Find the gaps.** List conflicts between rules, states with no defined behavior, ambiguous terms ("valid", "recent", "large") and missing error cases. Read each requirement two or three different ways; if the readings differ, it is ambiguous.
3. **Interview in rounds of 1 to 4 questions.** Use the AskUserQuestion tool when available, otherwise plain numbered questions. Each question offers 2 to 4 concrete options with the recommended one first. Order of rounds:
   1. Goal and who uses it
   2. Behavior and business rules
   3. Edge cases and errors
   4. What must not change (contracts, other flows, data)
   5. How we will know it works (acceptance checks)
4. **Stop when** every acceptance criterion is testable and no open question changes the design. Usually 2 to 4 rounds.
5. **Write SPEC.md** (format below) and ask the user to approve or edit the acceptance criteria.
6. **Hand off.** Suggest implementing in a new session or after `/clear`, starting from SPEC.md, so the implementation context is clean.

## Rules

- Never ask more than 4 questions at once.
- Every acceptance criterion must be checkable by running something (see the verify-work skill).
- Keep SPEC.md under about 80 lines. Long specs cost 40% to 130% more tokens and do not get read.
- Record decisions with their reason. Leave nothing as "TBD": write it as an open question with an owner.

## Output: SPEC.md

```
# <Feature>
Goal: <one sentence>

## Rules
- R1 ...

## Acceptance criteria
- [ ] AC1 Given ..., when ..., then ...
- [ ] AC2 ...

## Must not change
- ...

## Edge cases
- ...

## Decisions
- <decision> because <reason>

## Open questions
- <question> (owner)
```
