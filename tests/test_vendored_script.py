"""setup ships a byte-identical copy of health-check's canonical check_brain.py."""
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / "plugins/scarecrow/skills"


class VendoredScript(unittest.TestCase):
    def test_setup_copy_matches_health_check(self):
        canonical = (SKILLS / "health-check/scripts/check_brain.py").read_bytes()
        copy = (SKILLS / "setup/scripts/check_brain.py").read_bytes()
        self.assertEqual(copy, canonical,
                         "setup/scripts/check_brain.py differs; edit the health-check copy, then copy it over")


if __name__ == "__main__":
    unittest.main()
