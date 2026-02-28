#!/usr/bin/env python3
"""GitHub Actions向けの1回実行ランナー。

- tasks/inbox/*.json から1件だけ取得
- runner/agent_runner.py で処理
- 成功: tasks/done/ へ移動
- 失敗: tasks/failed/ へ移動

PC不要モードで、schedule実行と組み合わせる想定。
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


CONFIG = Path("agents/company-A-research.json")
INBOX = Path("tasks/inbox")
DONE = Path("tasks/done")
FAILED = Path("tasks/failed")


def main() -> int:
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


if __name__ == "__main__":
    raise SystemExit(main())
