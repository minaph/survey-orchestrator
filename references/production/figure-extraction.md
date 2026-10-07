# 原図候補の判断・取得・切り出し

この文書はG4-Vで使います。主張と根拠の位置が安定した後、視覚マニフェストや根拠スライドを設計する前に、原図候補を確認し、レビュー可能な原図切り出しを取得します。適切な候補原図がある場合、比較用の切り出しは省略できません。読者に原図を直接示すかは、その後の採用判断です。

再構成を許可するスライドの役割と意味忠実性の比較は[再構成のレビュー](reconstruction-review.md)、経路別属性、JSONパケット、ハッシュ、参照の一致は[視覚表現の契約](evidence-visual-contract.md)が定義します。取得できたことだけを再構成の許可とみなしません。

## 1. 候補と採用判断の単位

十分にアクセスでき、読者向けの主要主張を支える、選択済みの根拠用情報源を一つずつ確認します。図、表、方法図、結果グラフ、インターフェース、条件図などから、主張に関係する候補を選びます。選択した各候補に `figure_id` を与え、切り出しまたは領域描画した素材を根拠パケットに保持します。後で再構成を選ぶ場合も、この取得を先に行います。

候補がない場合は位置を添えた `no_useful_candidate`、アクセスできない場合は未解決の `inaccessible_source` を記録します。候補の走査を黙って省略しません。原図を保存しなかった判断と候補なしは区別します。スタイル分析だけに使う参照成果物（例：MIRUのスライド）は根拠用情報源ではないため、別途専門分野の根拠に使う場合を除き走査対象外です。

候補記録はスライド制作前に作ります。以下は既存項目の記録形であり、全項目を新たに必須化する一覧ではありません。

原図候補は、情報源・版・位置で特定する原資料側の対象です。採用前や不採用でも存在するため、確定した読者向け表現とは分けます。旧来の `visual_candidate` は、この候補と読者表現・契約を結ぶ合成ビューとして扱います。同じ項目を持つ独立台帳を追加せず、候補の記録と、採用後の主張・プロット・契約への参照から組み立てます。

同一ページに複数論文・複数原図を紹介する場合も、候補と採用した使用ごとに原図位置、切り出し、支持する主張、出典を対応づけます。同じ論文から選んだ別図も一律に一候補へまとめません。配置後の一覧や下部の文献順だけから図の所属を推測しません。制作マニフェストでは任意の `visuals` 配列へ各使用を含められるため、ページを分けることや偽の複合図化を取得条件にしません。[複数視覚使用の契約](evidence-visual-contract.md#一ページに複数の視覚使用を含める)を使い、候補台帳を増やさず既存の参照から生成します。

```text
figure_id, source_id, work_id, locator, caption_summary, claim_ids[],
candidate_type, candidate_visual_relation, source_version, access_status,
source_cutout_asset_ids, source_cutout_manifest_paths, source_scan_record_paths,
rights_basis, license_status, source_visual_route, fidelity,
decision, decision_reason_code
```

`candidate_visual_relation` は、意味を担う表現に採用する原図候補では必須で、それ以外の候補では任意です。これは原資料が示す関係であり、プロットの `figure_relation` や読者向けの `reader_visual_job` に置き換えません。候補を選ばない場合は既存のG4-V注記または候補なし走査記録へ残せます。

候補の `work_id` は、報告と研究の対応が一対一と確認済み、または図の位置から所属研究を確定できる場合に限り導出できます。一つの報告が複数研究を含む場合は、原図が属する研究を根拠付きで保持し、所属が未確定なら保留します。`source_id` だけから一つの研究を推定しません。

候補発見はまとめて進められますが、担当範囲内の選図・採用はページ担当者が判断し、監督者は全体との整合と公開時の確認を担います。中心命題が仕組みなら方法・構造図、出力品質なら同条件の結果図、用途なら利用場面図というように、候補が見せる関係で選びます。複数の適切な候補がある場合は、図と関連本文を読み、方法図の処理の流れと結果図の出力差などを比べて、中心命題を説明できる候補を選びます。

測定・設定、比較条件、結果の構造、不確実性、意味のある境界を検査できる候補を優先します。装飾的な著者写真、雑誌の枠、サーベイで既に説明する一般的な案内図を、存在するという理由だけで抽出しません。原図が適切で読めるなら直接利用を既定とし、必要な箇所の切り出しと近接した説明で原図を活かします。編集しやすさだけを再構成理由にしません。

採用時は[役割と経路の対応](reconstruction-review.md#役割と経路の対応)で原図利用と読者向け分類を判断し、[契約の6経路](evidence-visual-contract.md#原図経路と条件付き属性)へ記録します。原図の不使用・再構成を説明する最終理由は次の閉じた集合です。

| `decision_reason_code` | 判断の内容 |
|---|---|
| `layout_unreadable` | 意図した読む大きさで原図が密すぎる・判読できず、再構成で必要な関係を保存する |
| `no_source_figure` | 当該主張を表す原図がない。通常は `no_useful_candidate` と構造化走査記録を使う |
| `cross_source_comparison` | 複数資料の比較を単一原図で表せない。関連する全原図切り出しを保持する |
| `review_synthesis` | 原資料の報告結果ではなく、サーベイ独自の解釈・機序・分類・流れを明示する |

アクセス不能は候補なしではありません。`inaccessible_source` は保留状態として、スライドと監査記録に未解決であることを残します。再構成を原資料の報告として示す許可にはなりません。走査・アクセス記録は、実物の原図切り出しの来歴記録と区別します。

## 2. 日本の学術サーベイでの利用根拠の整理

ここでは既存の運用方針を記録し、法的見解を新たに判定しません。作業設定・機関方針で適切な学術的引用その他の利用経路が確認済みの場合は、その根拠を一度記録して図の選択へ進みます。出版社のライセンス探索を毎回の一律の阻害条件にしません。文化庁資料が説明する著作権法第32条の引用、第48条の出所明示、または作業で確立した別の根拠を、適用する利用経路として記録します。

サーベイ自身の論証を主とし、当該研究の根拠を説明・比較・批評するために限定的な原図を出典付きで使う場合、既に確認された引用経路を公開判断の入力として扱います。具体的な制限、出典の同一性の不明、第三者権利、装飾目的への転用、過大な使用量、意味の歪曲がある場合だけ、追加判断へ回します。原図を常に再構成して権利問題を回避する運用にはしません。

`rights_basis` には実際に依拠する経路を記録します。例は `article32_quotation`、`open_licence`、`permission`、`public_domain`、`reconstruction`、`unclear` です。`license_status` はライセンスを根拠とする場合の条件付き情報であり、第32条の引用経路では `not_applicable` とします。「オープンライセンスが見つからない」を「利用禁止」と同一視しません。著者・年とDOI/URLまたは同等の短い出典を図のそばに見える形で置きます。

原文での公式資料確認日：2026-08-09。これは過去の確認記録であり、この改訂で再確認したことを示しません。

- 文化庁「他人の著作物を利用したい場合など」：https://www.bunka.go.jp/seisaku/chosakuken/seidokaisetsu/chosakukensha_fumei/
- 文化庁「文化芸術活動に関する法的問題についてよくあるご質問」（著作権法第32条・第48条の説明）：https://www.bunka.go.jp/seisaku/bunka_gyosei/kibankyoka/faq/

## 3. 素材の選択と属性

1. ページのスクリーンショットより、出版社・リポジトリの原画像や高解像度素材を優先します。論文の版、図番号・ページ、キャプション、主張との対応を確認し、確立済みの利用根拠を記録します。
2. 無関係な余白・隣接パネルは切り出せますが、見かけの方向、尺度、比較対象、不確実性、ラベル、意味を変えません。密な図を意味を変えずに読める状態にできない場合は、役割と検証負担を確認して原図・文章・表・図なしも比較します。再構成を自動的な解決策にしません。
3. JSON付随記録または素材台帳に、次の条件に応じて属性を残します。科学的・法的判断をスクリプトへ委ねません。

| 属性の扱い | 記録内容 |
|---|---|
| 判明している場合に必要 | `figure_id`、`source_sha256`、`output_sha256`、取得時刻、原資料・図・ページ位置、出力寸法、MIME型、主張への参照、忠実性、変換履歴。比較専用なら `review_only` を指定 |
| 条件付き | `source_id`、`canonical_url_or_doi`、`retrieved_url`、`final_url`、変換ツール・版、ライセンス依拠時の `license_status` |
| 必要に応じて手動記入 | `rights_basis`、候補・採用判断、正規識別子、不使用理由、再利用より再構成を選ぶ編集判断 |

未確認の属性は `unknown` または `not provided` とし、作りません。全経路の `crop_spec` は同じJSON構造です。

```text
{"pdf_bbox_pt": [x0, y0, x1, y1] | null, "pixel_crop": [left, top, right, bottom] | null}
```

HTML抽出では `pdf_bbox_pt=null` とします。URL属性は `string | null` で、リダイレクトがない場合やローカル資料のURLを推測しません。ローカル入力は `local_source_path`、HTML画像は `local_image_path` を保持し、Web URL欄へ `file:///...` を入れません。

`--no-manifest` は探索専用です。レビュー・公開に使う原図切り出しには来歴の付随記録を保持します。主張を担う視覚表現へ採用する場合は `--visual-id <visual_id>` を渡し、その表現へ結びます。任意の `--generation-id <id>` を使う場合は、マニフェスト、契約、対応するレビュー記録と同じ値にします。

## 4. 原図と再構成素材の組合せ

再構成を選んだら派生素材を保持し、原図候補がある場合は原図切り出しとの対をレビュー資料に残します。原図なしの互換例外、候補なしの独自表現、時刻の順序は[経路別契約](evidence-visual-contract.md#原図経路と条件付き属性)に従います。原図があることは直接掲載を強制しませんが、再構成を選んだ場合は具体的な比較と帰属が必要です。

原図と派生図の対応（`visual_asset_pair`）は次の既存項目で表します。`reader_benefit` と `verification_cost` は任意で、採用時の便益と負担を残せます。

これは複数の原図素材と一つの派生素材の関係を表す論理ビューです。比較パケットと素材への参照で同じ対応を表せる場合は、別の手動レコードや識別子を作りません。保持・変更・追加解釈の判断は比較パケットを正本とし、読者用キャプションへ必要な範囲を要約します。

```text
source_cutout_asset_ids, derived_asset_id, derived_asset_path, claim_ids[],
source_figure_locator, decision_reason_code, preserved_relation,
changed_elements, added_interpretation, reader_benefit, verification_cost,
attribution_note, visual_review_status, visual_comparison_packet_path
```

派生素材について、原資料の値・関係を保存するのか、配置だけを変えるのか、資料間で正規化するのか、サーベイ独自解釈を加えるのかを説明します。原資料の報告と独自解釈を混同しない帰属注記を読者に見せます。対応原図の有無、文章・データ位置、全矢印・数値・ラベル・軸・凡例・注釈・主張セルは[再構成レビュー](reconstruction-review.md)で確認し、比較JSONの最小項目、付随記録のハッシュ、走査記録、監査ルート内の配置は[パケット契約](evidence-visual-contract.md#パケットと参照の検証)に従います。

## 5. HTMLからの取得

論文がPDFではなく記事ページとして公開されている場合に使います。

1. 正規の記事URLを保存または開きます。`<figure>`、`<img>`、`srcset`、`data-src` などの遅延読込属性を確認し、サムネイルより最大の原画像を選びます。キャプション、`alt`、図ID、画像URLは選択の手掛かりであり、科学的結果の同一性を保証しません。
2. 候補を列挙し、インデックスまたは一意のキャプション・図一致で一つを選び、取得後にピクセル座標で切り出します。要求URL、リダイレクト後URL、原画像ハッシュ、キャプション、変換履歴を保持します。
3. canvas、操作後の読込、利用可能な `<img>` がない場合は、許可されたブラウザ・書出し経路で元素材を取得するか、役割規則に沿って再構成を検討します。低解像度スクリーンショットへ黙って置き換えません。

```bash
python scripts/extract_source_figure.py html \
  --source https://example.org/article --list

python scripts/extract_source_figure.py html \
  --source https://example.org/article --match 'figure 2|fig2' \
  --source-id A02 --figure-id F-A02-02 --claim-id C07 \
  --rights-basis article32_quotation --fidelity-status pending \
  --crop 20,10,1180,760 --autocontrast \
  --output assets/author2024-fig2.png \
  --manifest audit/author2024-fig2.json
```

`--crop` は原画像の `left,top,right,bottom` です。範囲外なら座標を修正します。不十分な素材をスライド一杯にする目的で余白を補ったり拡大したりしません。

## 6. PDFおよびPDFへ変換できる資料からの取得

アクセスできる原資料がPDFの場合、またはスライド・文書をPDFへ書き出せる場合に使います。PPTX、DOCX、ODPなども同じページ描画・切り出し手順を使えます。編集可能な原ファイルを保持し、配置に影響する変換ツール・版を記録します。

1. G4-Vでキャプション検索と低解像度一覧画像から候補ページを探します。単独のラスター画像なら `pdfimages` またはPDFライブラリによる埋込画像抽出を優先し、合成・ベクトル・混合図ならラベルと線を保つ領域描画を使います。
2. 約200–300 DPIまたは同等のベクトル書出しを使います。補助スクリプトへページ番号とPDFポイントの矩形を渡します。PDF変換可能入力と、描画後のピクセル切り出しにも対応します。
3. 意図した投影・読む大きさで確認し、パネルラベル、軸、単位、凡例、不確実性、関連キャプションが欠けていないかを調べます。密すぎる場合の再構成は役割規則を満たす場合に限り、必要な関係と変換の開示を保持します。

```bash
python scripts/extract_source_figure.py pdf \
  --source paper.pdf --page 4 --bbox 36,42,576,390 --dpi 240 \
  --source-id A02 --figure-id F-A02-02 --claim-id C07 \
  --rights-basis article32_quotation --fidelity-status pending \
  --output assets/author2024-p4-fig2.png \
  --manifest audit/author2024-p4-fig2.json

# LibreOfficeがある場合、PPTX/DOCX/ODP入力を一時PDFへ変換します。
python scripts/extract_source_figure.py pdf \
  --source original-deck.pptx --page 7 --bbox 24,18,696,510 \
  --output assets/source-slide7.png
```

PDFの `--bbox` は左上原点のページポイントで `x0,y0,x1,y1`、`--crop` は任意の描画後ピクセル切り出しです。PDF領域指定 `--bbox` または `--crop` の少なくとも一方が必要で、全ページ画像を黙って原図として出力しません。補助スクリプトは科学的意味・法的状態を推定しません。変換した場合はそのツール・版をマニフェストに保持します。

## 7. 制作・監査への引継ぎ

取得・切り出しした視覚素材の記録項目は、判明済み・条件付きの区別を適用して保持します。

```text
asset_id, figure_id, source_id, claim_ids[], canonical_url_or_doi,
retrieved_url, final_url, source_sha256, figure_or_page_locator, asset_url,
acquisition_mode, rights_basis, license_status, retrieval_date, source_mime_type,
output_mime_type, crop_spec, output_dimensions, output_sha256, fidelity_status,
transformation_history, asset_role, review_only,
derived_asset_id, derived_asset_path, decision_reason_code, visual_review_status,
visual_comparison_packet_path, source_cutout_created_at,
reconstruction_created_at, attribution_note
```

`figure_id` を主張台帳とスライドの `source_pointer`・視覚マニフェストへ結びます。`source_scan_record_paths` は走査・アクセス試行、`source_cutout_manifest_paths` は実際の原図素材を指すため、置き換えません。画像はキャプション、方法、軸、条件、結果が支持する範囲の根拠として扱い、見た目だけから新しい効果を推論しません。

同じ素材の `asset_url` と `final_url` が同値なら、取得先を一度記録して出力先の欄へ生成します。異なる画像位置を表す場合だけ区別を残します。取得日時、寸法、ハッシュ、変換履歴なども、素材・取得記録の正本から生成し、台帳と付随記録へ二重に手入力しません。監査専用という `review_only` は使用時の役割であり、同じ物理素材を別の用途で読者に示せないという意味ではありません。

取得図が意味を担うのは、原資料に忠実な関係、方法、比較、結果、分布、境界を検査できる場合です。装飾切り出し、ページ全体の画像、関係を示さない出典行は制作契約の根拠表現を満たしません。再構成の派生素材は原図・比較パケットへ結び、誤りが原資料に由来するかサーベイの変換に由来するかを追跡できる状態で渡します。
