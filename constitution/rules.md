# Constitution Rules (Single Source of Truth)

## Non-negotiable Rules

1. **Human Approval First**
   - Any destructive or high-impact operation requires explicit human approval via GitHub issue comment `APPROVED:<operation-id>`.

2. **Whitelisted Commands Only**
   - Agents may execute only commands listed in their profile under `allowed_commands`.

3. **Scoped Workspace**
   - Agents must operate only inside their assigned workspace path.

4. **Full Auditability**
   - Each run must append a structured log to `logs/<agent-id>.jsonl`.

5. **Deterministic Artifacts**
   - Deliverables must be saved in `artifacts/<agent-id>/` with timestamp and mission ID.

6. **No Secret Exfiltration**
   - Secrets must never be committed to git, printed in logs, or posted in issues.

7. **Stop Conditions**
   - Abort loop on:
     - max steps reached,
     - approval missing for protected action,
     - repeated failure over threshold,
     - command outside whitelist.

## Governance

- Rule updates require pull request + repository owner approval.
- If this file conflicts with any agent config, this file wins.
