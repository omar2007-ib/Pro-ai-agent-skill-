#!/usr/bin/env python3
"""Dependency-free structural validator for portable Agent Skills in this repo.

This intentionally validates a small, documented subset of SKILL.md metadata;
it is not a full YAML parser and does not replace the official skills validator.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", re.DOTALL)


def validate_skill_file(path: Path) -> list[str]:
    """Return validation errors for one SKILL.md path; an empty list means pass."""
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{path}: cannot read UTF-8 file: {exc}"]

    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return [f"{path}: expected YAML frontmatter between opening and closing --- lines"]

    metadata: dict[str, str] = {}
    for line_number, line in enumerate(match.group(1).splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#") or line[:1].isspace():
            continue
        if ":" not in line:
            errors.append(f"{path}:{line_number}: malformed frontmatter entry")
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in metadata:
            errors.append(f"{path}:{line_number}: duplicate frontmatter key {key!r}")
            continue
        metadata[key] = value.strip("\"'")

    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if not name:
        errors.append(f"{path}: missing non-empty 'name' frontmatter field")
    elif len(name) > 64 or not NAME_PATTERN.fullmatch(name):
        errors.append(f"{path}: name must be kebab-case, 1-64 characters, without repeated hyphens")
    elif path.parent.name != name:
        errors.append(f"{path}: name {name!r} must match directory {path.parent.name!r}")

    if not description:
        errors.append(f"{path}: missing non-empty 'description' frontmatter field")
    elif len(description) > 1024:
        errors.append(f"{path}: description exceeds 1024 characters")
    elif "<" in description or ">" in description:
        errors.append(f"{path}: description must not contain angle brackets")

    body = match.group(2).strip()
    if not body:
        errors.append(f"{path}: skill instructions body is empty")
    if len(text.splitlines()) > 500:
        errors.append(f"{path}: SKILL.md exceeds the recommended 500-line limit")
    if not re.search(r"(?m)^#\s+\S", body):
        errors.append(f"{path}: body must contain a level-one Markdown title")
    return errors


def discover_skills(root: Path = SKILLS_ROOT) -> list[Path]:
    """Find skills under skills/<name>/SKILL.md without traversing unrelated files."""
    if not root.exists():
        return []
    return sorted(root.glob("*/SKILL.md"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, help="validate one SKILL.md instead of the repository catalog")
    args = parser.parse_args(argv)
    paths = [args.path] if args.path else discover_skills()
    if not paths:
        print("FAIL: no skills found; expected skills/<name>/SKILL.md")
        return 1

    failures = 0
    for path in paths:
        errors = validate_skill_file(path)
        if errors:
            failures += len(errors)
            for error in errors:
                print("FAIL:", error)
        else:
            print("PASS:", path)

    if failures:
        print(f"Result: FAILED ({failures} issue(s) across {len(paths)} skill file(s))")
        return 1
    print(f"Result: PASSED ({len(paths)} skill file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
