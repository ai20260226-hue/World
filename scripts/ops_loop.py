#!/usr/bin/env python3
"""Simple local operations loop for mission files.

- Watches `tasks/inbox/*.json`
- Runs runner/agent_runner.py for each mission file
- Moves processed missions to `tasks/done/` or `tasks/failed/`

This helps emulate a resilient always-on loop on a local PC.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import time
from pathlib import Path


def run_once(config: Path, inbox: Path, done: Path, failed: Path) -> int:
    inbox.mkdir(parents=True, exist_ok=True)
    done.mkdir(parents=True, exist_ok=True)
    failed.mkdir(parents=True, exist_ok=True)

    missions = sorted(inbox.glob("*.json"))
    if not missions:
        return 0

    processed = 0
    for mission in missions:
        proc = subprocess.run(
            [
                "python3",
                "runner/agent_runner.py",
                "--config",
                str(config),
                "--task",
                str(mission),
            ],
            text=True,
            capture_output=True,
        )
        target = done if proc.returncode == 0 else failed
        shutil.move(str(mission), str(target / mission.name))

        log_file = Path("logs/ops_loop.log")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as f:
            f.write(
                f"mission={mission.name} rc={proc.returncode} target={target.name}\n"
            )
            if proc.stdout:
                f.write(f"stdout={proc.stdout[-500:]}\n")
            if proc.stderr:
                f.write(f"stderr={proc.stderr[-500:]}\n")
        processed += 1
    return processed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="agents/company-A-research.json")
    parser.add_argument("--interval", type=int, default=30)
    parser.add_argument("--max-cycles", type=int, default=0, help="0 means unlimited")
    args = parser.parse_args()

    config = Path(args.config)
    inbox = Path("tasks/inbox")
    done = Path("tasks/done")
    failed = Path("tasks/failed")

    cycles = 0
    while True:
        run_once(config, inbox, done, failed)
        cycles += 1
        if args.max_cycles > 0 and cycles >= args.max_cycles:
            break
        time.sleep(args.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
