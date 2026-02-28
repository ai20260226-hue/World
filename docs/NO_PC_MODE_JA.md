# PCなしモード（GitHub Actionsだけで回す）

使えるPCがない場合は、ローカル常駐の代わりに **GitHub Actionsの定期実行** で回します。

## 仕組み

- `.github/workflows/cloud-mission-worker.yml` が15分ごとに起動
- `scripts/cloud_runner.py` が `tasks/inbox/*.json` から1件処理
- 成功したら `tasks/done/`、失敗したら `tasks/failed/` に移動
- ログ/メモリ/成果物はリポジトリに保存

## 使い方

1. GitHubでこのリポジトリを用意
2. `tasks/inbox/` にミッションJSONを追加してpush
3. 15分以内（または手動でworkflow_dispatch）に処理される
4. `artifacts/`, `logs/`, `memory/`, `tasks/done|failed` を確認

## 注意

- GitHub Actions無料枠には実行時間上限があります
- 「完全な無停止」は保証されません
- ただし「停止しても次回で再開しやすい」構造になります


## HF Spacesを使う場合（ローカルPCの完全代替）

- Worker用Spaceで `scripts/hf_space_worker.py --interval 60` を動かす
- Dashboard用Spaceで `hf_space/app.py` を動かす
- タスク投入は `tasks/inbox/*.json` をGitHubにpush
- 実行結果は `artifacts/`, `logs/`, `memory/` に反映

詳細は `hf_space/README.md` を参照。
