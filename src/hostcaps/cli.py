"""Command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .canonical import fingerprint
from .matcher import match
from .model import ValidationError, validate_host_manifest, validate_service_profile
from .privacy import redact


def load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump_json(value: Any, output: str | None) -> None:
    text = json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if output:
        Path(output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hostcaps")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate a host manifest or service profile")
    validate.add_argument("kind", choices=["host", "profile"])
    validate.add_argument("file")

    matcher = sub.add_parser("match", help="match a host against a service profile")
    matcher.add_argument("host")
    matcher.add_argument("profile")
    matcher.add_argument("--output")

    fp = sub.add_parser("fingerprint", help="print a deterministic document fingerprint")
    fp.add_argument("file")

    redactor = sub.add_parser("redact", help="create a policy-redacted public view")
    redactor.add_argument("manifest")
    redactor.add_argument("policy")
    redactor.add_argument("--output")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            doc = load_json(args.file)
            if args.kind == "host":
                validate_host_manifest(doc)
            else:
                validate_service_profile(doc)
            print("valid")
            return 0
        if args.command == "match":
            dump_json(match(load_json(args.host), load_json(args.profile)), args.output)
            return 0
        if args.command == "fingerprint":
            print(fingerprint(load_json(args.file)))
            return 0
        if args.command == "redact":
            dump_json(redact(load_json(args.manifest), load_json(args.policy)), args.output)
            return 0
    except (OSError, json.JSONDecodeError, ValidationError, ValueError, TypeError) as exc:
        parser.exit(2, f"hostcaps: error: {exc}\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
