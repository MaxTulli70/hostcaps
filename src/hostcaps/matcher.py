"""Deterministic capability-to-requirement matching."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .model import validate_host_manifest, validate_service_profile


MISSING = object()


def get_path(doc: dict[str, Any], path: str) -> Any:
    current: Any = doc
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return MISSING
        current = current[part]
    return current


def _version_tuple(value: Any) -> tuple[int, ...]:
    text = str(value).strip()
    pieces: list[int] = []
    for token in text.split("."):
        digits = "".join(ch for ch in token if ch.isdigit())
        if not digits:
            break
        pieces.append(int(digits))
    return tuple(pieces)


def _evaluate(actual: Any, op: str, expected: Any) -> bool:
    if op == "exists":
        return actual is not MISSING
    if actual is MISSING:
        return False
    if op == "eq":
        return actual == expected
    if op == "neq":
        return actual != expected
    if op == "gte":
        return actual >= expected
    if op == "lte":
        return actual <= expected
    if op == "contains":
        return isinstance(actual, (list, str, dict)) and expected in actual
    if op == "contains_any":
        return isinstance(actual, list) and isinstance(expected, list) and any(
            item in actual for item in expected
        )
    if op == "version_gte":
        candidates = actual if isinstance(actual, list) else [actual]
        return any(_version_tuple(candidate) >= _version_tuple(expected) for candidate in candidates)
    raise ValueError(f"unsupported operator: {op}")


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _evidence_for(host: dict[str, Any], path: str) -> dict[str, Any] | None:
    for item in host.get("evidence", []):
        if item.get("path") == path:
            return item
    return None


def match(
    host: dict[str, Any],
    profile: dict[str, Any],
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    validate_host_manifest(host)
    validate_service_profile(profile)
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)

    results: list[dict[str, Any]] = []
    required_fail = False
    required_unknown = False
    preferred_issue = False

    for rule in profile["requirements"]:
        path = rule["path"]
        actual = get_path(host, path)
        evidence = _evidence_for(host, path)
        max_age = rule.get("max_evidence_age_seconds")
        stale = False
        if max_age is not None:
            if evidence is None:
                stale = True
            else:
                age = (now - _parse_time(evidence["collected_at"])).total_seconds()
                stale = age > int(max_age)

        if actual is MISSING or stale:
            outcome = "unknown"
            passed = False
            reason = "capability is not declared" if actual is MISSING else "supporting evidence is stale"
        else:
            passed = _evaluate(actual, rule["op"], rule.get("value"))
            outcome = "pass" if passed else "fail"
            reason = "constraint satisfied" if passed else "constraint not satisfied"

        severity = rule.get("severity", "required")
        if severity == "required":
            if outcome == "fail":
                required_fail = True
            elif outcome == "unknown":
                required_unknown = True
        elif outcome != "pass":
            preferred_issue = True

        results.append(
            {
                "id": rule["id"],
                "path": path,
                "severity": severity,
                "operator": rule["op"],
                "expected": rule.get("value"),
                "actual": None if actual is MISSING else actual,
                "outcome": outcome,
                "reason": reason,
                "evidence": evidence,
            }
        )

    if required_fail:
        status = "incompatible"
    elif required_unknown:
        status = "unknown"
    elif preferred_issue:
        status = "compatible_with_warnings"
    else:
        status = "compatible"

    return {
        "report_version": "0.1",
        "host_id": host["host"]["id"],
        "service_id": profile["service"]["id"],
        "status": status,
        "summary": {
            "pass": sum(item["outcome"] == "pass" for item in results),
            "fail": sum(item["outcome"] == "fail" for item in results),
            "unknown": sum(item["outcome"] == "unknown" for item in results),
        },
        "results": results,
    }
