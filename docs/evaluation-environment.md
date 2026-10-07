# 評価・検査用の Devbox 環境

この環境は、今後の評価で PDF 検査の `fitz` 不足を避けるためのものです。
`fitz` の提供元は `PyMuPDF` です。別の `fitz` パッケージを追加しないでください。
過去の評価結果、ログ、実行用 snapshot はこのセットアップの対象外です。

## 初回セットアップ

プロジェクトルート、または配布 ZIP の展開先で実行します。Devbox と Nix、
パッケージ取得用のネットワーク接続が必要です。Nix の初回導入や共有キャッシュへの
書き込みには、実行環境によって許可が必要です。

```sh
devbox install
devbox run setup
devbox run check-env
```

`devbox.json` と `devbox.lock` が Python 3.12 を管理します。
`requirements.txt` が PyMuPDF、Pillow、python-pptx とその推移依存を固定します。
`setup` は Devbox の Python からローカルの `.venv` を作成し、依存を入れて
`pip check` を実行します。Python の plugin は無効化し、環境作成はこの明示的な
コマンドに集約しています。対応する wheel がないプラットフォームでは
インストールを失敗させ、予期しないソースビルドを避けます。

`.venv` ができると `devbox shell` と `devbox run` の開始時に有効になります。
通常のシステム Python から同じ検査を起動すると、この依存環境は使用されません。
リポジトリを移動した場合や Python のロックを更新した場合は、既存の `.venv` を
退避または削除してから `devbox run setup` を再実行してください。
`.devbox`、`.venv`、Python キャッシュ、配布用 `dist` はコミット・配布に含めません。

## 実行前の環境確認

```sh
devbox run check-env
devbox run test
```

`check-env` は一時ディレクトリで人工的な 1 ページ PDF を作成し、
PDF の読み取り、矩形領域の PNG 化、寸法・来歴 JSON の確認、PDF observer、
PPTX の作成と observer を実行します。一時生成物は終了時に削除します。
成功時には Python と依存バージョンを JSON で出力します。
これは依存環境のスモークテストであり、評価ケースの再実行や性能評価ではありません。
`test` はソースリポジトリの `tests/` の単体テストだけを実行します。
配布 ZIP には `tests/` を含めないため、ZIP 展開先では `check-env` を使ってください。
`test` は `tests/` のない展開先では失敗させ、0 件成功という誤解を避けます。

## 今後の評価への適用

CLI とそこから起動する検査プロセスにも環境を継承させるため、CLI 自体を
Devbox 内で起動してください。次の例は新しい評価を始める際の実行形です。
評価開始前に `check-env` の結果と以下のバージョンを新しい評価記録へ保存します。

```sh
devbox version
devbox run python --version
devbox run python -m pip freeze
devbox run -- codex exec '新しい評価の依頼文'
```

対話的に作業する場合も、セットアップ後に `devbox shell` を開き、そのシェル内で
CLI や検査を実行します。CLI 側で環境変数を消去したり、固定された別の Python を
選んだりする場合は継承されません。今後の runner を使う際は、評価に入る前に
その子プロセスでも `import fitz` が成功することを確認してください。
旧評価に保存された `runtime/runner.py`、snapshot、採点結果の書き換えは不要です。

```sh
devbox run python scripts/extract_source_figure.py pdf \
  --source paper.pdf --page 1 --bbox 40,60,240,160 \
  --output output/figure.png
devbox run python scripts/check_deck_quality.py --help
```

## 対象範囲と再現性

この環境が管理するのは既存の Python 検査・抽出スクリプトの依存です。
LibreOffice による Office 文書からの PDF 変換、ブラウザ、CLI 自体、
フォント、スライド作成ツールは別途用意します。Office 文書は事前に PDF 化して
から検査することもできます。フォントの扱いは [japanese-font-rendering](../skills/japanese-font-rendering/SKILL.md) を参照してください。
PDF/PPTX の読み取りが成功しても、別の変換エンジンやフォントによる見た目の
同一性までは保証しません。

Python の取得元は `devbox.lock`、Python パッケージは `requirements.txt` に固定します。
パッケージファイルの暗号学的ハッシュ固定は行っていません。環境更新時はこれらの
ファイルを変更し、`setup`、`check-env`、必要な単体テストを通してから採用してください。
過去の評価はその実行時の環境不足を含めた記録として保持します。
