"""Policy-based redaction for public capability views."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


def delete_path(doc: dict[str, Any], path: str) -> bool:
    parts = path.split(".")
    current: Any = doc
    for part in parts[:-1]:
        if not isinstance(current, dict) or part not in current:
            return False
        current = current[part]
    if isinstance(current, dict) and parts[-1] in current:
        del current[parts[-1]]
        return True
    return False


def redact(doc: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(doc)
    removed: list[str] = []
    for path in policy.get("remove_paths", []):
        if delete_path(result, path):
            removed.append(path)
    result["disclosure"] = {
        "view": policy.get("view", "public"),
        "redacted": sorted(removed),
    }
    return result
