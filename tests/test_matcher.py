import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from hostcaps.matcher import match

ROOT = Path(__file__).resolve().parents[1]


class MatcherTests(unittest.TestCase):
    def load(self, path):
        return json.loads((ROOT / path).read_text())

    def test_forgejo_is_compatible(self):
        report = match(
            self.load("examples/host-public.json"),
            self.load("profiles/forgejo.json"),
            now=datetime(2026, 7, 24, 16, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(report["status"], "compatible")
        self.assertEqual(report["summary"]["fail"], 0)

    def test_mastodon_fails_when_memory_is_too_low(self):
        host = self.load("examples/host-public.json")
        host["capabilities"]["compute"]["memory_mib"] = 4096
        report = match(host, self.load("profiles/mastodon.json"))
        self.assertEqual(report["status"], "incompatible")

    def test_missing_required_capability_is_unknown(self):
        host = self.load("examples/host-public.json")
        del host["capabilities"]["federation"]["matrix"]
        report = match(host, self.load("profiles/matrix-synapse.json"))
        self.assertEqual(report["status"], "unknown")

    def test_stale_required_evidence_is_unknown(self):
        profile = self.load("profiles/forgejo.json")
        profile["requirements"][1]["max_evidence_age_seconds"] = 60
        report = match(
            self.load("examples/host-public.json"),
            profile,
            now=datetime(2026, 7, 24, 17, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(report["status"], "unknown")


if __name__ == "__main__":
    unittest.main()
