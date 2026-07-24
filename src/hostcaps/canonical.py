"""Deterministic JSON encoding and fingerprints."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    """Return a stable UTF-8 JSON representation.

    This is a deterministic project encoding, not a claim of RFC 8785
    conformance. The funded work will review canonicalisation requirements.
    """

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()
