#!/usr/bin/env python3
"""HF Spaces向けミッションワーカー（1回処理 or ループ）。

想定:
- Spaceにこのリポジトリを配置
- `tasks/inbox/*.json` を処理
- 生成物は `artifacts/`, `logs/`, `memory/` に保存

使い方:
  python3 scripts/hf_space_worker.py --once
  python3 scripts/hf_space_worker.py --interval 60
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import time
from pathlib import Path

CONFIG = Path("agents/company-A-research.json")
INBOX = Path("tasks/inbox")
DONE = Path("tasks/done")
FAILED = Path("tasks/failed")


def process_one() -> int:
    INBOX.mkdir(parents=True, exist_ok=True)
    DONE.mkdir(parents=True, exist_ok=True)
    FAILED.mkdir(parents=True, exist_ok=True)

    missions = sorted(INBOX.glob("*.json"))
    if not missions:
        print("no-mission")
        return 0

    mission = missions[0]
    proc = subprocess.run(
        [
            "python3",
            "runner/agent_runner.py",
            "--config",
            str(CONFIG),
            "--task",
            str(mission),
        ],
        text=True,
        capture_output=True,
    )

    target = DONE if proc.returncode == 0 else FAILED
    shutil.move(str(mission), str(target / mission.name))
    print(f"mission={mission.name} rc={proc.returncode} target={target}")
    if proc.stdout:
        print(proc.stdout[-500:])
    if proc.stderr:
        print(proc.stderr[-500:])
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="process only one mission and exit")
    parser.add_argument("--interval", type=int, default=60, help="loop interval seconds")
    args = parser.parse_args()

    if args.once:
        return process_one()

    while True:
        process_one()
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
