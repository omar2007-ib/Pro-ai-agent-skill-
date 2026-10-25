#!/usr/bin/env python3
"""Unit tests for the dependency-free Agent Skills validator."""
import tempfile
import unittest
from pathlib import Path

from validate_agent_skills import validate_skill_file


VALID_SKILL = """---
name: sample-skill
description: Review a repository before changing code and run focused tests.
---
# Sample Skill

Instructions.
"""


class ValidateSkillFileTests(unittest.TestCase):
    def make_skill(self, content: str, directory: str = "sample-skill") -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / directory / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_accepts_valid_skill(self):
        self.assertEqual(validate_skill_file(self.make_skill(VALID_SKILL)), [])

    def test_rejects_directory_name_mismatch(self):
        errors = validate_skill_file(self.make_skill(VALID_SKILL, directory="other-name"))
        self.assertTrue(any("must match directory" in error for error in errors))

    def test_rejects_missing_description(self):
        content = VALID_SKILL.replace(
            "description: Review a repository before changing code and run focused tests.\n", ""
        )
        errors = validate_skill_file(self.make_skill(content))
        self.assertTrue(any("missing non-empty 'description'" in error for error in errors))

    def test_rejects_invalid_name(self):
        content = VALID_SKILL.replace("name: sample-skill", "name: Sample--Skill")
        errors = validate_skill_file(self.make_skill(content))
        self.assertTrue(any("name must be kebab-case" in error for error in errors))

    def test_rejects_unclosed_frontmatter(self):
        content = VALID_SKILL.replace("\n---\n# Sample Skill", "\n# Sample Skill")
        errors = validate_skill_file(self.make_skill(content))
        self.assertTrue(any("expected YAML frontmatter" in error for error in errors))

    def test_rejects_overlong_description(self):
        content = VALID_SKILL.replace(
            "description: Review a repository before changing code and run focused tests.",
            "description: " + ("x" * 1025),
        )
        errors = validate_skill_file(self.make_skill(content))
        self.assertTrue(any("exceeds 1024 characters" in error for error in errors))

    def test_rejects_empty_body(self):
        content = "---\nname: sample-skill\ndescription: A valid description.\n---\n"
        errors = validate_skill_file(self.make_skill(content))
        self.assertTrue(any("body is empty" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
