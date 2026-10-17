"""Dependency-free smoke checks for the Railway wrapper repository."""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RepositorySmokeTests(unittest.TestCase):
    def test_server_parses(self):
        ast.parse((ROOT / "server.py").read_text(encoding="utf-8"))

    def test_telegram_route_exists(self):
        source = (ROOT / "server.py").read_text(encoding="utf-8")
        self.assertIn('Route("/telegram", route_telegram', source)

    def test_persistent_volume_is_not_replaced(self):
        startup = (ROOT / "start.sh").read_text(encoding="utf-8")
        self.assertIn("/data/.hermes", startup)


if __name__ == "__main__":
    unittest.main()
