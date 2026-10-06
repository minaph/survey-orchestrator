# 主張を担う視覚表現の契約

この文書は、読者向けの主張を担う視覚表現について、識別子、意味、来歴、条件付き属性、参照の一致を定義します。装飾背景、節の案内、箇条書き、監査用の補助画像など、主張を担わない対象は4種類の意味検証から除外します。ただし、監査資料に含めるファイルの参照は有効でなければなりません。

候補の探索・採用・抽出は[原図の取得](figure-extraction.md)、スライドの役割による許可と要素単位の意味忠実性は[再構成のレビュー](reconstruction-review.md)、制作物と記録の同期は[制作契約](presentation-build-contract.md)を参照してください。機械検証の通過と意味上の妥当性は、別々に確認します。

## 対象単位と関係

契約は、`visual_id` で識別する一つの視覚表現と、その使用先の `slide_id` で識別する読者向けページに対応します。一ページに独立した複数の原図を置く場合も、各使用は別の契約を持ちます。主張・情報源・素材・レビュー記録を明示的な参照で結びます。

`figure_id` は原資料の図、`asset_id` は取得・生成した素材とその版、`visual_id` は読者向けの使用、`slide_id` は成果物のページを識別します。同じ原図を別の領域で切り出す場合や、同じ素材を別ページの主張に使う場合も、これらを一つの対象とみなしません。以下の機械必須条件は、この発表用契約と検証器を適用する場合の受渡し条件であり、装飾や非発表の調査に全属性を要求するモデルではありません。

```text
主張 -> 表現形式ごとの契約 -> 読者向け素材 + 監査記録
     -> 決定論的検査 -> 意味・原資料忠実性のレビュー -> 公開状態
```

共通部分は同一性、主張と情報源の参照、適用範囲、帰属、原図経路、レビュー状態を記録し、`semantics` は表現形式固有の意味を記録します。表をグラフへ変換したり、引用図へ表のセル構造を強制したりしません。

| `kind` | 検証する意味 |
|---|---|
| `table` | 行・列・セルの意味、行と列の全組合せ |
| `diagram` | ノード、辺、関係、方向、読む順序、凡例 |
| `chart` | 軸、単位、比較対象、集約、不確実性、数値範囲 |
| `source_figure` | 引用図または忠実な再構成の出典位置、原図切り出し、帰属、忠実性 |

主張IDがあるのに種類がこの集合に含まれない場合は、契約の明示的な拡張を検討するために止めます。未対応の種類を装飾扱いして検証を回避してはいけません。`claim_bearing=false` と明示した対象は意味検証の対象外です。

読者が検査する操作、比較・結果、境界の選択には[RRM](rrm.md)を使い、既存のプロット・レビュー注記または任意の `rrm_focus` に残します。RRMの6要素を必須スキーマにしません。G4-Vの原資料側の候補関係と、G4-P/G4-PDの読者側の役割も区別します。

## 共通属性と記録例

以下は共通構造を示す記録例です。`semantics` と経路別属性を未記入のため、このまま公開検証へ渡せる完成契約ではありません。

```json
{
  "visual_id": "V-01",
  "slide_id": "slide-1",
  "kind": "table",
  "claim_bearing": true,
  "reader_role": "資料間の比較",
  "claim_ids": ["C-01"],
  "source_ids": ["S-01"],
  "source_visual_route": "source_figure",
  "attribution": "著者（2024）、表2",
  "boundary": "観測した標本に限る",
  "uncertainty": "原資料に記載なし",
  "status": "SOURCE-REPORTED",
  "review": {
    "deterministic_status": "pending",
    "semantic_status": "pending",
    "fidelity_status": "not_required"
  },
  "contract_path": "contracts/V-01.json",
  "semantics": {}
}
```

`visual_id` と `slide_id` は空でない文字列です。真偽値、配列、オブジェクト、暗黙の文字列化を参照キーに使いません。`claim_ids` と `source_ids` は空でない文字列の配列です。新しい説明用の視覚表現で `source_ids` を空にできるのは、経路と走査記録がその理由を説明する場合だけです。`reader_role`、`boundary`、内容・来歴を表す `status` は空でない文字列を必須とします。`status` は公開判定ではなく、`review` の代用になりません。

主張を担うマニフェストの各視覚使用には `contract_path` が必要です。ただし、CLIで単一の契約ファイルを明示する代替指定は使えます。その場合も契約の識別子は対象の使用と一致させます。経路に応じた `figure_id`、`rights_basis`、原図ID・パス、走査・アクセス記録、派生素材ID・パス、理由、帰属、比較パケット、時刻は、マニフェストと契約の双方へ宣言して一致させます。無関係な台帳記録で不足を補完しません。適用しない項目は明示的な空配列、または後述の経路規則が任意とする箇所での省略を使います。

同じ意味・対象・版の値は正本で一度記録し、マニフェスト・契約・付随記録・パケットへ機械的に生成・同期します。照合用の複製を、それぞれ独立した判断として手入力しません。契約内部の自己参照 `contract_path` は検証器が必須としておらず、新たに記入する必要はありません。

原図切り出し、走査・アクセス記録、比較パケットは視覚表現単位です。参照するJSON自体に同じ `visual_id` を記録します。集合ファイルは、該当する記録がちょうど1件だけの場合に使えます。他の視覚表現の記録を混在させません。任意の `generation_id` を使う場合は、マニフェスト、契約、参照記録で一致させます。

検証器はJSONマニフェストとTSV/CSVを受け付けます。表形式入力の真偽値項目のみ、文字列 `true`/`false` と正確な `yes`/`no`/`1`/`0` を解釈します。意味ラベルや読む順序は実際のJSON配列として記述します。TSV/CSVの余分な列は無視せず、不正入力とします。

### 一ページに複数の視覚使用を含める

単一図の旧平坦形式は維持します。複数図を同一ページで扱う場合は、任意の `visuals` に既存の視覚使用レコードを配列として含めます。これはページと視覚使用の包含関係を渡す条件付きの包絡であり、独立した概念、必須台帳、新しい契約種別ではありません。JSONでは `slides` または `rows` 配下のページに配列を置き、TSVでは一ページ一行を保って `visuals` セルにJSON配列を記録します。空セルは旧形式、宣言した配列は一つ以上のオブジェクトを含めます。

親ページが保持するのは `slide_id`、`plot_version`、`plot_row_id`、`section_id`、`evidence_block_id` と、ページ単位の説明・観測属性です。後者は `narrative_job`、`evidence_class`、`presenter_note`、`citation_visible`、`numeric`、`denominator_unit`、`aggregation_level`、`caveat_visible`、`min_body_pt`、`protected_terms`、`internal_vocab_free` です。検査ビューへ継承するのはこの範囲だけです。子が同じ値を明記することはできますが、異なる値への上書き、親にないページ属性の追加、さらに内側の `visuals` は拒否します。契約ファイル自身の `slide_id` は引き続き必要です。

`visual_id`、`kind`、`claim_bearing`、契約参照、主張・情報源・素材・原図経路・レビュー状態は各子に置きます。成果物観測に使う `primary_visual_type` と `source_pointer` も各子が保持します。新形式ではこれらの旧平坦属性を親へ同時宣言しません。親の代表図や出典から他の図を補完せず、各図の支持対応を独立に検査します。宣言が混在する場合、子を優先して黙って上書きするのではなく曖昧な入力として拒否します。

全ての子を既存の経路・素材・契約検査へ渡し、プロットの `visual_ids`・主張・出典参照で全使用を覆います。読者レビューでは、複数図ページを対象にしたとき、そのページの全 `visual_id` を `reader_review.scope.items` に含めます。全件レビューでは全ページ、抽出レビューでは対象ページ内の全図を確認します。図の個数や論文の個数を新しい品質閾値にはしません。

複数図形式に再構成が含まれる場合、成果物観測では各子の `attribution_note` がページ本文に現れることを照合します。一つの一般的な再構成ラベルを別図の注記へ流用しません。この文字列照合だけでは注記と図の位置関係は分からないため、対応する図の近くにあるかは読者レビューで確認します。単一図の旧形式では従来の帰属検出を維持します。

最小の完全な検査用例は `tests/test_multi_visual_manifest.py` の `two_figure_fixture` です。一ページ二図のJSON・TSV、別々の契約と原図付随記録、主張・出典台帳、プロット、レビュー記録、PPTXパーサ用fixtureを一緒に生成します。二つとも検査し、ページ集計は一つのままであることを確認できます。これは架空の科学的結論を含まない検査用データで、描画された発表資料の品質例ではありません。

```bash
python3 -m unittest discover -s tests -p 'test_multi_visual_manifest.py'
```

## レビュー状態と情報状態

契約の `review` は必須で、`deterministic_status`、`semantic_status`、`fidelity_status` を持ちます。マニフェストの平坦な `semantic_status`、`fidelity_status`、`visual_review_status` は参照照合用であり、宣言した意味・忠実性の値は契約内の値と一致させます。

| 属性 | 記録する判断 |
|---|---|
| `deterministic_status` | 構造・型などの決定論的検査 |
| `semantic_status` | 表現自体の意味の妥当性 |
| `fidelity_status` | 原図や再構成に必要な原資料忠実性 |
| `visual_review_status` | G6での読者向け成果物または再構成のレビュー |

状態語彙は共通です。

```text
pending | passed | blocked | not_required | not_applicable
```

レビュー完了前は `pending`、不合格のレビューは `blocked` とします。`failed` は使いません。検証報告自体の失敗は `status=fail` です。`not_required` はその経路でレビューが不要な場合に限り、必要な原資料忠実性・再構成レビューを省略する指定ではありません。未確認と該当外を混同せず、未報告の科学的値は説明として明記します。G5の制作品質の `PASS` とG6の独立レビューを別々に記録し、一方の通過から他方を推定しません。

異なるレビュー責任・対象・時点の判断は区別して残します。例えば原図切り出しの忠実性と、派生図の忠実性は同じ判断ではありません。その記録から、現行検証器が照合する用途の状態を各欄へ反映します。同一判断の平坦な属性と `review` 内属性の複製は、別のレビューを増やすものではありません。

## 表現形式ごとの意味

### 表：TableContract

```json
{
  "row_axis": {
    "name": "研究",
    "meaning": "比較する研究または報告",
    "labels": ["A", "B"]
  },
  "column_axis": {
    "name": "条件",
    "meaning": "結果が報告された条件",
    "labels": ["対照", "課題"]
  },
  "cell_meaning": "報告された平均得点",
  "orientation": "行=研究; 列=条件",
  "axis_mirror": "rows = 比較する研究または報告; columns = 結果が報告された条件; cell = 報告された平均得点; orientation = 行=研究; 列=条件",
  "unit": "点",
  "cells": [[1.2, 1.5], [2.0, 2.4]]
}
```

`row_axis.name`、`row_axis.meaning`、`column_axis.name`、`column_axis.meaning` と、行・列の対応を説明する `orientation` は空でない文字列です。`axis_mirror` は同じ宣言から次の正確な形式で生成するレビュー用の照合文です。固定接頭辞は検証用なので変更しません。

```text
rows = <row_axis.meaning>; columns = <column_axis.meaning>; cell = <cell_meaning>; orientation = <orientation>
```

検証器はこの展開と与えられた照合文を比較します。読者表、監査行、レビュー用の照合文を同じ軸宣言から作り、宣言の科学的妥当性は意味レビューで確認します。`row_axis.labels` と `column_axis.labels` は空でない一意の文字列です。

`axis_mirror` は完全に導出できる生成結果であり、新しい意味判断項目ではありません。通常の `orientation` も同じ軸宣言から生成できます。転置などで読者の対応が変わる場合だけ、その違いを確認して宣言へ反映します。数値表の `unit` は意味の解釈に必要ですが、質的な比較表へ測定単位を作りません。現行検証器は全ての表に空でない `unit` を要求するため、量を表さない表では該当外であることを明記して受け渡します。

`cells` は `len(row_labels) * len(column_labels)` 個の位置を持つ完全な矩形行列です。各項目に文字列の `row` と `column` を宣言するセル集合も使えます。その場合も全組合せがそれぞれ1回だけ現れ、未知・重複の組合せを含めません。数値セルは有限数に限り、真偽値、NaN、無限大は禁止です。形状と参照の一致を検証しても、値の科学的真偽は確定しません。

意味レビューでは、各比較列のセルが同じ意味型かを確認します。測定計画、メタデータ、設計上の問い、限界は比較行列の外に置くか、未測定と明示します。

### 図式：DiagramContract

```json
{
  "nodes": [
    {"id": "n1", "label": "入力", "meaning": "初期状態"},
    {"id": "n2", "label": "出力", "meaning": "観測結果"}
  ],
  "edges": [
    {"from": "n1", "to": "n2", "relation": "temporal"}
  ],
  "reading_order": ["n1", "n2"],
  "legend": "実線矢印は時間的順序を表す"
}
```

ノードIDは一意の文字列で、辺の両端は宣言済みノードへ解決されなければなりません。辺は次の制御語彙から空でない関係を宣言します。

```text
causal | temporal | classification | reading_order | flow |
dependency | comparison | aggregation | other_explicit
```

矢印の形だけから関係を推定しません。`reading_order` は必須で、各ノードをちょうど1回ずつ指定します。色、線種、形、位置が意味を担う場合は凡例または軸・尺度を宣言し、凡例が必要な表現には凡例を付けます。宣言した解釈の妥当性は意味レビューで判断します。

この `reading_order` の必須性は現行検証器の条件です。手順図では読む順が意味を変えますが、順序を持たない対称比較図では科学的な全順序は不要です。その場合は読者の確認を助ける順として指定し、対象間の時間的・因果的順序を新たに主張しません。

### グラフ：ChartContract

```json
{
  "x_axis": {"name": "条件", "unit": "カテゴリ"},
  "y_axis": {"name": "得点", "unit": "点"},
  "comparator": "対照条件",
  "aggregation": "平均と95%信頼区間",
  "domain": {"type": "continuous", "min": 0, "max": 10},
  "uncertainty": "95%信頼区間"
}
```

主張を担うグラフは比較対象を宣言します。比較対象が該当しない場合も、説明を添えて `none_applicable` とします。連続・対数範囲の `min` と `max` は有限の数値スカラーで、`min < max` とします。配列・オブジェクトを数値境界にせず、対数範囲は両端を正にします。真偽値、NaN、無限大は禁止です。検証器は任意桁の整数を無条件に浮動小数点へ変換しないため、巨大整数も `OverflowError` ではなく構造化された検証結果になります。

### 原図：SourceFigureContract

原図記録には `figure_id`、`locator`、`rights_basis` と、原図・派生素材への参照を加えます。以下の経路別条件は機械検証用です。機械的に有効でも、文献紹介での再構成禁止、キャプション、由来、要素ごとの意味確認は[再構成のレビュー](reconstruction-review.md)に従います。

現行検証器は `source_figure` にも空でない `semantics` を要求しますが、その内部の形式固有の意味は検証せず、原図位置と経路・素材の条件を検査します。この欄の存在を意味の保証と扱いません。原図の意味忠実性は、出典・切り出しとの比較と人によるレビューで確かめます。

## 原図経路と条件付き属性

`source_visual_route` はG4-Vでの原図利用の決定です。読者に見せる種類 `kind` や、資料報告とサーベイ独自解釈の区別とは別に記録します。経路は次の6値から一つを選び、複数値を結合しません。

| 経路 | 必要な宣言・記録と制約 |
|---|---|
| `source_figure` | `figure_id`、原図切り出しとその参照、帰属、忠実性。一般的な `source_scan_record_paths` で代替せず、候補確認は図台帳と原図の付随記録に残す |
| `faithful_reconstruction` | 派生素材、許可理由、比較パケット、読者に見えるサーベイ制作の帰属。対応原図がある場合は原図切り出しを保持。原図なしの例外は後述 |
| `new_explanatory_visual` | 比較・根拠として実際に使用する候補原図、派生素材、比較パケット、帰属。理由は対応する `cross_source_comparison` または `review_synthesis`。`no_source_figure` は使えない |
| `no_useful_candidate` | 最終表現を形成する原図を用いない経路。`decision_reason_code=no_source_figure` と構造化走査記録が必要。原図切り出しID・パスをこの経路へ宣言しない。読者表現が独自統合でもこの経路を使える |
| `inaccessible_source` | 視覚表現ごとの構造化アクセス記録。未解決なので厳格な根拠公開検証を通過できない |
| `not_applicable` | 根拠を要しないページ向け。主張を担う視覚表現、および根拠・方法・境界・統合ページには使用不可 |

`faithful_reconstruction` と `new_explanatory_visual` は、派生素材ID・パス、比較パケット、`preserved_relation`、`changed_elements`、`added_interpretation`、帰属を宣言します。厳格な公開時は `visual_review_status=passed` とし、原図を伴う経路では忠実性も通過させます。原図が読みやすく適切な場合は `source_figure` を既定とし、編集しやすさだけを再構成の理由にしません。

原図を使わない独自の図式・グラフや、文章から作る表現は `no_useful_candidate` とします。原図候補を統合の比較・根拠に実際に使う場合は `new_explanatory_visual` とします。この意味上の対応は[役割と経路の対応](reconstruction-review.md#役割と経路の対応)で判断してください。

既存検証器が受け付ける、再構成における唯一の原図なし例外は次の組合せです。

```text
route=faithful_reconstruction
decision_reason_code=no_source_figure
source_scan_record_paths=<ローカルの構造化された候補なし記録>
source_cutout_asset_ids/source_cutout_manifest_paths=<空>
```

これは互換経路であり、文章由来の再構成や原図を用いない統合を忠実な原図再構成に分類し直す許可ではありません。この例外では既存検証器に合わせて `source_ids` を空にし、選択済み `figure_id`、存在しない原図の `rights_basis`、架空の切り出しを宣言しません。走査観測時刻を `reconstruction_created_at` 以前にします。原図が存在する場合は `source_cutout_created_at` を派生素材作成時刻以前にし、原図なしではその時刻を捏造しません。

## パケットと参照の検証

比較パケットの最小キーは `visual_id`、`source_cutout_asset_ids`、`derived_asset_id`、`claim_ids`、`decision_reason_code`、`visual_review_status`、`preserved_relation`、`changed_elements`、`added_interpretation` です。`generation_id`、`reader_benefit`、`verification_cost` は任意です。パケットはキャプションと要素対応表の代用になりません。

原図切り出しのJSON付随記録は `asset_role=source_cutout`、`review_only=true`、素材ID、原資料・図・主張への参照、原資料と出力のハッシュ、`source_hash_basis`、出力パスを宣言します。SHA-256は有効な64文字です。検証器は保存出力から `output_sha256` を再計算し、`source_snapshot_path`、`local_image_path`、`local_source_path` がある場合は原資料から `source_sha256` も再計算します。ローカルファイル由来ではパッケージ相対の原資料パス、リモート由来ではURL/DOIの位置指定を保持します。不正ハッシュ、解決不能パスを厳格モードで拒否します。

走査・アクセス記録は次のように区別します。いずれも同じ `visual_id`、`locator`、`observed_at` または `created_at` を含めます。

| 記録 | `record_type` | 記録内の経路と状態 | 追加の必須内容 |
|---|---|---|---|
| 候補なし走査 | `source_figure_scan` | `source_visual_route=no_useful_candidate`、`status=no_candidate` | 空でない `reason`、または同等の `summary`/`note` |
| アクセス試行 | `source_figure_access` | `source_visual_route=inaccessible_source`、`status=inaccessible` | 空でない `access_status` |

原図なしの互換経路でも、走査記録内の経路は走査結果を表す `no_useful_candidate` です。任意のJSONや対象を限定しない記録群を全ページの証拠として使いません。

```text
manifest.visual_id/slide_id
  -> contract.visual_id/slide_id
  -> contract.claim_ids -> ledger.claims[].claim_id
  -> contract.source_ids -> ledger.sources[].source_id
  -> 参照する素材ID/パス -> ledger.assets[].asset_id（存在する場合）
```

欠落、空値、不正形式、入力間の不一致は構造化された失敗になります。JSONはオブジェクト、または明示的に対応した配列形式である必要があります。付随記録、派生素材、契約、パケットなどのローカル参照を読む際は、非厳格の診断モードでも `--audit-root` を明示します。URLは出典位置であってローカル監査記録ではありません。`..` や解決後のパスによって監査ルート外へ出る参照は失敗とし、指定した監査資料の外を読み書きしません。

## 決定論的検査と意味レビュー

検証器は型、有限数値範囲、表の全組合せ、図式の端点・関係、経路条件、時刻、パス包含、宣言済みハッシュ、マニフェスト・台帳・契約の一致を検証します。関係の科学的妥当性、主張の重要性、再構成による意味保存は、意味・原資料忠実性レビューで判断します。

表は全て読者が読む大きさで確認し、行軸、列軸、セルの意味、向き、および少なくとも一つの代表的な行と列の組合せの解釈を `axis_mirror` と照合して記録します。`check_evidence_visual_contract.py` で構造を先に検証し、その後 `check_deck_quality.py` でPPTX/PDFの実物、可視の帰属、ページ対応、経路別パケットを観測します。宣言だけを観測証拠として扱いません。

```bash
python scripts/check_evidence_visual_contract.py \
  --manifest audit/visual_manifest.json \
  --ledger audit/evidence_ledger.json \
  --plot audit/storyline_plot.json \
  --audit-root audit \
  --strict
```

コマンドはJSON報告を出力し、厳格モードで決定論的な失敗がある場合は非ゼロ終了します。不正入力も、未処理のトレースバックではなく報告項目として返します。読者表、表の監査記録、契約、マニフェスト、制作記録、品質判定は同じ宣言・生成状態へ同期します。与えたID・ハッシュ・参照は確認しますが、プロジェクト固有のレビュー回次履歴を普遍的なスキーマ要件にはしません。
