#!/usr/bin/env python3
"""Wake a Codex thread after one PBS/Torque job leaves qstat."""

from __future__ import annotations

import argparse
import math
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence


HOST_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.-]*$")
JOB_ID_PATTERN = re.compile(r"^[0-9]+(?:\.[A-Za-z0-9][A-Za-z0-9.-]*)?$")
THREAD_ID_PATTERN = re.compile(r"^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$")
MESSAGE_LIMIT = 16 * 1024
Runner = Callable[[list[str]], Any]


@dataclass(frozen=True)
class Config:
    host: str
    job_id: str
    thread_id: str
    spec: Path
    run: Path
    message: str
    interval: float


def _existing_absolute_path(value: str, label: str) -> Path:
    path = Path(value)
    if not path.is_absolute() or not path.exists():
        raise ValueError(f"{label} path must be absolute and existing")
    return path.resolve()


def parse_args(argv: Sequence[str] | None = None) -> Config:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--thread-id", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--run", required=True)
    parser.add_argument("--message", required=True)
    parser.add_argument("--interval", type=float, default=30.0)
    args = parser.parse_args(argv)

    if not HOST_PATTERN.fullmatch(args.host):
        raise ValueError("invalid host")
    if not JOB_ID_PATTERN.fullmatch(args.job_id):
        raise ValueError("invalid PBS job ID")
    if not THREAD_ID_PATTERN.fullmatch(args.thread_id):
        raise ValueError("invalid Codex thread ID")
    if "\0" in args.message:
        raise ValueError("message contains NUL")
    if len(args.message.encode("utf-8")) > MESSAGE_LIMIT:
        raise ValueError("message exceeds 16 KiB")
    if not math.isfinite(args.interval) or args.interval <= 0:
        raise ValueError("interval must be positive and finite")

    return Config(
        host=args.host,
        job_id=args.job_id,
        thread_id=args.thread_id,
        spec=_existing_absolute_path(args.spec, "Spec"),
        run=_existing_absolute_path(args.run, "Run"),
        message=args.message,
        interval=args.interval,
    )


def build_delivery(config: Config) -> str:
    return (
        "PBS_JOB_LEFT_QSTAT\n"
        f"host={config.host}\n"
        f"job_id={config.job_id}\n"
        f"spec={config.spec}\n"
        f"run={config.run}\n"
        f"instruction={config.message}"
    )


def wait_until_left_qstat(
    config: Config,
    *,
    runner: Runner = subprocess.run,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    command = ["ssh", config.host, "qstat", config.job_id]
    while True:
        result = runner(command)
        if result.returncode != 0:
            return result.returncode
        sleep(config.interval)


def deliver(config: Config, *, runner: Runner = subprocess.run) -> int:
    result = runner(
        [
            "codex",
            "queue",
            "--thread",
            config.thread_id,
            "--message",
            build_delivery(config),
        ]
    )
    return result.returncode


def main(argv: Sequence[str] | None = None) -> int:
    try:
        config = parse_args(argv)
        wait_until_left_qstat(config)
        return deliver(config)
    except (OSError, ValueError) as error:
        print(error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
