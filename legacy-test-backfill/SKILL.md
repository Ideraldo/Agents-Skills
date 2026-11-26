---
name: legacy-test-backfill
description: "Use when adding tests to existing code that has few or none, before refactoring or upgrading it, or when asked to raise coverage. Picks what to test by risk, writes characterization tests that assert real outputs, and runs an anti-cheat checklist so the agent cannot make tests pass by weakening them or touching production code."
---

# Legacy test backfill

Agents write a lot of tests that prove little: a 2026 study found about 80% of agent-written tests do not check the output value at all. Duolingo merged 225,000 lines of agent-written tests by adding hard gates around them. This skill applies the same gates.

## Inputs

- The code area (project, folder, class).
- Test framework in use (xUnit, NUnit, MSTest, Jest, Jasmine/Karma, etc.) and how to run it.
- Optional: the functional spec (see legacy-spec-extraction).

## Steps

1. **Prioritize** by risk: money and dates, validations, branching business rules, code with recent bugs (`git log --grep fix`), code about to change. Skip trivial getters and pure plumbing.
2. **Write characterization tests**: capture what the code does today, even if it looks wrong. Name them for behavior (`Rejects_negative_amount`), not for methods.
3. **Assert real outputs**: returned values, persisted state, emitted events, error messages. A test with no assertion on output is not done.
4. **Cover edges** per rule: boundary values, null/empty, culture and timezone, rounding.
5. **Add property tests** for rules that are laws ("total equals sum of parts", "state X can never go back to Y"): FsCheck or CsCheck in .NET, fast-check in TypeScript.
6. **Run the anti-cheat checklist** (below) on the diff before reporting.
7. **Run the suite 3 times**; any test that flips is flaky. Fix the cause or remove it with a note; never add sleeps or retries.

## Anti-cheat checklist

- [ ] Only test files, fixtures, fakes and mocks changed. Any production file touched: stop and report.
- [ ] No existing test deleted, skipped or with weakened assertions.
- [ ] No `Thread.Sleep`, `Task.Delay`, `setTimeout` waits or retry loops.
- [ ] No calls to real external services, paid APIs or shared databases.
- [ ] Every test has at least one assertion on an output or state.
- [ ] Tests fail when the behavior is broken: mutate one rule by hand (or with Stryker) and confirm a test goes red.

## Rules

- If a test reveals a likely bug, keep the test asserting current behavior, mark it with a comment and list it in the report. Fixing is a separate change.
- Keep test PRs separate from behavior changes.

## Output

- Tests added, grouped by rule.
- Checklist with each item ticked or explained.
- Suspected bugs found.
- Command and output of the final run.
