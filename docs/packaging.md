# スキルの配布用ZIP

リポジトリのルートで、Python 3.12環境からビルドします。ビルド自体はPython標準ライブラリとGitを使います。親の実行時ファイルはGit登録前でも対象にしますが、依存スキルは固定されたGitサブモジュールから取得します。環境の準備とチェッカーの依存関係は[環境手順](evaluation-environment.md)に従います。

```bash
git submodule update --init --recursive
python scripts/package_release.py
python scripts/package_release.py --layout flat --output dist/survey-orchestrator-flat.zip
```

通常のZIPには `survey-orchestrator/SKILL.md` が入り、`flat` では `SKILL.md` がZIP直下に入ります。利用先が要求する構造を選んでください。展開後のスキル内には `SKILL.md` が一つだけあり、参照資料は相対パスで読めます。子スキルの取得やGitは配布版の利用には必要ありません。チェッカーなどを実行する場合は、展開先で環境手順を実施します。Devbox、Python環境、フォントやレンダラーの実体をZIPへ埋め込むものではありません。ZIPの再ビルドは、Gitの固定版を検証できるリポジトリで行います。

## 同梱範囲と検証

`scripts/package_release.py` の明示した許可一覧にあるエントリーポイント、UIメタデータ、実行スクリプト、環境定義・ロック・依存一覧、参照文書と作例素材を同梱します。作例のPNGと来歴JSONを含みますが、提供PDF全体、評価用コーパス、評価出力・履歴、テスト、監査報告、作業用一時ファイル、Git情報、仮想環境、キャッシュ、隠しファイル・秘密情報用設定は含めません。許可一覧にない新しい実行スクリプトや素材が必要になったら一覧も更新してください。

同梱MarkdownのローカルリンクとHTMLの `src` / `href` の参照先がZIP内に存在すること、エントリーポイントが一つであることをビルド時に確認します。必要ファイルの欠落、リンクの未同梱、実行パスのシンボリックリンクでは失敗します。正常にZIPを作成し整合性を確認した後だけ出力を置換するため、検証や書込に失敗した場合は既存のZIPを保持します。ZIP内の時刻とファイル順序を固定し、同じ入力から同じアーカイブを作ります。

作例の来歴にある `tmp/MIRU2026_tutorial_share.pdf` は取得時の原本の所在記録です。配布版にはその原本を同梱せず、PNGと元の来歴記録を保持します。履歴上のパスを配布版で取得できるファイルへのリンクと解釈しないでください。原典未照合や利用範囲は[作例の説明](../references/presentation/survey-slide-templates.md)を参照します。

## 依存スキルの固定版と同梱

開発時は、日本語描画の[原本](../skills/japanese-font-rendering/SKILL.md)と執筆・推敲の[原本](../skills/evidence-based-writing/SKILL.md)を、それぞれ `skills/` のsubmoduleから参照します。ビルドでは親のGitインデックスが固定したコミットと子の `HEAD` が一致し、子に変更や未追跡ファイルがないことを確認します。依存先が未初期化、固定版が不一致、または子が変更済みの場合は失敗します。文脈ログを更新した場合は、依存側でコミットし、親の固定版を更新してからビルドしてください。

配布版では各子の `SKILL.md` を同じディレクトリの `GUIDE.md` に変え、YAML frontmatterのみを除去して手順本文を保持します。親の参照も `GUIDE.md` へ変換します。文脈別のレシピ、検証済み・未検証の区別、文脈ログ、アイコンを同梱し、独立したスキルとして探索される子のUIメタデータは含めません。元リポジトリと確認したコミットを 各子の `provenance.json` に記録し、機械固有の取得元パスやGit設定を配布版へ持ち込みません。

ZIPの選定、単一エントリーポイント、リンク検証、atomicな出力の構成は、`grade-informed-etd-decision-support` の `scripts/package_release.py` と `scripts/portable_content.py` を参考にしました。親の実行時ファイルの選定ではGitインデックスに依存せず、実行スクリプト・素材・環境定義も同梱するための許可一覧を使います。

`references/` は調査・発表の実行時に読む資料を用途別に収録します。環境と配布の手順は `docs/`、過去の検証は `audit/` と `evaluations/` に置きます。ZIPには利用に必要な環境・配布手順を明示して含め、開発監査・評価は含めません。
