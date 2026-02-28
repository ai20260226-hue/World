# HF Space deployment (No local PC)

このフォルダは、HF Spaces上で以下を実現するための最小テンプレートです。

1. `app.py` でダッシュボード表示（queue/memory/artifacts）
2. `scripts/hf_space_worker.py` を別プロセスまたは定期トリガで実行

## 推奨構成

- **Space A (Worker Space)**
  - `scripts/hf_space_worker.py --interval 60` を実行
  - `tasks/inbox/*.json` を処理
- **Space B (Dashboard Space)**
  - `hf_space/app.py` を実行
  - 進捗と成果物を可視化

## 注意

- 無料枠は常時稼働保証なし
- そのため、1回処理を短く保ち再開可能にする
- 永続データはGitHub連携で保全する
