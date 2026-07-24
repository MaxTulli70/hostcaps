import json
import unittest
from pathlib import Path

from hostcaps.model import ValidationError, validate_host_manifest, validate_service_profile

ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def test_example_host_is_valid(self):
        validate_host_manifest(json.loads((ROOT / "examples/host-public.json").read_text()))

    def test_example_profile_is_valid(self):
        validate_service_profile(json.loads((ROOT / "profiles/forgejo.json").read_text()))

    def test_missing_capabilities_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_host_manifest({"spec_version": "0.1", "host": {"id": "x", "generated_at": "2026-01-01T00:00:00Z"}})


if __name__ == "__main__":
    unittest.main()
