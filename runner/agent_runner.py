#!/usr/bin/env python3
"""Minimal local agent runner template for resumable short loops.

Usage:
  python runner/agent_runner.py --config agents/company-A-research.json --task tasks/mission_example.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shlex
import subprocess
from pathlib import Path


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_config(path: Path) -> dict:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml  # optional dependency
        except ModuleNotFoundError as exc:
            raise RuntimeError("YAML config requires PyYAML. Use JSON config or install pyyaml.") from exc
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    raise RuntimeError("Unsupported config format. Use .json or .yaml")


def save_json(path: Path, data: dict) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def append_jsonl(path: Path, item: dict) -> None:
    ensure_parent(path)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def is_allowed(cmd: str, allowed: list[str]) -> bool:
    if not cmd.strip():
        return False
    head = shlex.split(cmd)[0]
    return head in allowed


def run_command(cmd: str, cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(
        cmd,
        cwd=str(cwd),
        shell=True,
        text=True,
        capture_output=True,
        timeout=120,
    )
    return p.returncode, p.stdout[-2000:], p.stderr[-2000:]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--task", required=True)
    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    task = load_json(Path(args.task), default={})

    agent_id = cfg["agent_id"]
    workspace = Path(cfg["workspace"]).resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    memory_path = Path(cfg["memory"]["file"])
    log_path = Path(cfg["logs"]["file"])
    artifacts_dir = Path(cfg["artifacts_dir"])
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    loop_cfg = cfg["loop"]
    max_steps = int(loop_cfg["max_steps_per_run"])
    allowed = cfg["allowed_commands"]

    memory = load_json(memory_path, default={"step": 0, "last_task": None})

    commands = task.get("commands", [])
    mission_id = task.get("mission_id", "mission-unknown")

    executed = 0
    for raw_cmd in commands:
        if executed >= max_steps:
            break
        if not is_allowed(raw_cmd, allowed):
            append_jsonl(
                log_path,
                {
                    "ts": utc_now(),
                    "agent_id": agent_id,
                    "mission_id": mission_id,
                    "status": "blocked",
                    "reason": "command_not_whitelisted",
                    "command": raw_cmd,
                },
            )
            continue

        code, out, err = run_command(raw_cmd, workspace)
        executed += 1
        append_jsonl(
            log_path,
            {
                "ts": utc_now(),
                "agent_id": agent_id,
                "mission_id": mission_id,
                "status": "ok" if code == 0 else "error",
                "command": raw_cmd,
                "exit_code": code,
                "stdout_tail": out,
                "stderr_tail": err,
            },
        )

    memory["step"] = int(memory.get("step", 0)) + executed
    memory["last_task"] = mission_id
    memory["last_run_at"] = utc_now()
    save_json(memory_path, memory)

    report_path = artifacts_dir / f"{mission_id}-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    report_path.write_text(
        "\n".join(
            [
                f"# Mission Report: {mission_id}",
                f"- agent_id: {agent_id}",
                f"- executed_steps: {executed}",
                f"- memory_file: {memory_path}",
                f"- logs_file: {log_path}",
            ]
        ),
        encoding="utf-8",
    )

    print(f"done: {agent_id} mission={mission_id} steps={executed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
