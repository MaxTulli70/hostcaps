import json
import unittest
from pathlib import Path

from hostcaps.canonical import fingerprint
from hostcaps.privacy import redact

ROOT = Path(__file__).resolve().parents[1]


class PrivacyFingerprintTests(unittest.TestCase):
    def load(self, path):
        return json.loads((ROOT / path).read_text())

    def test_redaction_removes_private_paths(self):
        result = redact(
            self.load("examples/host-private.json"),
            self.load("examples/public-view-policy.json"),
        )
        self.assertNotIn("operator_contact", result["host"])
        self.assertNotIn("internal_asset_id", result["host"])
        self.assertEqual(result["disclosure"]["view"], "public")

    def test_fingerprint_is_key_order_independent(self):
        left = {"b": 2, "a": 1}
        right = {"a": 1, "b": 2}
        self.assertEqual(fingerprint(left), fingerprint(right))


if __name__ == "__main__":
    unittest.main()
