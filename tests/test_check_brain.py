"""Behavior tests for health-check's canonical check_brain.py. Standard library only.

Run from the repository root: python -m unittest discover -s tests
"""
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "plugins/scarecrow/skills/health-check/scripts/check_brain.py"
TODAY = "2026-10-27"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")


def page(title, extra=""):
    return f"---\ntype: concept\nsources:\n  - raw/a.md\nverified: 2026-10-01\n---\n# {title}\n{extra}"


class Brain(unittest.TestCase):
    """Each test starts from a minimal brain that passes the full check cleanly."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        r = self.root
        write(r / "AGENTS.md", """
            # Rules
            Sources in raw/ are immutable.
            ## Health check
            Next health check: 2026-11-20. Pages older than 90 days are stale.
            ## Folder map
            | Path | Purpose |
            |---|---|
            | `raw/` | sources |
            | `wiki/` | compiled pages |
            | `projects/` | work |
            | `_system/` | corrections and changelog |
            """)
        write(r / "CLAUDE.md", "# Brain\nRules live in AGENTS.md.\n@AGENTS.md\n")
        write(r / "open-questions.md", "# Open questions\n")
        write(r / "raw/a.md", "source\n")
        write(r / "wiki/index.md", "# Index\n- [Alpha](alpha.md) - alpha\n- [Beta](beta.md) - beta\n")
        write(r / "wiki/log.md", "# Log\n## [2026-10-01] ingest | a\nalpha.md beta.md raw/a.md\n")
        write(r / "wiki/alpha.md", page("Alpha", "[Beta](beta.md)\n"))
        write(r / "wiki/beta.md", page("Beta", "[Alpha](alpha.md)\n"))
        write(r / "_system/corrections.md", "# Corrections\n| Date | Wrong | Right |\n|---|---|---|\n")
        write(r / "_system/changelog.md", "# Changelog\n")
        write(r / "projects/acme/_index.md", """
            ---
            status: active
            last-updated: 2026-10-20
            decision: "2026-10-20: proceed"
            feedback: none
            log: "#log"
            ---
            # Acme
            """)
        write(r / "projects/acme/status.md", "# Status\nLast updated: 2026-10-20\n")
        self.run_script("--record-raw")

    def tearDown(self):
        self.tmp.cleanup()

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.root), *args],
                              capture_output=True, text=True, encoding="utf-8")

    def check(self, *args):
        proc = self.run_script("--json", "--today", TODAY, *args)
        self.assertNotIn("Traceback", proc.stderr, proc.stderr)
        return proc, json.loads(proc.stdout)

    def hits(self, data, check, level=None):
        return [r for r in data["results"] if r["check"] == check and (level is None or r["level"] == level)]

    # ------------------------------------------------------------ baseline

    def test_baseline_passes(self):
        proc, data = self.check()
        self.assertEqual(proc.returncode, 0, data["results"])
        self.assertEqual(data["summary"], {"fail": 0, "warn": 0}, data["results"])

    # ------------------------------------------------------------ robustness

    def test_non_utf8_page_does_not_crash(self):
        write(self.root / "wiki/alpha.md", page("Alpha", "caf\xe9 [Beta](beta.md)\n").encode("latin-1"))
        proc, data = self.check()
        self.assertEqual(data["summary"]["fail"], 0, data["results"])

    def test_bom_before_frontmatter_is_accepted(self):
        write(self.root / "wiki/alpha.md", b"\xef\xbb\xbf" + page("Alpha", "[Beta](beta.md)\n").encode())
        _, data = self.check()
        self.assertEqual(self.hits(data, "M4"), [])

    def test_invalid_health_check_date_is_a_fail_not_a_crash(self):
        agents = self.root / "AGENTS.md"
        agents.write_text(agents.read_text().replace("2026-11-20", "2026-11-31"), encoding="utf-8")
        proc, data = self.check()
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(any("2026-11-31" in r["msg"] for r in self.hits(data, "M3", "FAIL")), data["results"])

    def test_invalid_status_and_log_dates_do_not_crash(self):
        write(self.root / "projects/acme/status.md", "Last updated: 2026-02-30\n")
        write(self.root / "wiki/log.md", "# Log\n## [2026-13-01] ingest | a\nalpha.md beta.md raw/a.md\n")
        self.check()

    def test_corrupt_manifest_is_a_fail_not_a_crash(self):
        (self.root / "raw/.manifest.json").write_text("{", encoding="utf-8")
        proc, data = self.check()
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(self.hits(data, "M7", "FAIL"))
        rec = self.run_script("--record-raw")
        self.assertNotIn("Traceback", rec.stderr)
        self.assertEqual(rec.returncode, 1)

    # ------------------------------------------------------------ links (M6)

    def test_percent_encoded_and_angle_bracket_links_resolve(self):
        write(self.root / "wiki/my note.md", page("My note", "[Alpha](alpha.md)\n"))
        write(self.root / "wiki/index.md", "# Index\n- [Alpha](alpha.md)\n- [Beta](beta.md)\n"
                                           "- [My note](my%20note.md)\n- [Again](<my note.md>)\n")
        _, data = self.check()
        self.assertEqual(self.hits(data, "M6"), [], data["results"])
        self.assertEqual(self.hits(data, "M5"), [], data["results"])

    def test_links_inside_code_are_ignored(self):
        write(self.root / "wiki/alpha.md", page("Alpha", "[Beta](beta.md)\n\n```markdown\n[x](<page>.md)\n```\n"
                                                         "Inline `[y](missing.md)` too.\n"))
        _, data = self.check()
        self.assertEqual(self.hits(data, "M6"), [], data["results"])

    def test_real_broken_link_still_fails(self):
        write(self.root / "wiki/alpha.md", page("Alpha", "[Beta](beta.md) [Gone](gone.md)\n"))
        _, data = self.check()
        self.assertEqual(len(self.hits(data, "M6", "FAIL")), 1, data["results"])

    # ------------------------------------------------------------ index (M5)

    def test_page_whose_name_is_a_substring_of_a_listed_page_is_not_listed(self):
        write(self.root / "wiki/al.md", page("Al", "[Alpha](alpha.md)\n"))
        _, data = self.check()
        self.assertTrue(any(r["path"] == "wiki/al.md" for r in self.hits(data, "M5", "FAIL")), data["results"])

    def test_wikilink_in_index_counts_as_listed(self):
        write(self.root / "wiki/index.md", "# Index\n- [[alpha]]\n- [[beta|Beta page]]\n")
        _, data = self.check()
        self.assertEqual(self.hits(data, "M5"), [], data["results"])

    def test_nested_page_listed_by_relative_link(self):
        write(self.root / "wiki/topics/gamma.md", page("Gamma", "[Alpha](../alpha.md)\n"))
        idx = self.root / "wiki/index.md"
        idx.write_text(idx.read_text() + "- [Gamma](topics/gamma.md)\n", encoding="utf-8")
        _, data = self.check()
        self.assertEqual(self.hits(data, "M5"), [], data["results"])

    # ------------------------------------------------------------ status age (M15)

    def test_fresh_copy_does_not_report_project_files_newer_than_status(self):
        # Every file was just written, as after a clone or sync; status.md says it was updated on 2026-10-20.
        _, data = self.check()
        self.assertEqual(self.hits(data, "M15"), [], data["results"])

    def test_file_edited_on_a_later_day_than_status_is_reported(self):
        status = self.root / "projects/acme/status.md"
        later = self.root / "projects/acme/notes.md"
        write(later, "notes\n")
        day = 86400
        now = time.time()
        os.utime(status, (now - 3 * day, now - 3 * day))
        os.utime(later, (now, now))
        write(status, "# Status\nLast updated: 2026-10-20\n")
        os.utime(status, (now - 3 * day, now - 3 * day))
        proc = self.run_script("--json")  # real today, so mtimes and dates agree
        data = json.loads(proc.stdout)
        self.assertTrue(any("changed after" in r["msg"] for r in self.hits(data, "M15")), data["results"])

    # ------------------------------------------------------------ messages (M9)

    def test_bad_status_message_lists_every_accepted_status(self):
        hub = self.root / "projects/acme/_index.md"
        hub.write_text(hub.read_text().replace("status: active", "status: live"), encoding="utf-8")
        _, data = self.check()
        msg = " ".join(r["msg"] for r in self.hits(data, "M9"))
        for s in ("active", "paused", "done", "reference", "draft", "testing", "stable", "deprecated"):
            self.assertIn(s, msg)


if __name__ == "__main__":
    unittest.main()
