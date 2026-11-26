#!/usr/bin/env python3
"""Quality ratchet: metrics may only get better.

Usage:
  python3 ratchet.py init     # run all metrics, write quality-baseline.json
  python3 ratchet.py check    # fail (exit 1) if any metric is worse than baseline
  python3 ratchet.py update   # move baseline only in the better direction

Reads ratchet.config.json: {"metrics": {"name": {"cmd": "...", "better": "higher|lower"}}}
Each cmd must print a single number on its last line.
"""
import json
import subprocess
import sys

CONFIG, BASELINE = "ratchet.config.json", "quality-baseline.json"


def measure(cmd):
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip().splitlines()
    if not out:
        raise RuntimeError(f"no output from: {cmd}")
    return float(out[-1].strip().rstrip("%"))


def run_all(metrics):
    return {name: measure(m["cmd"]) for name, m in metrics.items()}


def worse(name, now, base, better):
    return now < base if better == "higher" else now > base


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("init", "check", "update"):
        print(__doc__)
        sys.exit(2)
    mode = sys.argv[1]
    metrics = json.load(open(CONFIG))["metrics"]
    current = run_all(metrics)

    if mode == "init":
        json.dump(current, open(BASELINE, "w"), indent=2)
        print(json.dumps(current, indent=2))
        return

    base = json.load(open(BASELINE))
    failed = False
    for name, m in metrics.items():
        now, b = current[name], base.get(name)
        if b is None:
            print(f"NEW   {name}: {now} (not in baseline)")
            continue
        if worse(name, now, b, m["better"]):
            failed = True
            print(f"WORSE {name}: {b} -> {now} ({m['better']} is better)")
        else:
            print(f"OK    {name}: {b} -> {now}")
            if mode == "update":
                base[name] = now
    if mode == "update":
        for name in current:
            base.setdefault(name, current[name])
        json.dump(base, open(BASELINE, "w"), indent=2)
        print("baseline updated (only in the better direction)")
        return
    if failed:
        print("\nQuality ratchet failed: a metric got worse than the baseline.")
        sys.exit(1)


if __name__ == "__main__":
    main()
