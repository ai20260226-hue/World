# World: Zero-budget local AI operations templates

This repository provides a practical starter kit for:
- HF Spaces as a visibility/submission UI,
- local PC as the command runner,
- GitHub as instruction + memory + audit storage.

## Quickstart (single mission)

```bash
python3 runner/agent_runner.py \
  --config agents/company-A-research.json \
  --task tasks/mission_example.json
```

Outputs are created under:
- `memory/`
- `logs/`
- `artifacts/`

## Quickstart (continuous local loop)

```bash
python3 scripts/ops_loop.py --interval 30
```

- Watches `tasks/inbox/*.json`
- Moves processed tasks to `tasks/done/` or `tasks/failed/`

## Docs

- System design: `hf_spaces_zero_budget_blueprint.md`
- Japanese runbook: `docs/NEXT_STEPS_JA.md`
- Governance rules: `constitution/rules.md`
- Action plan (JA): `docs/NEXT_ACTION_PLAN_JA.md`


## No-PC mode (GitHub Actions)

If you do not have a usable PC, use the scheduled cloud worker:
- Workflow: `.github/workflows/cloud-mission-worker.yml`
- Runner script: `scripts/cloud_runner.py`
- Queue: `tasks/inbox/*.json`

See `docs/NO_PC_MODE_JA.md` for the Japanese setup guide.


## HF Spaces mode (replace local PC)

If you want to run without a local PC at all:
- Worker: `scripts/hf_space_worker.py`
- Dashboard app: `hf_space/app.py`
- Guide: `hf_space/README.md` and `docs/NO_PC_MODE_JA.md`


## Dispatch mission from GitHub

You can dispatch a new mission via:
- Workflow: `.github/workflows/mission-dispatch.yml`
- Script: `scripts/new_mission.py`
