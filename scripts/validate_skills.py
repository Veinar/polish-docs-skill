#!/usr/bin/env python3
"""Validate SKILL.md files against the Agent Skills spec (https://agentskills.io/specification).

Usage: python scripts/validate_skills.py [skills_dir]
Stdlib only, so it runs in CI without installing anything.
"""
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED = ("anthropic", "claude")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
# Anthropic's recommended ceiling for the SKILL.md body
MAX_BODY_LINES = 500
EM_DASH = "\u2014"


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    fields = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    return fields, text[end + 5:]


def validate(skill_md):
    errors = []
    fields, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if fields is None:
        return ["missing or malformed YAML frontmatter"]

    name = fields.get("name", "")
    if not name:
        errors.append("missing 'name'")
    else:
        if len(name) > MAX_NAME:
            errors.append(f"'name' longer than {MAX_NAME} characters")
        if not NAME_RE.match(name):
            errors.append("'name' must be lowercase letters, digits and single hyphens")
        if any(word in name for word in RESERVED):
            errors.append(f"'name' contains a reserved word {RESERVED}")
        if name != skill_md.parent.name:
            errors.append(f"'name' ({name}) must match directory ({skill_md.parent.name})")

    description = fields.get("description", "")
    if not description:
        errors.append("missing 'description'")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"'description' is {len(description)} chars (max {MAX_DESCRIPTION})")
    if re.search(r"<[^>]+>", name + description):
        errors.append("'name'/'description' must not contain XML tags")

    body_lines = len(body.splitlines())
    if body_lines > MAX_BODY_LINES:
        errors.append(f"body has {body_lines} lines (recommended max {MAX_BODY_LINES})")

    # House style: the em dash is forbidden in skill files, en dash only
    for number, line in enumerate(skill_md.read_text(encoding="utf-8").splitlines(), 1):
        if EM_DASH in line:
            errors.append(f"em dash (U+2014) on line {number}; use en dash (U+2013)")

    for link in re.findall(r"\]\(([^)#]+)\)", body):
        if not link.startswith(("http://", "https://")) and not (skill_md.parent / link).exists():
            errors.append(f"broken relative link: {link}")
    return errors


def main():
    skills_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "skills")
    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        print(f"No */SKILL.md found under {skills_dir}")
        return 1
    failed = False
    for skill_md in skill_files:
        errors = validate(skill_md)
        for ref in sorted(skill_md.parent.rglob("*.md")):
            if ref == skill_md:
                continue
            for number, line in enumerate(ref.read_text(encoding="utf-8").splitlines(), 1):
                if EM_DASH in line:
                    errors.append(f"em dash (U+2014) in {ref.relative_to(skill_md.parent)}:{number}; use en dash (U+2013)")
        status = "FAIL" if errors else "OK"
        print(f"[{status}] {skill_md}")
        for error in errors:
            print(f"    - {error}")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
