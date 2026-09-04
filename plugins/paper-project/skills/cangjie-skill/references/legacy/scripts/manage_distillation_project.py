#!/usr/bin/env python3
"""Command-line interface for Cangjie knowledge-distillation projects."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from distillation_project import (
    ProjectError,
    initialize_project,
    parse_source,
    project_status,
    validate_project,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="initialize a distillation project")
    init.add_argument("--project-root", type=Path, required=True)
    init.add_argument("--project-id", required=True)
    init.add_argument("--topic", required=True)
    init.add_argument("--source-id", required=True)
    init.add_argument("--source-pdf", type=Path, required=True)
    init.add_argument("--title", required=True)
    init.add_argument("--scope-file", type=Path)
    parse = commands.add_parser("parse", help="parse a copied project source")
    parse.add_argument("--project-root", type=Path, required=True)
    parse.add_argument("--source-id", required=True)
    parse.add_argument("--force", action="store_true")
    status = commands.add_parser("status", help="report project progress")
    status.add_argument("--project-root", type=Path, required=True)
    status.add_argument("--json", action="store_true")
    validate = commands.add_parser("validate", help="validate project integrity")
    validate.add_argument("--project-root", type=Path, required=True)
    validate.add_argument("--shared-root", type=Path)
    validate.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "init":
            initialize_project(
                args.project_root,
                args.project_id,
                args.topic,
                args.source_id,
                args.source_pdf,
                args.title,
                args.scope_file,
            )
            print(args.project_root.resolve())
            return 0
        if args.command == "parse":
            output = parse_source(args.project_root, args.source_id, force=args.force)
            print(output)
            return 0
        if args.command == "status":
            status = project_status(args.project_root)
            print(json.dumps(status, ensure_ascii=False, indent=2))
            return 0
        if args.command == "validate":
            issues = validate_project(args.project_root, args.shared_root)
            if args.json:
                print(
                    json.dumps(
                        [issue._asdict() for issue in issues],
                        ensure_ascii=False,
                        indent=2,
                    )
                )
            else:
                for issue in issues:
                    print(f"{issue.level}: {issue.code}: {issue.path}: {issue.message}")
            return 1 if any(issue.level == "error" for issue in issues) else 0
    except ProjectError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
