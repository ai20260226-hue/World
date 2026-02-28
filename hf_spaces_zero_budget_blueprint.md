# HF Spaces無料枠で「ローカルAI群」を運用する実践設計（ゼロ予算向け）

## 1. 先に結論

- **無料枠のHF Spacesだけで「無限ループ・常時24/365稼働」は保証できない**（スリープ・停止・再起動の可能性）。
- ただし、
  - Spacesを**UI/成果物提出ポータル**として使い、
  - 実処理は**あなたのPC側エージェント**で行い、
  - 状態管理は**GitHub**に集約
  する構成なら、ゼロ予算で最も現実的に近づける。

## 2. 無料枠で「止まりにくく見せる」考え方

> 「無限ループ」ではなく、**ジョブ再開可能な短いループ**を繰り返す。

- 各AIは長時間ループではなく、1回あたり短い処理（例: 30秒〜3分）だけ実行。
- ループ状態（次にやること、途中結果、最終チェックポイント）をGitHubに保存。
- 停止しても次回起動時にチェックポイントから再開。

### ループの標準手順（全AI共通）

1. GitHubから自分宛タスク取得（Issue/JSON）
2. 直近メモリ読込（`memory/<agent-id>.json`）
3. 1ステップだけ実行
4. ログ・成果物を保存
5. 次ステップ予約（自己Issueまたはstate更新）
6. 終了（停止しても再開可能）

## 3. 「成果物提出場所」の作り方（おすすめ順）

### A. GitHub Releases / PR / Issue（最優先）

- 成果物を`artifacts/`に置いてPR提出
- 大きな成果はRelease Asset化
- 会話系結果はIssueコメント
- 利点: 履歴・差分・監査が強い

### B. HF Spaces（提出ポータルUI）

- Space上に提出一覧ページを作る
- GitHub APIから最新成果を読み出して表示
- 利点: あなたが確認しやすい

### C. Hugging Face Datasetリポジトリ（任意）

- JSONL/CSV/ログを時系列蓄積
- 利点: データ保管と再利用に向く

## 4. 推奨アーキテクチャ（無料重視）

- **HF Spaces**: 可視化・承認画面・提出物ビューア
- **ローカルPC**: 実際のコマンド実行、思考ループ
- **GitHub**: 指示、長期記憶、監査ログ、成果物保管

```text
You(指示)
  -> GitHub Issue
    -> ローカルAI Runner(PC)
      -> コマンド実行(許可リスト)
      -> 結果をGitHubへ(ログ/PR/Artifact)
    -> HF Space UIがGitHubから表示
```

## 5. 役割分担（国/財閥モデルを崩さずに実装）

- 国（あなた）: ルール策定・最終承認
- 省庁/財閥AI: 目標分解・配分提案（提案のみ）
- 会社/部署AI: 実行計画化
- 作業AI: 実行と報告

### 重要ルール

- 上位AIは**提案権のみ**、実行は下位AI+承認で実施。
- 全AIが共通で従う`constitution/rules.md`を単一の正本にする。
- ルール変更は必ずPR + あなた承認。

## 6. ローカルPCコマンド実行の最低安全策

- 許可コマンド方式（ホワイトリスト）
- 作業ディレクトリ固定
- 秘密情報は環境変数またはローカルvault
- 実行前後ログを必ず保存
- 危険コマンド拒否（削除系・権限変更系を厳格制限）

## 7. GitHubから指示する運用テンプレート

### Issueテンプレート（最小）

```md
# Mission
- target_agent: company-A-research
- objective: ○○の調査と提案
- deadline: 2026-03-01T12:00:00+09:00

# Constraints
- must_follow_rules: constitution/rules.md
- budget: 0
- allowed_tools: [shell, git, python]

# Output
- report_path: artifacts/company-A/report.md
- summary_comment: required
```

### AI側の完了定義

- 必須ファイル作成（report/log/state）
- Issueに要約コメント
- 失敗時は原因・再開手順を残す

## 8. 無料枠運用で現実的な期待値

- 「常時稼働」より「**停止前提で復元が速い**」が正解。
- 1体目を安定化してから複製する。
- 監査可能性（誰が何をしたか）が最優先。

## 9. 最初の3日で作るべき最小セット

1. GitHubリポジトリ骨格（`constitution/`, `agents/`, `memory/`, `logs/`, `artifacts/`）
2. 1体の作業AI Runner（ローカル）
3. Issue受信→実行→PR提出の1サイクル
4. HF Spaceに「提出一覧」画面
5. 停止後再開テスト（PC再起動を含む）

---

必要なら次に、上記構成をそのまま使える
- ディレクトリ雛形
- `rules.md`雛形
- AIランナーの疑似コード
- GitHub Actions最小例
をまとめて作成できる。

## 10. このリポジトリに追加した最小実装テンプレート

- `constitution/rules.md`: 全AI共通ルール（承認・監査・停止条件）
- `agents/company-A-research.json`: エージェント設定（許可コマンド、ループ、ログ先）
- `runner/agent_runner.py`: 短い再開可能ループの最小ランナー
- `tasks/mission_example.json`: ローカル実行用サンプルミッション
- `.github/ISSUE_TEMPLATE/mission.md`: GitHubから指示するためのIssueテンプレート
- `.github/workflows/validate-runner.yml`: テンプレート検証用の最小CI

### ローカル実行例

```bash
python runner/agent_runner.py \
  --config agents/company-A-research.json \
  --task tasks/mission_example.json
```

この実行で、`memory/`, `logs/`, `artifacts/` 配下に状態・ログ・レポートが生成される。

## 11. 「どうすればいい？」に対する最短アクション

1. `python3 runner/agent_runner.py --config agents/company-A-research.json --task tasks/mission_example.json` を実行して1体目を確認。
2. `python3 scripts/ops_loop.py --interval 30` を常駐実行し、`tasks/inbox/*.json` を順次処理。
3. 成果物は `artifacts/`、監査は `logs/`、状態は `memory/` で確認。
4. 2体目以降は `agents/*.json` を複製して役割・許可コマンドのみ変更。
5. HF Spaces は提出ポータルとして使い、実行はローカルPCに固定。


## 12. PCを使えない場合の代替（No-PC mode）

- GitHub Actionsのスケジュール実行を使い、`tasks/inbox/*.json` を定期処理する。
- 実行は `.github/workflows/cloud-mission-worker.yml` + `scripts/cloud_runner.py`。
- 1回で1ミッションずつ処理し、成功/失敗を `tasks/done|failed` に分類。
- この方式でも「無停止保証」はないが、停止前提の再開可能運用ができる。


## 13. ローカルPCの代わりにHFを使う構成

- **Worker Space**: `scripts/hf_space_worker.py` で `tasks/inbox` を短サイクル処理
- **Dashboard Space**: `hf_space/app.py` で進捗・成果物を可視化
- **GitHub**: タスク配布・長期記憶・監査ログの正本

この構成により、手元PCなしでも運用できる。
ただし無料枠のため停止は前提で、再開可能設計を維持する。
