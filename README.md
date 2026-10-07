# 文献調査オーケストレーター

学術的な問いから文献調査、根拠の比較・統合、発表資料の構成と制作までを扱うスキルです。使い方は [SKILL.md](SKILL.md)、スライドの作例は [テンプレート集](assets/survey-slide-templates.html)を参照してください。

## 取得と環境準備

```sh
git clone --recurse-submodules https://github.com/minaph/survey-orchestrator.git
cd survey-orchestrator
devbox install
devbox run setup
devbox run check-env
```

すでにcloneしている場合は `git submodule update --init --recursive` で依存スキルを取得します。執筆・推敲には[evidence-based-writing](skills/evidence-based-writing/SKILL.md)、日本語描画の手順には、固定コミットの [japanese-font-rendering](skills/japanese-font-rendering/SKILL.md) を使います。

DevboxはPythonとPDF/PPTX検査に必要な依存を管理します。以降の評価ではCLIもこの環境内で起動します。フォントやOffice変換器、ブラウザ、CLI本体は用途に応じて用意してください。具体的なコマンドと対象範囲は[評価環境手順](docs/evaluation-environment.md)に記載しています。

## 配布ビルド

```sh
devbox run python scripts/package_release.py
devbox run python scripts/package_release.py --layout flat --output dist/survey-orchestrator-flat.zip
```

ZIPには本体、参照文書、作例、実行スクリプト、環境定義、日本語描画・執筆スキルのガイドを同梱します。展開先で利用する場合も環境準備が必要です。同梱範囲と依存コミットの確認は[配布手順](docs/packaging.md)を参照してください。

## 評価記録と限界

[単一スライド評価](evaluations/luna-single-slide/REPORT.md)、[構成能力評価](evaluations/luna-plot-study/REPORT.md)、[全体監査](evaluations/completion-review.md)に、実施内容・レビュー・未解決事項を保存しています。環境整備後の評価は再実行しておらず、過去の未合格や制作前の修正事項を合格へ読み替えていません。

公開リポジトリには評価報告、プロット、レビュー、生成成果、検証用の記録を含めます。取得論文のPDFと全文、提供された参考PDF、作業用の複製、CLI生ログは含めません。保存時のハッシュと出所の記録は残るため、記録が参照する全ファイルが公開リポジトリだけで揃うわけではありません。配布ZIPには評価記録自体を含めません。

## 文書の所在

`references/research/` は調査・モデリング、`presentation/` は構成・デザイン、`writing/` は執筆・語句・文書機能、`production/` は制作・図・表示検査、`workflow/` は調査遂行・レビューを扱います。環境導入と配布は `docs/`、改訂監査は `audit/`、評価記録は `evaluations/` に置きます。評価当時のsnapshotは当時の構成を保持します。
