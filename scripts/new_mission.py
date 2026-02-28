#!/usr/bin/env python3
"""Create a mission JSON in tasks/inbox quickly.

Example:
  python3 scripts/new_mission.py \
    --mission-id companyA-003 \
    --command "pwd" \
    --command "echo hello"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mission-id", required=True)
    parser.add_argument("--command", action="append", required=True)
    parser.add_argument("--output-dir", default="tasks/inbox")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.mission_id}.json"

    payload = {
        "mission_id": args.mission_id,
        "commands": args.command,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
