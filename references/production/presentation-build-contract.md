# プレゼンテーションの制作契約

最初の読者向けスライドを作る前に、この制作契約を整えます。利用分野に依存しない制作・同期の要件を扱い、専門分野のモジュールは根拠の構成規則や表示形式を追加できます。ただし、読みやすさ、来歴、原資料忠実性を弱めません。

## 制作対象と不変条件

制作の対象は、読者向けの各ページ、そのページのプロット行、視覚表現、根拠・原図素材、契約、レビュー記録です。マニフェストは計画と制作上の約束を記録するもので、実装が約束を満たした証拠ではありません。

- スライド生成前に[ストーリーライン・プロット](../presentation/storyline-plot.md)を作成・改訂します。各行の説明・案内の役割を定め、根拠を担う行には問い、適用範囲付きの主張、図の関係、次の問いを置き、現行プロットからマニフェストを導きます。配置中に物語を作りません。
- 根拠を担うサーベイ発表では、初回G4-Vの候補判断後、G5前に条件付きG4-Pレビューを行います。初めて発表可能になったとき、または中心の問い、節順序、主要主張、視覚経路が実質的に変わったときが対象です。`go`/`revise`/`narrow`/`stop` を最も早い影響行の修正へ反映し、`go` をG5・G6通過と扱いません。
- 各スライドに説明・案内上の役割を与え、根拠・考察・結論を担うページでは問いと主張を明確にします。目次・概観・参考文献は[文書機能](../writing/document-functions.md)に合う平易な見出しを使い、独自の知見や下端の主張を追加する必要はありません。任意の `rrm_focus` は探索、修正、読者向け翻訳、レビューを改善する場合だけ使います。意味を変える対象・操作・結果・境界は既存の主張・根拠・プロット参照から読み取れる形でも構いません。6属性の必須化や固定読順にはしません。
- 読者向けの主張の近くに、人が読める出典を置きます。完全な文献情報と監査用の位置指定は注記・監査資料にも置けます。
- 根拠ページでは、専門分野の意味が許す場合に「主張 → 根拠を担う表現 → 境界・不確実性」を示します。値の入った表、方法図、比較、式、地図、グラフ、原図を基本とし、再構成の採用は[原図の取得](figure-extraction.md)と[役割による許可](reconstruction-review.md#対象と役割による許可)に従います。大きな数値や空のカードは根拠を表しません。
- 自動フィット・自動縮小は使いません。文字を小さくする前に削除・分割します。余白は構図として使い、欠けた方法・結果・比較・境界の代わりにしません。
- WBS、RACI、監督者・実装担当・レビュー担当のラベル、検索の計測記録、内部ID、制作指示を読者向け表示へ出しません。
- 原図利用・再構成では、単位、条件、軸、比較対象、帰無的な結果、不確実性、限界を原資料から保持します。主要主張に選んだ候補原図はG4-Vで切り出して保持し、視覚形式を決める前に取得と採用判断を済ませます。

## G4-V・G4-P・G5の同期

G4-Vは原資料側の候補関係、位置、経路、来歴、忠実性を記録します。G4-Pは候補をプロット・主張へ結び、その中のG4-PD/VDDR注記に `claim_id`、`reader_visual_job`、`reader_layout_route`、`boundary_visibility`、`meaning_changing_fields_visible`、説明の進展への寄与を残します。解釈主張の本文を複製せず、主張を参照します。注記は `visual_id` をキーとし、任意で `plot_row_id` を持ちます。注記がある場合、G5は配置前にその内容を反映します。

`reader_layout_route` は配置だけの指定です。`reader` は通常の1枚、`dense` は意図的に密だが検査可能な1枚、`split` は一つの関係を分担する複数枚です。視覚表現の種類ではありません。密な配置で完全な出典位置を注記へ移せても、解釈を変える条件、分母、単位、比較対象、不確実性は読者向けに残します。G4-PDを第二の来歴台帳や公開判定条件にしません。

## 文章と図の役割

意味を担う説明・根拠・統合の視覚表現では、配置前に既存のプロット・レビュー注記または制作注記で、文章と図の役割を分けます。文章は前提、定義、原資料の表現、注意、解釈、限界を担います。図は本文だけでは得られない、検査可能な関係・観測を示します。本文を繰り返すだけなら、除去、保留、実際の役割変更、再設計を選びます。説明・根拠・統合の役割が残る対象を名目だけで再分類しません。

意味レビューでは、図内ラベル、軸、凡例、注釈、キャプション、出典は残して本文を隠し、図から何を観測できるかを述べます。次に図を隠し、本文の主張・注意・限界を述べます。前者が後者の言い換えだけなら、制作前にプロットか図を修正します。これは意味を確かめる補助手順で、マニフェストへの必須属性追加、OCR、画像と文章の類似度、物体数の公開判定にはしません。全スライドに図を要求するものでもありません。

G4-PとG6それぞれの確認対象・母集団・抽出範囲は[レビュー基準](../workflow/review-rubric.md)に従って宣言します。制作契約は、その確認結果を制作・再確認へ反映します。

## 不変条件・プロファイル・作業閾値

数値やスタイルの条件は、次の3種類を区別します。

| 条件の種類 | 意味 |
|---|---|
| 不変条件 | 可読性、見える来歴、原資料忠実性、隠れた文字なし、支持されない推論なし、自動フィットなし |
| プロファイルの既定 | 選んだ参照から得た白い面、暗い文字、一定のアクセント役割、見出しと本文の階層など |
| 作業閾値 | 会場、媒体、言語、読者、成果物に合わせて根拠付きで選ぶ下限・上限 |

投影向けには18ptを安全側の既定にできますが、全分野・全媒体の普遍則にはしません。`accent <= 35%`、意味を担う図の固定個数、単一文字サイズ、方法・結果・限界の固定3枚構成も、作業・プロファイルに応じた条件として理由を説明します。数値既定を緩める場合もアクセシビリティと投影時の安全性を保持します。

必要なら暗い本文、控えめな補助文字、一つのアクセントを使います。アクセントの意味は現在の注目点や警告などに定め、無表示のカテゴリ、状態、引用、箇条書き、装飾へ使い回しません。取得した原図は原図の色を保持できます。

## 視覚マニフェストと素材台帳

読者向けの各スライドに1行のTSVを作ります。主要な根拠ページはG4-Vの候補判断から導き、原図と再構成の選択を配置時へ先送りしません。原図を検討したが読者向けに使わない場合は、切り出しと具体的な不使用理由を監査用に保持し、意図的な判断と探索漏れを区別できるようにします。

マニフェストは、プロット、視覚契約、素材、レビューの正本から生成する制作ビューです。`section_id`、同じレビュー状態、素材パス、寸法など、既存情報から導出できる値を別の判断として手入力しません。意味上の必要性と、検証器が受渡し形式として要求する列の存在を分けて扱います。

共通マニフェストは一ページ一行を維持し、単一図の旧平坦形式と、任意の `visuals` 配列に複数の視覚使用を含める形式を受け付けます。同一ページの独立した原図は、各子に別の `visual_id`・`kind`・契約・出典を保持します。ページを重複行にせず、偽の複合契約へまとめたり、検査器の制約だけを理由に分割したりしません。一原図の複数パネルが同じ意味構造を示す場合は、原資料の関係を保つ一つの使用として扱えます。代表図だけ宣言して他の主張図を未検査にしません。

`visuals` は既存のページと視覚使用の包含関係を記述する条件付きの包絡で、独立台帳ではありません。TSVのセルにはJSON配列を記録します。親からの継承範囲、子による上書き、旧属性との混在の拒否、完全な一ページ二図のfixtureは[複数視覚使用の契約](evidence-visual-contract.md#一ページに複数の視覚使用を含める)に従います。図ごとの種類・経路・主張・出典・素材・状態は子へ置き、ページ数、数値宣言、文字サイズなどの観測は親ページを一回だけ集計します。

`split` ではページごとに異なる `slide_id` と使用ごとの `visual_id` を与え、共有する主張・関係をプロットで対応づけます。一つのプロット行で複数ページを扱う場合は、`slide_ids` と `visual_ids` に各使用を列挙できます。同じ `visual_id` を別の行や配列要素で使うと重複として拒否されます。原図や素材を再利用する場合も、物理素材と読者向け使用を区別します。

G4-Pの適用時は `T → B → Bottom → Figure → Next` のつながりを確認し、全予定スライドに短い `presenter_note` または明示的な `not_needed` を残します。これは話すための補助で、完全な原稿でも、読者が持ち帰る主張の代わりでもありません。

素材台帳を使う場合、契約・候補・素材・マニフェストを次の既存項目で主張とスライドへ結びます。列挙は対象間の対応を示すもので、新規の必須属性を追加するものではありません。

```text
視覚表現・契約: visual_id, slide_id, kind, claim_bearing, reader_role,
                  claim_ids[], source_ids[], source_visual_route, boundary, status,
                  semantic_status, fidelity_status, visual_review_status,
                  review{deterministic_status, semantic_status, fidelity_status},
                  contract_path
原図候補:         figure_id, source_id, work_id, locator, claim_ids[],
                  candidate_type, candidate_visual_relation, rights_basis,
                  license_status, source_visual_route, fidelity, decision,
                  decision_reason_code, source_cutout_asset_ids,
                  source_cutout_manifest_paths, source_scan_record_paths
素材:             asset_id, figure_id, source_id, locator, rights_basis,
                  license_status, acquisition_mode, crop_spec, fidelity,
                  transformation_history, asset_role, review_only,
                  derived_asset_id, derived_asset_path, visual_review_status,
                  visual_comparison_packet_path, source_cutout_created_at,
                  reconstruction_created_at, attribution_note
スライド:         slide_id, plot_version, plot_row_id, section_id, evidence_block_id,
                  source_pointer, source_visual_route, primary_visual_type, figure_id,
                  presenter_note, rrm_focus（任意）
```

`candidate_visual_relation` の採用時条件は[候補記録](figure-extraction.md#1-候補と採用判断の単位)に従います。機械契約の4種類 `table`、`diagram`、`chart`、`source_figure` と、`contract_path`、経路別の両側宣言、`visual_id`、任意の `generation_id` による参照の一致は[視覚表現の契約](evidence-visual-contract.md)に従います。装飾・案内専用の図形を主張用契約へ昇格させません。権利属性は[利用根拠の整理](figure-extraction.md#2-日本の学術サーベイでの利用根拠の整理)に従い、引用に対して一律に `license_status=cleared` を要求しません。

`slide_id` は `1`、`S1`、`slide-1` など、実物ページへ数値で一意に対応できる値にします。行順に依存する自由なラベルは使いません。旧平坦形式のマニフェスト項目は次の通りです。複数図形式では図単位の項目を任意の `visuals` 配列の各子へ置き、ページ単位の項目は親に残します。

```text
slide_id, plot_version, plot_row_id, section_id, evidence_block_id, visual_id, kind,
claim_bearing, contract_path, reader_role, boundary, status, narrative_job,
presenter_note, evidence_class, primary_visual_type, source_pointer,
source_visual_route, figure_id, source_ids, claim_ids, source_cutout_asset_ids,
source_cutout_manifest_paths, source_scan_record_paths, rights_basis,
derived_asset_id, derived_asset_path, decision_reason_code, attribution_note,
semantic_status, fidelity_status, visual_review_status, visual_comparison_packet_path,
source_cutout_created_at, reconstruction_created_at, citation_visible, numeric,
denominator_unit, aggregation_level, caveat_visible, min_body_pt,
protected_terms, internal_vocab_free
```

### 表示形式と根拠の分類

`source_visual_route` は原図に関する判断、`primary_visual_type` は最終表示形式です。原図候補を用いない独自表現でも図を持てるため、両者を同一視しません。経路とレビュー状態の制御語彙、原図なしの唯一の互換例外は[経路別契約](evidence-visual-contract.md#原図経路と条件付き属性)に従います。`inaccessible_source` は未解決の状態であり、原資料の報告として再構成を提示できません。

`primary_visual_type` の許可値は次の通りです。

```text
source_figure | reconstructed_figure | result_table | result_plot |
method_diagram | comparison | equation | boundary_map |
photo_or_screenshot | none
```

`none` は、表紙、概要、移行、参考文献、最終回答などで、そのページの役割に根拠が不要な場合だけ使います。`number_card`、`summary_card`、`colored_container`、`decorative_chain`、`placeholder` を根拠表現として使いません。

`evidence_class` には `evidence`、`synthesis`、`method`、`boundary`、`orientation`、`transition`、`reference`、`cover` などを使います。方法・結果・境界の順序は専門分野の根拠構成に合わせ、固定の3枚へ押し込みません。主要な根拠群では、方法・基盤、結果・比較、限界・境界を成果物内のどこかで探せるようにします。

`numeric=yes` は量的情報を示す場合だけです。[定量属性の定義](../research/evidence-model.md#定量的な根拠主張だけに用いる属性)に従い、その数量に適用する分子、分母、単位・尺度、集約水準、重複規則、日付、不確実性を保持します。平均や係数に分母を作らず、現行検証器が数値ページに求める `denominator_unit` 欄にも、適用する単位・尺度と分母の該当外を記せます。質的・概念的内容は `numeric=no` または `not applicable` とし、分母を作りません。表の軸・セル・向き・`axis_mirror` は[表契約](evidence-visual-contract.md#表tablecontract)の同じ宣言から読者表と監査行へ生成します。G5通過だけで読者向け注記や制作記録に最終G6判定を書きません。

## 実物に基づく公開前検査

1. マニフェスト構造を検証し、行数と実物ページ数を比較します。[視覚表現の契約](evidence-visual-contract.md#決定論的検査と意味レビュー)の構造検査を実物観測より先に実行します。
2. 生成したPPTXに `scripts/check_deck_quality.py` を実行し、取得可能なら取込・再書出しPPTXと納品PDFも確認します。厳格モードは `--plot` と `--review-record` を渡し、ローカル参照を読む場合は常に明示的な `--audit-root` を渡します。マニフェストを監査資料の隣に置くだけでは代替できません。レビュー記録のプロット・読者状態は公開条件ですが、検証器が確認するのは形式的な対象範囲と修正・再確認の形です。
3. 実際のオブジェクトと読者向け文字を観測させます。`citation_visible=yes` や `primary_visual_type=source_figure` の宣言だけでは通過できません。ページ上に物体があるという観測は、各図の存在・帰属・可読性を個別確認した証明ではありません。複数図ページでは全使用を読者レビューの対象へ列挙し、それぞれの要約・評価・留保・出典との対応を確認します。
4. 固定解像度で描画した成果物全体と、機械検査で指摘された全ページを確認します。描画ツール、閾値、アクセスできない表示面を記録します。
5. 作業・プロファイルに根拠付きの視覚物体数の下限がある場合だけ、`--min-observed-visuals` を渡します。物体の存在と根拠としての意味は別です。関係、方法、比較、結果、分布、境界を示すとレビューで確認した表現だけを意味あるものとして数えます。
6. 再構成した根拠表現は、適用する原図との比較と[再構成レビュー](reconstruction-review.md)を完了させます。整った描画やマニフェストは、原資料忠実性・帰属の比較に代わりません。
7. 厳格な公開検査では、原図の付随記録、走査記録、比較パケット、派生素材をローカル監査資料内へ置き、JSON内容、ID、パス、ハッシュ、状態を検証可能にします。URLは位置指定であり、レビュー可能なローカル記録の代用ではありません。

検証器は決定論的な欠陥を失敗として返し、ヒューリスティックな懸念や意味上の懸念はレビューへ渡します。検査と判断の境界は[検証方針](../workflow/verification.md)に従います。
