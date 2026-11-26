---
name: quality-ratchet
description: "Use when setting up CI quality gates for a codebase that gets agent-written PRs, when a legacy repo can't meet strict thresholds yet, or when the user wants 'no PR can make things worse'. Freezes current metrics (coverage, warnings, duplication, file size) in a baseline and fails any change that makes one of them worse, tightening the baseline as things improve."
---

# Quality ratchet

Legacy code can't pass strict quality gates on day one, and agents will happily add one more 900-line file. A ratchet solves both: today's numbers become the floor, any PR may add code but may not make a metric worse, and every improvement raises the floor. From Lucas Montano's 2026 talk on dropping line-by-line AI reviews in favor of deterministic gates.

## Inputs

- Commands that produce each metric in the repo (examples below).
- Where CI runs (GitHub Actions, Azure DevOps, GitLab, Jenkins).

## Steps

1. **Pick 3 to 6 metrics** that can be computed by a command and written to JSON. Common ones:
   - test coverage % (coverlet / `dotnet test --collect`, `ng test --code-coverage`, `jest --coverage`)
   - build warnings count
   - lint errors count
   - duplication % (jscpd)
   - largest file in lines, number of files over 500 lines
2. **Write `ratchet.config.json`** declaring, for each metric, the command that prints a number and whether higher or lower is better.
3. **Create the baseline**: `python3 scripts/ratchet.py init` runs every command and saves `quality-baseline.json`. Commit it.
4. **Add the CI step**: `python3 scripts/ratchet.py check`. It fails (exit 1) if any metric got worse than the baseline, printing which and by how much.
5. **Tighten on improvement**: on the main branch after merge, run `python3 scripts/ratchet.py update`, which only moves numbers in the better direction, and commit the new baseline.
6. **Tell the agent**: add one line to CLAUDE.md pointing to the check, so it runs `ratchet.py check` before finishing.

## Rules

- The baseline only moves toward better. Loosening it is a human decision in its own PR, with a reason.
- Keep each metric command fast enough for CI; slow metrics run nightly instead.

## Output

The config, the script in place, the first baseline, and the CI snippet.

## Example `ratchet.config.json`

```json
{
  "metrics": {
    "coverage_pct": {"cmd": "python3 tools/coverage_pct.py", "better": "higher"},
    "build_warnings": {"cmd": "dotnet build -nologo 2>&1 | grep -c 'warning '", "better": "lower"},
    "files_over_500_lines": {"cmd": "git ls-files '*.cs' '*.ts' | xargs wc -l | awk '$1>500 && $2!=\"total\"' | wc -l", "better": "lower"}
  }
}
```
