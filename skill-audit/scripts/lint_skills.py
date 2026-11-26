#!/usr/bin/env python3
"""Static lint for Agent Skills (SKILL.md). No dependencies.

Usage: python3 lint_skills.py <skill-folder-or-repo> [--strict]
Exit code 1 if any ERROR is found (or any WARN with --strict).
"""
import os
import re
import sys

PORTABLE_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
TRIGGER_WORDS = re.compile(r"\b(use (when|whenever|before|after|for|to)|use this|quando|sempre que)\b", re.I)
SECRET_PATTERNS = [
    re.compile(r"(api[_-]?key|secret|password|senha|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}", re.I),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]
PERSONAL_PATH = re.compile(r"(/Users/[A-Za-z]|/home/(?!claude)[a-z]+/|C:\\\\Users\\\\)")
MODEL_NAME = re.compile(r"\b(claude-(opus|sonnet|haiku|fable)-[0-9]|gpt-[0-9][\w.-]*)\b", re.I)
VERIFY_HEADING = re.compile(r"^#+\s*(output|verif|check|sa[ií]da|evid)", re.I | re.M)


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm, body = text[3:end], text[end + 4:]
    keys, cur = {}, None
    for line in fm.splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            cur = m.group(1)
            keys[cur] = m.group(2).strip().strip('"').strip("'")
        elif cur and line.startswith(" "):
            keys[cur] += " " + line.strip()
    return keys, body


def lint(path):
    issues = []
    folder = os.path.basename(os.path.dirname(path))
    text = open(path, encoding="utf-8").read()
    fm, body = parse_frontmatter(text)
    if fm is None:
        return [("ERROR", "missing YAML frontmatter")]
    for k in fm:
        if k not in PORTABLE_KEYS:
            issues.append(("WARN", f"frontmatter key '{k}' may not be portable outside Claude Code"))
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not name:
        issues.append(("ERROR", "missing name"))
    elif name != folder and folder != "_template":
        issues.append(("WARN", f"name '{name}' differs from folder '{folder}'"))
    if not desc:
        issues.append(("ERROR", "missing description"))
    else:
        if len(desc) < 30:
            issues.append(("ERROR", "description shorter than 30 chars"))
        if len(desc) > 1024:
            issues.append(("ERROR", f"description longer than 1024 chars ({len(desc)})"))
        if not TRIGGER_WORDS.search(desc):
            issues.append(("WARN", "description does not say when to use it ('Use when...')"))
    lines = body.count("\n") + 1
    if lines > 500:
        issues.append(("WARN", f"body has {lines} lines (> 500)"))
    if not VERIFY_HEADING.search(body):
        issues.append(("WARN", "no Output/Verification section"))
    for pat in SECRET_PATTERNS:
        if pat.search(text):
            issues.append(("ERROR", "possible secret: " + pat.pattern[:30]))
    if PERSONAL_PATH.search(text):
        issues.append(("WARN", "personal absolute path found"))
    if MODEL_NAME.search(text):
        issues.append(("WARN", "hardcoded model id; prefer describing capability"))
    if re.search(r"\b(IMPORTANT|NEVER|ALWAYS|MUST)\b.*\b(IMPORTANT|NEVER|ALWAYS|MUST)\b", body):
        issues.append(("INFO", "several all-caps imperatives on one line; newer models over-apply them"))
    return issues


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    root, strict = sys.argv[1], "--strict" in sys.argv
    files = []
    if os.path.isfile(root):
        files = [root]
    else:
        for d, dirs, fs in os.walk(root):
            dirs[:] = [x for x in dirs if not x.startswith(".") and x != "node_modules"]
            files += [os.path.join(d, f) for f in fs if f == "SKILL.md"]
    worst = 0
    for f in sorted(files):
        issues = lint(f)
        status = "OK" if not issues else ""
        print(f"{f}: {status}")
        for level, msg in issues:
            print(f"  {level}: {msg}")
            if level == "ERROR" or (strict and level == "WARN"):
                worst = 1
    print(f"\n{len(files)} skill(s) checked.")
    sys.exit(worst)


if __name__ == "__main__":
    main()
