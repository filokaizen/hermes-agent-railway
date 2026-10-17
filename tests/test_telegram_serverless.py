"""Lightweight checks; no Railway or Telegram secrets required."""
import ast
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "server.py").read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)


class TelegramServerlessTests(unittest.TestCase):
    def test_webhook_route_registered_before_generic_proxy(self):
        index = SOURCE.index('Route("/telegram", route_telegram, methods=["POST"])')
        self.assertLess(index, SOURCE.index('Route("/{path:path}"'))

    def test_public_webhook_requires_secret(self):
        func = next(n for n in TREE.body if isinstance(n, ast.AsyncFunctionDef) and n.name == "route_telegram")
        code = ast.get_source_segment(SOURCE, func)
        self.assertIn("hmac.compare_digest", code)
        self.assertIn("X-Telegram-Bot-Api-Secret-Token", code)
        self.assertIn("127.0.0.1", code)
        self.assertIn("status_code=503", code)

    def test_gateway_does_not_rewrite_existing_config_on_start(self):
        manager = next(n for n in TREE.body if isinstance(n, ast.ClassDef) and n.name == "Gateway")
        start = next(n for n in manager.body if isinstance(n, ast.AsyncFunctionDef) and n.name == "start")
        code = ast.get_source_segment(SOURCE, start)
        self.assertIn("if not config_path.exists():", code)
        self.assertIn("write_config_yaml(read_env(ENV_FILE))", code)


if __name__ == "__main__":
    unittest.main()
