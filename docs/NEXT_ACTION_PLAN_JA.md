# 次にどうすればいい？（実行順チェックリスト）

## 0. 目標

- ローカルPCなしで、HF + GitHubだけでミッション処理を回す。

## 1. まずGitHubだけで指示できる状態にする

1. Actionsタブで `Mission Dispatch (GitHub -> inbox)` を手動実行
2. `mission_id` と `command_1` を入力
3. `tasks/inbox/<mission_id>.json` が生成されることを確認

## 2. 処理エンジンを選ぶ

- A: GitHub Actions定期実行（すでに追加済み）
  - `.github/workflows/cloud-mission-worker.yml`
- B: HF Space Worker
  - `scripts/hf_space_worker.py --interval 60`

## 3. 成果を確認

- `tasks/done/` / `tasks/failed/`
- `artifacts/`
- `logs/`
- `memory/`

## 4. 次の拡張（優先度順）

1. `agents/` に2体目を追加
2. `scripts/hf_space_worker.py` を agent_id 指定対応に拡張
3. Dashboard (`hf_space/app.py`) に agent別表示を追加
4. 失敗ミッション自動再試行ルールを追加
