---
name: Mission
about: Assign a mission to an agent
labels: [mission]
---

# Mission
- target_agent: company-A-research
- mission_id: companyA-scan-001
- objective: 調査してレポートを作成
- deadline: 2026-03-01T12:00:00+09:00

# Constraints
- must_follow_rules: constitution/rules.md
- budget: 0
- allowed_tools: [shell, git, python]

# Output
- report_path: artifacts/company-A-research/
- summary_comment: required
