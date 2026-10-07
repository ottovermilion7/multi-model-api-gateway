import pathlib
import unittest

ROOT = pathlib.Path(__file__).parents[1]


class ComposeTests(unittest.TestCase):
    def test_safe_compose_shape(self):
        compose = (ROOT / "compose/docker-compose.yml").read_text(encoding="utf-8")
        config = (ROOT / "compose/litellm.config.yaml").read_text(encoding="utf-8")
        self.assertIn("ghcr.io/berriai/litellm:v1.104.0", compose)
        self.assertIn("127.0.0.1:4000:4000", compose)
        self.assertIn("ARGO_API_KEY", compose)
        self.assertIn("https://argolink.io/v1", config)
        self.assertIn("gpt-6-sol", config)
        self.assertIn("fallbacks:", config)
        self.assertNotIn("sk-", compose + config)

    def test_readme_documents_safety_boundary(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("POST /v1/responses", readme)
        self.assertIn("ambiguous POST", readme)
        self.assertIn("image digest", readme)
        self.assertNotIn("api." + "argolink.io", readme)


if __name__ == "__main__":
    unittest.main()
