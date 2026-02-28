# World: Zero-budget local AI operations templates

This repository now includes practical templates to run resumable local AI loops with:
- HF Spaces as a visibility/submission UI,
- local PC as command runner,
- GitHub as instruction + memory + audit store.

## Quickstart

```bash
python3 runner/agent_runner.py \
  --config agents/company-A-research.json \
  --task tasks/mission_example.json
```

Outputs are created under:
- `memory/`
- `logs/`
- `artifacts/`

See `hf_spaces_zero_budget_blueprint.md` for system design details.
