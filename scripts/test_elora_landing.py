#!/usr/bin/env python3
"""Regression checks for ELORA AI's responsive, keyboard-accessible navigation."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


class LandingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.menu_button = None
        self.navigation = None
        self.links = []
        self.in_primary_navigation = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "button" and "menu-toggle" in attrs.get("class", "").split():
            self.menu_button = attrs
        if tag == "div" and attrs.get("id") == "primary-navigation":
            self.navigation = attrs
        if tag == "nav" and attrs.get("aria-label") == "Main navigation":
            self.in_primary_navigation = True
        if tag == "a" and self.in_primary_navigation:
            self.links.append(attrs)

    def handle_endtag(self, tag):
        if tag == "nav" and self.in_primary_navigation:
            self.in_primary_navigation = False


class ResponsiveNavigationTests(unittest.TestCase):
    def setUp(self):
        self.parser = LandingParser()
        self.parser.feed(HTML)

    def test_ids_are_unique(self):
        self.assertEqual(len(self.parser.ids), len(set(self.parser.ids)))

    def test_menu_button_has_accessible_control_state(self):
        self.assertIsNotNone(self.parser.menu_button)
        self.assertEqual(self.parser.menu_button.get("type"), "button")
        self.assertEqual(self.parser.menu_button.get("aria-expanded"), "false")
        self.assertEqual(self.parser.menu_button.get("aria-controls"), "primary-navigation")

    def test_navigation_has_stable_id_and_all_primary_links(self):
        self.assertIsNotNone(self.parser.navigation)
        self.assertEqual(self.parser.navigation.get("id"), "primary-navigation")
        self.assertEqual(len(self.parser.links), 3)
        self.assertTrue(any(link.get("href") == "mailto:owner@elora.ai" for link in self.parser.links))

    def test_mobile_menu_and_keyboard_dismissal_are_implemented(self):
        self.assertIn("@media(max-width:760px)", HTML)
        self.assertIn(".navlinks.is-open{display:flex}", HTML)
        self.assertIn('event.key === "Escape"', HTML)
        self.assertIn("menuToggle.focus()", HTML)
        self.assertIn('event.target.closest("a")', HTML)

    def test_reduced_motion_preference_is_preserved(self):
        self.assertIn("@media(prefers-reduced-motion:reduce)", HTML)


if __name__ == "__main__":
    unittest.main(verbosity=2)
