"""Lightweight validation for the v0.1 manifests.

The JSON Schemas in ``schemas/`` are the normative draft artefacts. This
module intentionally performs a dependency-free structural validation so the
starter repository can be executed without network access.
"""

from __future__ import annotations

from typing import Any


class ValidationError(ValueError):
    pass


def _require(mapping: dict[str, Any], key: str, expected: type, where: str) -> Any:
    if key not in mapping:
        raise ValidationError(f"{where}: missing required key '{key}'")
    value = mapping[key]
    if not isinstance(value, expected):
        raise ValidationError(
            f"{where}.{key}: expected {expected.__name__}, got {type(value).__name__}"
        )
    return value


def validate_host_manifest(doc: Any) -> None:
    if not isinstance(doc, dict):
        raise ValidationError("host manifest must be a JSON object")
    _require(doc, "spec_version", str, "host manifest")
    host = _require(doc, "host", dict, "host manifest")
    _require(host, "id", str, "host")
    _require(host, "generated_at", str, "host")
    capabilities = _require(doc, "capabilities", dict, "host manifest")
    if not capabilities:
        raise ValidationError("capabilities must not be empty")
    evidence = doc.get("evidence", [])
    if not isinstance(evidence, list):
        raise ValidationError("evidence must be an array")
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            raise ValidationError(f"evidence[{index}] must be an object")
        _require(item, "path", str, f"evidence[{index}]")
        _require(item, "method", str, f"evidence[{index}]")
        _require(item, "collected_at", str, f"evidence[{index}]")


def validate_service_profile(doc: Any) -> None:
    if not isinstance(doc, dict):
        raise ValidationError("service profile must be a JSON object")
    _require(doc, "spec_version", str, "service profile")
    service = _require(doc, "service", dict, "service profile")
    _require(service, "id", str, "service")
    _require(service, "name", str, "service")
    rules = _require(doc, "requirements", list, "service profile")
    if not rules:
        raise ValidationError("requirements must not be empty")
    allowed_ops = {
        "eq",
        "neq",
        "gte",
        "lte",
        "contains",
        "contains_any",
        "exists",
        "version_gte",
    }
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            raise ValidationError(f"requirements[{index}] must be an object")
        _require(rule, "id", str, f"requirements[{index}]")
        _require(rule, "path", str, f"requirements[{index}]")
        op = _require(rule, "op", str, f"requirements[{index}]")
        if op not in allowed_ops:
            raise ValidationError(f"requirements[{index}].op: unsupported operator '{op}'")
        severity = rule.get("severity", "required")
        if severity not in {"required", "preferred"}:
            raise ValidationError(
                f"requirements[{index}].severity must be 'required' or 'preferred'"
            )
        if op != "exists" and "value" not in rule:
            raise ValidationError(f"requirements[{index}]: operator '{op}' requires value")
