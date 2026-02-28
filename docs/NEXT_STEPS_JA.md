# どうすればいい？（最短実行手順）

このリポジトリは「無料枠HF Spaces + ローカルPC実行 + GitHub保存」の型を作るためのテンプレートです。

## 1) まず1体を安定運用する

```bash
python3 runner/agent_runner.py \
  --config agents/company-A-research.json \
  --task tasks/mission_example.json
```

- 成功したら `memory/`, `logs/`, `artifacts/` に出力されます。

## 2) 擬似24時間ループをローカルで動かす

```bash
python3 scripts/ops_loop.py --interval 30
```

- `tasks/inbox/*.json` を自動処理
- 成功: `tasks/done/`、失敗: `tasks/failed/` に移動
- 実行ログは `logs/ops_loop.log`

## 3) 指示ファイルを追加して運用する

例: `tasks/inbox/companyA-002.json`

```json
{
  "mission_id": "companyA-002",
  "commands": [
    "pwd",
    "echo hello",
    "python3 -V"
  ]
}
```

## 4) HF Spacesは提出ポータルに限定する

- 無料枠で「無停止稼働」を狙わない
- Spaceは成果物一覧の表示（GitHub API読み出し）に使う
- 実行はローカルPC側に集約

## 5) 次にやること（優先順位）

1. `agents/` に2体目・3体目の設定JSONを作る
2. ミッション配布ルールを決める（どのagentがどのtaskを取るか）
3. GitHub Issueから `tasks/inbox/` へ変換する小スクリプトを追加
4. 失敗時リトライと人間承認フローを強化


## PCがない場合

`docs/NO_PC_MODE_JA.md` の手順で、GitHub Actions定期実行に切り替えてください。
