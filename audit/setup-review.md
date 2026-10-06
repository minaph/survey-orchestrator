# 同梱ビルド・評価環境・公開準備の記録

## 依頼と対応範囲

ユーザーは、参照プロジェクトの同梱方式を踏まえたビルドスクリプト、DevboxによるPyMuPDFの導入、以降の評価での利用手順、作業完了後のコミットを依頼しました。その後、配置された `japanese-font-rendering` のGit初期化、本体へのsubmodule登録と同梱、両リポジトリの `minaph` 配下へのpublic公開を追加しました。過去の評価の再実行は不要との指定を保持しています。

実装は独立コンテキストのGPT-6.1 Sol / high Subworkerへ、同梱ビルド、Devbox環境、依存リポジトリと公開対象整理に分けて委任しました。親は依存関係の判断、統合、利用者向け文書、検証結果の確認と公開判断を担当します。

## 実装と検証

| 対象 | 実施と結果 |
| --- | --- |
| 依存スキル | 原本5ファイルを変更せずGit初期化・コミット。`59f6a6e53e42e79a456542955c3a7292017cbd32` を `skills/japanese-font-rendering` のgitlinkに固定 |
| 配布ビルド | 通常版と直下版を生成。各59ファイル、約3.65MB。子の固定コミット・clean状態、ローカル参照閉包、ZIP整合性、単一SKILLエントリーポイントを確認 |
| 原本の保持 | 子SKILLをGUIDEへ改名しfrontmatterを除いた本文、参照資料、アイコンが原本と一致。来歴JSONに公開先とコミットを保存 |
| 配布物の利用 | 展開後の主要6 CLIの `--help` が両形式で成功。再ビルドにはsubmoduleを取得したGitリポジトリが必要 |
| Devbox | `init`、Python追加、`install`、`setup` を実施。macOS 15.6 arm64、Devbox 0.18.0、Nix 2.28.1、Python 3.12.14で確認 |
| Python依存 | PyMuPDF 1.26.7、Pillow 12.0.0、python-pptx 1.0.2、lxml 6.0.2、typing_extensions 4.15.0、XlsxWriter 3.2.9。`pip check` 正常 |
| 新規環境 | 初回ensurepipが一度失敗した後、作成したvenvを退避し、`devbox run setup` だけで新規作成できることを確認 |
| スモーク確認 | 新しい人工PDF/PPTXで生成・読込・画像化・切り抜き・来歴・observer確認に成功。Devboxから起動したPython子プロセスも `.venv` を使い `fitz` を読み込めた |
| 単体テスト | `devbox run test` で77件成功。うち同梱ビルドの11件は依存欠落・変更・固定版不一致・書込失敗時の保護も確認 |

python-pptxを実際に導入すると、以前の最小PPTX fixtureにOPC情報が不足していることが判明しました。元の担当Subworkerに差し戻し、有効な最小PPTXへ修正しました。検査処理をmockして失敗を隠す変更は行っていません。

## 公開範囲と保持する限界

公開Gitにはスキル本体、依存のgitlink、ビルド・環境定義、テスト、監査、評価報告・プロット・レビュー・生成成果を含めます。取得原論文と全文、提供PDF、作業用複製、CLI生ログは `.gitignore` で除外し、ローカルでは保持します。READMEに、公開記録が参照する全入力・ログが公開リポジトリだけで揃うわけではないことを記載しました。配布ZIPには評価記録を含めません。

今回の動作確認は環境とビルドを対象とし、Luna評価、匿名比較、構成評価、旧Case 1の正式検査は再実行していません。過去の失敗を合格へ変更していません。Run 1・3の制作前の図案修正と、改訂版の初回品質が未実証であることも維持します。他OS・CPU、Office変換器、フォント自体の導入や表示品質全般の認定は今回の確認範囲に含めません。

独立Reviewerには依頼文を引用し、mainへのマージ可否、本番での利用への影響、文書と運用の矛盾を厳しく確認するよう依頼しました。指摘と承認範囲は[独立レビュー](setup-release-independent-review.md)に保存します。

## レビュー対応と終了判断

Reviewerは関連25単体テストと人工PDF/PPTXの環境チェックを独立実行し、すべて成功しました。ブロッキング指摘はなく、非阻害のP3として配布手順の「Gitインデックスに依存しない」という説明の範囲を指摘しました。親はこの指摘を採用し、元のSubworkerが「親の実行時ファイルの選定」に限定しました。今回、不採用とした過剰要求はありません。

文言修正後、親がDevboxから両ZIPを再生成し、Reviewerは各59ファイルが現ソースの選定結果と完全一致することを再確認しました。依存原本の保持、固定コミット、リンク、ZIP整合性の確認と、環境の実動作を根拠に、今回のセットアップ・配布手順についてマージと本番利用を承認しました。親もこの範囲で実装完了と判断しました。

公開に先立つ保全確認では、作業開始時に記録した既存評価・作例・提供PDFの626ファイルをSHA-256で照合し、変更・欠落は0件でした。公開対象から除外した原本や生ログも削除していません。公開の完了は、リポジトリのvisibility、pushしたコミット、公開先からのsubmodule取得を別途確認して判断します。

## 公開後の確認

権限昇格した `gh repo create --public --source ... --push` により、`minaph/japanese-font-rendering` と `minaph/survey-orchestrator` を作成・公開しました。`gh repo view` で両方の `visibility=PUBLIC` と `defaultBranchRef=main` を確認し、`git ls-remote` で公開コミットを照合しました。

| リポジトリ | 公開確認したコミット | 内容 |
| --- | --- | --- |
| `minaph/japanese-font-rendering` | `59f6a6e53e42e79a456542955c3a7292017cbd32` | 原本5ファイルの初期コミット |
| `minaph/survey-orchestrator` | `00c491c` | スキル本体・同梱ビルド・Devbox環境 |
| `minaph/survey-orchestrator` | `6e569097f24e2031b1c0a18304a921316f3633f4` | 評価成果・監査記録の追加。公開cloneの確認対象 |

公開URLから別ディレクトリへ `git clone --recurse-submodules` を実行し、固定した依存コミットを取得できました。そのcloneから両ZIPをビルドし、Devbox環境で作成したレビュー済みZIPとバイト単位で一致することをSHA-256で確認しました。

| ZIP | SHA-256 |
| --- | --- |
| `survey-orchestrator.zip` | `404c000e091303c69c4328954495ccaaf67ceb35bac3a16a31ffd6398dce5693` |
| `survey-orchestrator-flat.zip` | `a5d029a1c811d71e40314b3c81f928a45b4ff3402a78e5e8d993c5ba56610572` |

この公開確認記録を最後の文書コミットとして追加します。実行用ファイルと依存コミットには変更を加えないため、確認したZIPの内容も維持されます。両publicリポジトリの存在、公開コミットの取得、submoduleの再現、配布ビルドの一致を根拠に、今回の公開作業を完了と判断しました。
