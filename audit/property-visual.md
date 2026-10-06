# 図・素材・制作契約の項目別監査

対象は177監査行です。属性、包絡、既存の記録区分、自然言語で確認する観点を含みます。新しい必須項目を提案する表ではありません。監査全体の採否と限界は [総括](../PROPERTY_AUDIT.md) を参照してください。

「維持」は意味を保つ判断であり、全案件で独立列や独立レコードを必須にする意味ではありません。「削除候補」は独立した入力・正本を減らす判断です。既存値を失わず参照・導出・統合する方法を、重複・適用条件の欄に示します。現チェッカーの要求と意味上の必要性は別欄です。所在は監査時のファイルを示し、改訂で移動する行番号には依存しません。



## candidate / contract / manifest / sidecar

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `figure_id`<br>結合・運用 | 条件付き | どの原資料の図を採用・描き直したか | 切り出し違いと別原図を区別できない | source_idと版別locatorで自然キーを構成可能だがIDは結合用に有用 / 適用: 候補複数・再利用時に必要 | source_figureと原図あり再構成、sidecarで必須。候補台帳自体は未検査 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## candidate / sidecar / scan / access

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `source_id`<br>結合・運用 | 維持 | 候補・素材・走査がどの情報源に由来するか | 同じ図番号を別資料と混同する | 素材の出所として一度保存し用途側source_idsへ生成 / 適用: 情報源が特定できる場合に必要 | sidecar必須。scan/accessは視覚表現にsource_idsがある場合のみ必須 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## candidate

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `work_id`<br>結合・運用 | 条件付き | 候補原図がどの研究に属し、複数報告に再掲された同じ研究の図か | 一報告に複数研究がある場合の原図所属を追えず、研究単位の重複候補・支持を誤集計する | 報告と研究の対応が一対一と確認済み、または図の位置から所属研究が確定する場合だけ既存参照から導出できる。一報告複数研究では所属を根拠付きで保持し、複数候補・未確定なら保留する / 適用: 研究単位の図所属・重複・版間比較を判断する場合に必要。情報源だけでは所属が一意でない場合もある | 候補台帳のwork_idを検証しない | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[references/evidence-model.md](../references/evidence-model.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `locator`<br>保存 | 維持 | 候補のどのページ・図・範囲を採用するか | 図の同一性と主張の支持位置を再確認できない | source_id＋版＋locatorで自然識別。原図契約へ参照・生成 / 適用: 候補の位置を特定する場合に必要 | candidateのcaption_summaryは検査なし。契約locatorは原図kind/route時必須 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `caption_summary`<br>保存 | 条件付き | 候補のキャプションから何を読むべきか | 候補一覧で重要関係を短く選別できず原キャプションを読み直す | 原資料captionから要約可能。短い候補一覧が不要なら独立保存不要 / 適用: 候補一覧での短い選別が有用な場合だけ | 候補caption_summary自体は検査なし | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `candidate_type`<br>保存 | 条件付き | 表・グラフ・方法図等の候補の性質は何か | 候補探索を型で絞れないが採用理由は記述できる | 原図の識別情報・関係説明で足りる単一候補では別分類不要 / 適用: 複数候補の選別に寄与する場合のみ | 機械検査なし | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `candidate_visual_relation`<br>確認観点 / 保存 | 条件付き | 原資料側で何の関係を検査できるか | 見た目で候補を選び主張の支持範囲を見失う | 原資料の関係であり読者側reader_visual_jobとは統合不可。既存G4-V注記に一度保存可 / 適用: 意味を担う採用候補では必要 | この属性の存在・意味をcheckerは検査しない | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `source_version`<br>保存 | 統合・導出 | どの版の図を選び、ページ差をどう読むか | 改訂図と旧図を同一扱いする | 情報源の版情報を参照できれば候補への再記入は不要 / 適用: 複数版がある場合 | 機械検査なし | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `access_status`<br>確認観点 / 保存 | 条件付き | 候補探索に必要な原資料を見られたか | 候補なしと未アクセスを混同する | 探索時の状態。アクセス試行記録へ一度残して候補へ参照可能 / 適用: 未アクセス・一部アクセス時に必要 | candidate欄は検査なし。access recordでは空でない理由が必須 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `fidelity`<br>確認観点 | 統合・導出 | 切り出し・変換は必要な関係を保存するか | 候補採用前の忠実性懸念を失う | candidate.fidelityと最終fidelity_statusの対象・時点を明示する。確定判断を複製しない / 適用: 候補の変形・採否判断時 | この綴りの候補属性は検査なし | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `decision`<br>保存 | 条件付き | 候補を採用・不採用・保留としたか | 候補が発見されたことと採用したことを区別できない | 単に6経路を再掲するならsource_visual_routeから導出。候補ごとの採否は別に必要 / 適用: 複数候補・不採用時に必要 | 候補decisionは検査なし | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## contract / manifest / sidecar / packet / scan / access / element_map / G4-PD

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `visual_id`<br>結合・運用 | 維持 | どの読者表現の使用・レビュー記録か | 別スライドのパケットを流用する誤結合を検出できない | 意味として表示単位で保存し各資料には生成する。図候補IDや素材IDとは別 / 適用: 表示・レビューを複数扱う場合に必要 | EVC manifestは非主張も必須、重複不可。参照記録は必須 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/reconstruction-review.md](../references/reconstruction-review.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## contract / manifest / element_map / G4-PD

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `slide_id`<br>結合・運用 | 条件付き | 視覚表現は実物のどのページにあるか | 成果物のページと指摘が対応しない | assetや候補には不要。プロットから制作ビューへ生成できる / 適用: 発表・読者ページがある場合 | EVC manifest/contract必須。deckは数値形式とページ重複を検査 | [references/reconstruction-review.md](../references/reconstruction-review.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |

## contract / manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `kind`<br>保存 / 結合・運用 | 維持 | 表・図式・グラフ・原図のどの意味構造を検査するか | 型に応じた検証を選べない | primary_visual_typeとは粒度が異なる。source_figureは来歴、他3値は形式で分類軸に混在あり / 適用: 形式別の検査時に必要 | EVC非主張でも宣言必須、主張では4値限定。原図routeはkind=source_figureを要求 | [references/reconstruction-review.md](../references/reconstruction-review.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |
| `claim_bearing`<br>確認観点 | 維持 | この対象は根拠・説明を担い意味レビューが必要か | 装飾扱いで主張要素を検査から逃がす | claim_idsの有無から単純導出すると未登録主張を逃すため独立した分類確認に意義 / 適用: 対象範囲判定時必要 | manifest必須。claim_ids付きfalseは禁止、contract真偽値も必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |
| `reader_role`<br>保存 | 統合・導出 | 読者が図から何を理解・比較するか | 図の作成目的を意味レビューで再構成できない | G4-PD.reader_visual_jobと同じ役割なら正本から生成。文学紹介/独自統合という許可分類とは区別 / 適用: 読者役割が曖昧な場合に必要 | 主張manifest/contractは空でない一致値が必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## candidate / contract / manifest / pair / packet / sidecar

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `claim_ids`<br>結合・運用 | 維持 | 図・変換はどの主張を支えるか | 証拠の範囲を超えて別主張に利用する | 使用関係の正本に一度保存して各ビューへ投影。候補段階と最終用途の対応が変わる時は版を区別 / 適用: 主張を担う使用時に必要 | 主張manifest/contract必須。packetは集合一致、sidecarは主張集合の共通部分を要求 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## contract / manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `source_ids`<br>結合・運用 | 条件付き | 最終表現がどの情報源を根拠とするか（faithful原図なし互換例外では情報源を表示せず走査記録に依拠する） | 資料間比較の支持元が不明になる | claim→evidence→sourceから導出可能な場合も直接図由来と区別し正本用途関係から生成 / 適用: 根拠情報源がある場合に必要 | 経路で必須性変化。原図/原図あり再構成/未アクセスは非空、faithful原図なし例外では空を強制 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## candidate / contract / manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `source_visual_route`<br>保存 | 条件付き | 原図を使うか、再構成か、候補なし・未アクセスか | 原図の採用判断と探索未実施を混同する | 原図有無・採用理由と関係するが編集判断は単純導出不可。マニフェストと契約には生成 / 適用: G4-V対象で必要 | 主張manifest/contract必須一致、非主張EVCはskip、deckは6値を全ページ要求 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/reconstruction-review.md](../references/reconstruction-review.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## scan / access

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `source_visual_route`<br>導出 | 統合・導出 | 走査結果が候補なし・未アクセスのどちらか | 単独で配布された記録の用途を読めなくなるがrecord_type/statusで判定可 | record_type=scan/accessとstatusから一意導出。表示経路とは別の時点の結果 / 適用: 独立保存は不要、単独記録への表示は有用 | 現checkerは必須。faithful原図なし例外でもscan内はno_useful_candidate | [references/figure-extraction.md](../references/figure-extraction.md)、[references/reconstruction-review.md](../references/reconstruction-review.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## contract

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `attribution`<br>保存 | 条件付き | 原著者の報告とサーベイの制作を読者が区別できるか | 主張・図の作成者の帰属を読めない | attribution_note/キャプションへ一元化可。短い出典と変換説明の違いは残す / 適用: 読者への帰属が必要な場合 | 共通attribution自体は機械必須でない。再構成はattribution_note必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## pair / contract / manifest / asset

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `attribution_note`<br>保存 | 条件付き | 再構成のどの部分がサーベイの選択か | 原資料が作った関係と独自解釈を混同する | キャプションの正本から読者文・機械欄へ生成可能。出典だけでは代替不可 / 適用: サーベイ作成の表現に必要 | 再構成routeでmanifest/contract一致の必須文字列、no_candidateでは機械必須でない | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## contract / manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `boundary`<br>確認観点 / 保存 | 維持 | 主張・視覚関係をどの条件・標本へ限定するか | 図から過剰な一般化をする | claim/plotの境界をそのまま使う場合は参照・生成。図固有の選択範囲は別に保持 / 適用: 主張を担う表現に必要 | 主張manifest/contractの非空・一致が必須、内容の妥当性は未検査 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## contract / chart / element_map

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `uncertainty`<br>確認観点 / 保存 | 条件付き | 推定値・関係にどの不確実性があるか | 精密な値や確定因果と誤読する | 同じ不確実性を共通contract/chartへ二重入力せず正本から生成。要素別の違いは残す / 適用: 推定・変動・未報告が解釈に影響する場合 | 共通は未検査、chartでは存在時だけ非空文字列検査。elementは手動 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## contract / manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `status`<br>保存 | 条件付き | 表示内容が原資料報告かサーベイ解釈か | 主張・読者文の帰属区分が曖昧になる | source_visual_routeだけでは導出できない。claim_role/originで十分なら読者要約は生成 / 適用: 混合由来・解釈の区別が必要な場合 | 主張manifest/contractの非空一致が必須、許容語彙・意味は検査なし | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## contract

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `review`<br>結合・運用 | 維持 | 異なる検査観点の状態を区別して参照できるか | 単一PASSで科学的妥当性まで保証したように見える | 既存レビュー記録が正本ならコンテナは生成ビューでよい / 適用: 複数レビュー観点がある場合 | 主張contract必須オブジェクト。新たな独立IDは不要 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/reconstruction-review.md](../references/reconstruction-review.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |

## contract.review / build_record

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `deterministic_status`<br>導出 / 結合・運用 | 統合・導出 | 型・参照・数値等の機械検査が完了したか | 未検査と機械検査済みを混同する | 機械報告から導出し手入力を避ける。宣言値だけでは結果の証拠にならない / 適用: 機械検査する公開工程で必要 | nested reviewに必須。strictはpassed要求。EVCは入力の宣言を検査するだけ | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## contract.review / manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `semantic_status`<br>確認観点 / 保存 | 維持 | 表・矢印・図の意味をレビューしたか | 機械的に正しいが科学的に誤った図を公開する | 同じレビュー判断をflat/nestedへ生成。意味と忠実性は一方から導出しない / 適用: 主張表現に必要 | nestedとmanifest semanticは必須一致、strictはpassed | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## contract.review / manifest / sidecar / asset

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `fidelity_status`<br>確認観点 / 保存 | 条件付き | 必要な原資料の意味を切り出し・再構成で保存したか | 原資料誤りと変換誤りを区別できない | 切り出し忠実性と再構成忠実性の対象が異なるのにsidecarで同じ値を強制している。レビューの対象範囲を明示し用途に投影 / 適用: 原図使用・再構成時。候補なしは条件により不要 | nested必須、flatはmanifestまたはcontractで必要。sidecarは用途値と一致。strict原図はpassed/not_required、原図あり再構成はpassed | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## contract / manifest / packet / pair

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `visual_review_status`<br>確認観点 / 保存 | 条件付き | 読者向け図とキャプション・全要素のレビューが完了したか | 整った図や構造検査で未レビューを隠す | semantic/fidelityの単純ANDでは読者可読性・帰属の観点を失う。正本レビュー範囲を一度記録しpacket等に生成 / 適用: 再構成・高リスク読者図で必要 | 再構成strictはpassed必須、no_candidateはEVCで機械必須でない。deckは列要求 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/reconstruction-review.md](../references/reconstruction-review.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |

## contract / manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `contract_path`<br>結合・運用 | 統合・導出 | どの意味宣言をこの表示から検証するか | 検証の対象契約を選べない | contract内の自己参照は内容を増やさずpathで取得済み。正本はmanifest参照だけでよい / 適用: 外部分離した契約を使う場合 | EVC主張row必須またはCLI fallback。contract内contract_pathは未検査。deckはrow必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |

## contract

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `semantics`<br>保存 | 条件付き | この形式の行列・関係・軸の宣言は何か | 形式固有の意味を定義できない | kindごとの契約に内包。独立した別レコードIDは不要 / 適用: table/diagram/chartでは必要 | 主張全kindで非空object必須。source_figureでは中身を検査せずroot locatorのみ検査 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## contract / manifest / sidecar / packet / scan / access

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `generation_id`<br>結合・運用 | 条件付き | 同じ図IDの別生成・修正素材を取り違えていないか | 版を並存させる作業で古いレビューを流用する | 既存ID・出力hash・plot版で識別できる単発作業には不要 / 適用: 同一識別子で複数生成が並存する場合 | 任意だが一度指定すると全該当宣言の一致が必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## candidate / contract / manifest / pair / packet

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `decision_reason_code`<br>保存 | 条件付き | なぜ原図を使わず再構成・候補なしを選んだか | 易しさだけで再構成し原図探索を省く | 候補ごとの採否理由と最終用途の理由が違う場合は区別。no_candidateの固定値は生成可 / 適用: 原図不使用・再構成時に必要 | 再構成4語の閉集合、no_candidate=no_source_figureを要求。両側とpacketで一致 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## candidate / asset / sidecar / contract / manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `rights_basis`<br>確認観点 / 保存 | 条件付き | どの確認済み利用根拠に依拠するか | 利用条件が未確認のまま公開判断する | 同一原資料の同じ用途なら情報源または素材の正本から生成。用途が違えば判断も再確認 / 適用: 実際の原図利用時。原図なしには該当外 | 原図/原図あり再構成で必須、strictはunclear/not provided拒否。faithful原図なしは宣言禁止 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## candidate / asset / sidecar

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `license_status`<br>確認観点 | 条件付き | ライセンスに依拠した利用条件を確認したか | ライセンス条件を満たすか判断しにくい | rights_basisでライセンス依拠の場合だけ値を管理。引用ではnot_applicable / 適用: ライセンスを根拠とする場合のみ | EVC/deckはこの値を必須・clearedと要求しない。extractorは既定not_applicable | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## candidate / contract / manifest / pair / packet

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `source_cutout_asset_ids`<br>結合・運用 | 条件付き | どの原図素材と比較して意味を保存したか | 比較対象の物理素材を固定できない | 正本の変換関係から各ビューへ生成。asset_idはfigure_idと別 / 適用: 原図を使う最終経路に必要 | 原図/原図あり再構成は非空。no_candidateとfaithful原図なしは空。packetは集合一致 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## candidate / contract / manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `source_cutout_manifest_paths`<br>結合・運用 | 条件付き | 原図素材の取得・hash・出所をどの記録で確認するか | 原図の参照はあるが取得内容を検査できない | asset_id→sidecar path対応から生成可能。pathとIDを別々に手入力しない / 適用: 原図を使い外部付随記録へ分ける場合 | 原図/原図あり再構成は非空。ID配列と対応、監査root内、両側順序一致 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `source_scan_record_paths`<br>結合・運用 | 条件付き | 候補なし・アクセス不能をどの観測が支えるか | 未探索を候補なしと誤記しても検査不能 | 走査関係の正本から生成。実素材sidecarで代用不可 / 適用: 候補なし・未アクセス・faithful原図なし例外 | 該当route必須。原図/原図あり再構成では禁止 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## pair / packet / contract / manifest / asset

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `derived_asset_id`<br>結合・運用 | 条件付き | 比較・レビュー対象の派生素材はどれか | 別の再構成ファイルをレビューした結果を使う | 素材IDを正本にしpathはasset参照から導出可。独立pair IDは不要 / 適用: 再構成して素材が存在する場合 | faithful/new route、packetで必須一致。asset台帳に存在必須 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## pair / contract / manifest / asset

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `derived_asset_path`<br>結合・運用 | 統合・導出 | 派生素材をどこから開いて確認できるか | 素材IDがあっても実物を比較できない | asset_id→pathから生成可能。pair/manifest/contractへの手入力は不要 / 適用: ファイルを使う再構成時 | faithful/new routeで必須、root内実ファイルが必要 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## pair / asset / contract / manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `visual_comparison_packet_path`<br>結合・運用 | 条件付き | 変換の保持・変更・解釈とレビューをどこで読めるか | 原図と派生素材の関係を再調査する | pairをpacketに統合すれば同じ関係の別pathは生成参照で足りる / 適用: 再構成の比較を外部記録にする場合 | faithful/new routeで必須、packetのJSON内容を検査 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## asset / contract / manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `source_cutout_created_at`<br>結合・運用 | 統合・導出 | 原図確認が再構成作成より先か | 後から原図を探して整合したように見せる | 素材のretrieved_at/creation eventから生成。手動二重時刻は不整合要因 / 適用: 工程順序を確認する原図あり経路 | 原図/原図あり再構成必須、再構成時刻以下。faithful原図なしでは禁止 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `reconstruction_created_at`<br>結合・運用 | 条件付き | 派生図が候補走査・原図取得後に作られたか | 制作順序の必要条件を検査不能 | 制作イベントから生成し同じ時計・形式へ統一。時刻だけでは原図を読んだ証拠にならない / 適用: 再構成の手順を検証する場合 | faithful/new route必須、cutout/scanより早い時刻は禁止 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## pair

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `source_figure_locator`<br>保存 | 統合・導出 | 変換元の原図を原資料のどこで見られるか | 素材をなくすと変換元へ戻れない | figure_id→candidate.locatorから導出できる。候補正本を参照する / 適用: 原図由来の再構成時 | pair自体は未検査。source_figure contractではlocatorのaliasとして必須 | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## pair / packet

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `preserved_relation`<br>保存 | 維持 | 変換後も保持した関係・値は何か | 見た目だけの比較で意味保存を判断する | captionの保持群と重複するが監査の詳細と読者要約を区別。element_mapから要約可能 / 適用: 再構成比較時に必要 | packetの非空文字列が必須。具体的な関係は機械判定しない | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `changed_elements`<br>保存 | 維持 | どの要素・配置・省略を変更したか | 加工で意味を変えた箇所を確認できない | element_mapの変換起源を正本としpacket/読者説明へ要約・生成 / 適用: 変換時に必要。変更なしも明示 | packet非空文字列必須 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `added_interpretation`<br>保存 | 維持 | 原資料にないどの解釈をサーベイが加えたか | 原資料の事実と作成者の推論を混同する | element_map.origin/source_supportから全て安定導出はできないが一度記録して要約可能 / 適用: 独自解釈有無を判断する再構成時 | packet非空文字列必須。無しも明示文字列が必要 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `reader_benefit`<br>確認観点 | 条件付き | 再構成によって何が読み取りやすくなるか | 編集コストだけで図を選ぶ | decision reasonをそのまま再掲するなら不要。局所的な便益を採否注記へ統合可 / 適用: 再構成と原図の採否が拮抗する場合 | 任意、存在・型も機械検査しない | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `verification_cost`<br>確認観点 | 条件付き | 原図取得・全要素レビューの負担に見合うか | 不必要な再構成を選びレビュー負担を増す | 独立の数値算定は不要。reader_benefitと一つの採否注記へ統合可 / 適用: 検証負担が採否判断を変える場合 | 任意、機械検査なし | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## asset / sidecar

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `asset_id`<br>結合・運用 | 維持 | 一つの保存素材・版をどれとして参照するか | 同じ原図の異なる切り出し・変換結果を混同する | path/hashで識別できるが移動・比較関係の安定キーとして有用。1視覚使用と1素材は同一でない / 適用: 素材を再利用・比較する場合 | sidecar必須、参照素材はasset台帳への存在要求 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `canonical_url_or_doi`<br>保存 | 条件付き | 情報源の正規の位置へ戻れるか | 取得URLが変わると情報源の同一性を見失う | source recordから参照・生成できる。取得URLと同義ではない / 適用: リモート情報源・書誌同一性確認時 | strict sidecarでlocal sourceなしならcanonical_url_or_doiまたはsource_url_or_doiが必要 | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `retrieved_url`<br>保存 | 条件付き | 実際にどのURLを要求して画像・PDFを得たか | 正規URLと取得物の相違を追跡不能 | canonicalと違う場合のみ差分を保存。localにはnull / 適用: リモート取得で追跡が必要な場合 | extractor出力、EVCはこの個別キーを必須としない | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |
| `final_url`<br>保存 | 条件付き | リダイレクト後にどの実物を得たか | 転送による版・出所の違いを見逃す | retrieved_urlと同一なら保存ビューへ同値を生成できる。ない場合推測禁止 / 適用: 転送・取得先差がある場合 | EVC個別必須でない | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |
| `source_sha256`<br>導出 / 結合・運用 | 維持 | 取得・比較の基礎となる原資料bytesは同じか | 別版からの再抽出や改変を検出不能 | ファイルから算出するが過去の基準hashを保存する意味がある。台帳とsidecarへ生成 / 適用: 素材の同一性と監査再現が必要な場合 | sidecar64桁必須、local material存在時は再計算照合 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `output_sha256`<br>導出 / 結合・運用 | 維持 | 保存切り出しがレビュー当時の素材と同じか | レビュー後の差替えを検出不能 | 生成時に算出し基準として保存。各記録へ手動転記しない / 適用: レビュー対象を固定する場合 | sidecar64桁必須、出力ファイルから常時再計算照合 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `source_hash_basis`<br>保存 | 維持 | 原画像bytes・PDF全体など何のhashか | HTMLページhashと画像hashを誤比較する | source material種とacquisition modeから一部導出可。hash対象の差は残す / 適用: 複数取得経路がある場合 | sidecar必須。local basisの場合はlocal materialへの参照必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## sidecar

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `source_snapshot_path/local_image_path/local_source_path`<br>結合・運用 | 条件付き | 原資料bytesをローカルで再検証できるか | 保存hashの基礎を再計算できない | 同じsource materialへの経路aliases。実際の媒体・snapshotの違いは区別、同じpathを複数手入力しない / 適用: local hash basis時、再現を要する素材時 | いずれかある場合解決・再hash。strict local basisで無しは失敗 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## asset / sidecar

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `figure_or_page_locator`<br>保存 | 条件付き | どのページ・領域を切り出したか | 複合PDFと画像素材の対応を復元できない | candidate.locatorとcrop_spec/pageから生成できるが取得時点の範囲を残す / 適用: 原資料からの切り出し時 | sidecar一般必須としては検査されない。routeのcontract.locatorとは別 | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `asset_url`<br>結合・運用 | 削除候補 | 取得画像自体のリモート位置はどこか | 元素材の再取得先が失われる場合がある | extractorではfinal_urlと同一。独立の手入力属性としては削除候補 / 適用: 元素材のURLが他のURLで保持されない場合だけ | 個別検査なし | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |
| `acquisition_mode`<br>保存 | 条件付き | 画像取得・PDF領域描画など何を行ったか | 変換の種類と切り出し品質を解釈できない | transformation_historyで十分な場合別項目は索引。mode aliasは生成可能 / 適用: 取得経路の説明・再実行時 | extractor出力、EVC個別必須でない | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |
| `retrieval_date/retrieved_at`<br>保存 | 統合・導出 | どの時点で原資料を取得したか | 更新される資料の版・取得順序が不明になる | 同じ取得時刻のaliases。source_cutout_created_atへ工程時刻を生成可能 / 適用: 可変情報源または工程順序に関係する時 | extractorは両方生成。sidecar取得時刻自体の必須検査なし | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |
| `source_mime_type`<br>保存 | 条件付き | 原資料は画像・PDF・変換元のどれか | 取得・再処理に合うツールを選びにくい | bytes/headerから導出可能。PDF変換元と変換後のMIMEを混同しない / 適用: 形式が再処理判断を変える場合 | 個別検査なし | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |
| `output_mime_type`<br>導出 | 統合・導出 | 出力素材の形式は何か | 対応する描画ツールの選択がやや難しくなる | ファイルから安定導出でき、拡張子とbytesも保持されるため人手入力不要 / 適用: 外部ツールとの受渡し時 | 個別検査なし | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |
| `crop_spec`<br>保存 | 維持 | 原図のどの領域を取ったか | 不要な範囲と意味の切落しを原資料と比較できない | 変換操作の正本。上位のpixel_crop/pdf_bbox_pt aliasは生成 / 適用: 切り出しの再現時必要 | extractorの座標指定は検査。EVCはcrop_spec内容を検査しない | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |

## asset.crop_spec

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `pdf_bbox_pt`<br>保存 | 条件付き | PDFページのどの矩形領域か | 同じページから別領域を抽出しても区別不能 | HTMLはnull。pixel_cropとは座標系・適用段階が異なり統合不可 / 適用: PDF領域指定時のみ | extractorは有限座標・範囲検査。EVC個別検査なし | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |
| `pixel_crop`<br>保存 | 条件付き | 原画像・描画後画像のどの領域を採用したか | ピクセル領域の加工を再現できない | pdf_bbox_ptと異なる段階。上位aliasは生成 / 適用: ピクセル切り出し時のみ | extractorは範囲外拒否。PDFはbbox/crop少なくとも一つ必須 | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |

## asset / sidecar

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `output_dimensions/output_size_px`<br>導出 | 統合・導出 | 読者の読む大きさで解像度が十分か | 品質の事前判断が少し遅れるが実物で確認可 | 出力画像から安定導出し、同義aliasesを手動維持しない / 適用: 解像度による採否を行う場合 | EVC個別必須でない。extractorは両方出力 | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |
| `transformation_history`<br>保存 | 維持 | 取得後に何の変換・切り出し・正規化を行ったか | 加工で意味を変えた原因を追跡できない | crop_spec/conversionに構造があれば説明は生成。人手の意味判断は別に残す / 適用: 原資料を変換した時必要 | EVC内容を検査しない。extractorは履歴を生成 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |
| `asset_role`<br>保存 | 条件付き | 比較用原図・派生素材など何の役割か | 素材を読者表示と監査比較のどちらに使うか曖昧になる | source_cutout sidecarの種別から固定値生成可。一般assetでは役割を保持 / 適用: 異種素材の管理時 | sidecarはasset_role=source_cutoutを必須、他素材の全種類は未検査 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `review_only`<br>保存 | 統合・導出 | 素材は比較専用か読者表示にも使うか | 監査用の未加工ページなどを表示素材と誤用する | 物理assetの固定属性にすると同じ素材の表示利用と矛盾。使用関係の属性へ位置づける / 適用: 用途が分かれる場合 | source-cutout sidecarは常にtrue必須。実物の表示有無をこの欄で検査しない | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## sidecar

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `output`<br>結合・運用 | 維持 | hash照合の対象切り出しファイルはどこか | ID/hashはあっても実物へ到達できない | asset recordの出力pathから生成。derived_asset_pathと対象が違う / 適用: 物理ファイルを検証する場合 | sidecarの実ファイル参照必須、監査root内、hash照合 | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## asset.conversion

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `conversion.tool`<br>保存 | 条件付き | どの変換ツールを使ったか | 変換による配置差の原因を特定できない | 取得時に保存しtransformation_historyへ生成 / 適用: 元資料をPDFへ変換した場合 | extractor出力、EVC個別必須でない | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |
| `conversion.version`<br>保存 | 条件付き | そのツールのどの版を使ったか | 同じツール名でも異なる描画結果を再現できない | 自動取得しconversion正本と履歴へ一度反映 / 適用: 元資料をPDFへ変換した場合 | extractor出力、EVC個別必須でない | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/extract_source_figure.py](../scripts/extract_source_figure.py) |

## scan / access

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `record_type`<br>結合・運用 | 維持 | 走査結果かアクセス試行かを単独記録で識別できるか | JSON記録を別用途の証拠として受け付けやすい | status/routeと1対1に近いがデータ種別の判別子として一つ残し他を生成 / 適用: 独立の観測記録を扱う場合 | source_figure_scan/accessの指定値が必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `status`<br>保存 | 統合・導出 | 観測結果が候補なし・未アクセスのどちらだったか | 未知・未確認と確認済み候補なしを混同する | record_type/routeから導出可能なこの2種のみなら独立入力は冗長。観測結果の正本は一つ / 適用: 探索の結果を保存する場合 | no_candidate/inaccessibleの指定値必須 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `locator`<br>保存 | 維持 | どの範囲を調べ、何へアクセスを試みたか | 同じ情報源の未調査部分を候補なしと判断する | candidate locatorは図の位置、ここは検索範囲で意味が異なる。単純統合不可 / 適用: 候補の位置を特定する場合に必要 | 必須非空。source_locator/access_locator aliases許容 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## scan

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `reason/summary/note`<br>保存 | 維持 | その範囲に主張を表す原図がない理由は何か | 候補探索をしたという宣言しか残らない | 同義aliasesを一つに統一して記録可能。decision_reason_codeの固定値だけでは不足 / 適用: 候補なしの判定に必要 | いずれか非空文字列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## access

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `access_status`<br>保存 | 維持 | アクセスできなかった具体的理由・範囲は何か | アクセス失敗と資料自体の不存在を誤認する | 固定status=inaccessibleとは別の説明。source access記録へ統合可能 / 適用: 未アクセス時必要 | 必須非空文字列 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## scan / access

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `observed_at/created_at/timestamp`<br>保存 / 結合・運用 | 維持 | 何時の観測で候補なし・アクセス不能と判断したか | 更新後の資料へ古い観測をそのまま適用する | 同一の観測時点としてaliasesの一つで足りる。created_atを観測時刻と混同しない / 適用: 変化する情報源・工程順序の確認時 | いずれかISO時刻必須、原図なし再構成より遅い観測は禁止 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## contract.source_figure

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `locator`<br>保存 | 維持 | 表示した原図の根拠位置はどこか | 読者用画像と情報源の原図を照合できない | candidate/assetの位置から生成。source_figure_locator alias可 / 適用: 候補の位置を特定する場合に必要 | source_figure kind/routeで必須。sidecar locatorの深い意味一致は未検査 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## TableContract

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `row_axis`<br>保存 | 維持 | 行がどの比較対象集合を表すか | セルの所属対象を定義できない | 列軸とは別の役割。objectコンテナ自体は新規対象でない / 適用: 表を意味レビューする場合 | object必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `row_axis.name`<br>保存 | 条件付き | 行軸を読者が何と呼ぶか | 行見出しを得るためmeaningを読む必要がある | meaningと同一なら短名を別手入力せず表示名を生成 / 適用: 複雑な意味と短い表示を分ける場合 | 非空文字列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `row_axis.meaning`<br>保存 | 維持 | 各行を一件とする比較単位は何か | 研究・報告・実験条件を同じ単位として比較してしまう | nameのみでは単位・境界を説明できない / 適用: 行比較の単位が解釈を変える場合に必要 | 非空文字列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `row_axis.labels`<br>保存 / 結合・運用 | 維持 | 比較する各行の対象はどれか | セル配置と根拠対象が対応しない | セルmapから導出するだけでは欠けた行を検出不能。予定対象集合として保存 / 適用: 行集合を定義する表に必要 | 非空・一意の文字列配列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `column_axis`<br>保存 | 維持 | 列がどの条件・評価軸を表すか | セルの比較軸を定義できない | row_axisとは意味が異なる役割 / 適用: 表を意味レビューする場合 | object必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `column_axis.name`<br>保存 | 条件付き | 列軸を読者が何と呼ぶか | 読者表示の短名をmeaningから切り出す必要がある | meaningと同一なら生成可 / 適用: 短名と条件説明を分ける場合 | 非空文字列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `column_axis.meaning`<br>保存 | 維持 | 比較結果がどの条件・軸で報告されたか | 異なる条件を同じ比較軸へ混在させる | nameでは測定条件の範囲を説明しきれない / 適用: 条件が結果の解釈に影響する場合 | 非空文字列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `column_axis.labels`<br>保存 / 結合・運用 | 維持 | どの条件・指標の列を揃えるか | 対象条件の欠落・重複を検出不能 | 予定列集合を保存。cell mapからの単純導出では欠落検出が弱い / 適用: 比較表に必要 | 非空・一意の文字列配列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `cell_meaning`<br>保存 | 維持 | 各セルは観測値・評価・未測定のどれか | 計画やメタデータを結果と混同する | 列別に意味が違う表では表全体の単一意味が粗い。明示された比較列の型と対応を保つ / 適用: 主張を担う表に必要 | 非空文字列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `orientation`<br>確認観点 / 保存 | 統合・導出 | 行・列の対応を読者が正しく読むか | 軸の入替え・転置を見逃す | 通常はrow_axis/column_axisから生成可能。見た目の転置や非標準配置時は独立の確認意味あり / 適用: 通常配置では生成、意味の転置が問題になる場合に保持 | 常に非空文字列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `axis_mirror`<br>導出 | 統合・導出 | 契約・読者表・レビュー用説明が同じ軸宣言か | 照合補助文がなくなるが元の軸宣言で同じ問いには答えられる | row/column meaning、cell_meaning、orientationから完全導出。独立属性として手動編集不可 / 適用: 独立保存は不要 | 常に非空文字列必須、規定展開に完全一致 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `unit`<br>保存 | 条件付き | 数値セルが何の単位か | 数値の尺度・意味を読めない | 質的表では適用外。同じ列に異なる単位なら全表単位だけで足りない / 適用: 数値・量を表す表に必要 | 現checkerは質的表でも非空unitを必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `cells`<br>保存 | 維持 | 行と列の組合せごとに何が報告されたか | 比較の値・結果自体が失われる | 原資料dataから生成可能でも、採用した当時の値と未測定状態は必要 / 適用: 根拠表に必要 | 矩形行列または完全Cartesianのcell map必須。数値有限、意味的な値の真偽は未検査 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## TableContract.cells

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `cells[].row`<br>結合・運用 | 条件付き | セルがどの比較対象行に属するか | 別研究の値を当該研究の結果と読む | map形式のみ必要、行列なら行位置から導出 / 適用: cell map形式の場合だけ | mapでは非空文字列必須、全組合せの一意性検査 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `cells[].column`<br>結合・運用 | 条件付き | セルがどの条件・軸の列に属するか | 対照と課題など条件を入れ替える | map形式のみ必要、行列なら列位置から導出 / 適用: cell map形式の場合だけ | mapでは非空文字列必須、全組合せの一意性検査 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `value`<br>保存 | 維持 | このセルの報告値は何か | 対応位置だけあって結果がなくなる | 行列では直接の値、mapではvalueキー。観測データから生成できても採用状態を保持 / 適用: 観測・比較の結果がある場合 | mapはvalueキー自体を必須にしない。存在する数値の有限性だけ検査 | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## DiagramContract

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `nodes`<br>保存 | 維持 | 関係を結ぶ対象集合は何か | 辺が何の対象を結ぶか定義不能 | element mapとの共通対象を参照し、意味を二重手入力しない / 適用: 関係図に必要 | 非空list必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## DiagramContract.nodes

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `id`<br>結合・運用 | 維持 | どのノードを端点・読順から参照するか | 同名ノード・表記変更で別対象を混同する | ラベルとは異なる局所識別子。図を超える普遍IDは不要 / 適用: 複数ノードを結ぶ場合 | 各nodeの非空一意文字列必須 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `label`<br>保存 | 条件付き | ノードを読者へどう表示するか | 内部IDまたはmeaningの長文しか表示できない | meaningと同一なら表示文字列を生成。短名は条件付き / 適用: 短い表示名が必要な場合 | 現checkerはlabelを必須・型検査しない | [references/reconstruction-review.md](../references/reconstruction-review.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `meaning`<br>保存 | 維持 | ノードが表す対象・状態・構成概念は何か | 見た目のラベルから機序・カテゴリを推測する | labelとは異なる意味定義。element mapの意味と一元化可 / 適用: 意味を担うnodeに必要 | 各node非空文字列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## DiagramContract

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `edges`<br>保存 | 維持 | どの対象間にどの関係があるか | 図が説明する関係が失われる | 意味関係は保存、描画位置は別。ノード集合だけから導出不能 / 適用: 関係を表す図で必要 | list必須だが空listも許容 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## DiagramContract.edges

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `edges[].from`<br>結合・運用 | 維持 | 関係の出発点はどのノードか | 原因・前提・入力側を逆に読み得る | 図式内局所参照。対称比較でも端点を指定する / 適用: 辺を持つ場合 | 非空文字列必須、宣言済みnodeへの解決必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `edges[].to`<br>結合・運用 | 維持 | 関係の到達点はどのノードか | 結果・後続・出力側を逆に読み得る | 図式内局所参照。fromとは有向意味上区別 / 適用: 辺を持つ場合 | 非空文字列必須、宣言済みnodeへの解決必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## DiagramContract.edges / element_map

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `relation/relation_type`<br>保存 | 維持 | 因果・時間・分類・比較など何の関係か | 矢印の形で根拠以上の因果を推論する | meaning/原資料文章だけから安全に導出できない。element_mapとの同値は生成 / 適用: 関係を伝える意味要素に必要 | diagram各辺は制御語彙必須。element_mapは機械未検査 | [references/reconstruction-review.md](../references/reconstruction-review.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## DiagramContract

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `reading_order`<br>保存 / 確認観点 | 条件付き | 読者が図をどの順で検査するか | 手順図・物語図の読む順が曖昧になる | 手順は辺から導出できる場合あり。対称比較や無順序の分類は単一全順序が不要で新たな意味を足す / 適用: 順序が解釈・説明を変える場合のみ | 現checkerは全diagramで各nodeを一度含む順序を必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `legend`<br>保存 | 条件付き | 色・線種・形・位置が何を意味するか | 装飾をカテゴリ・因果強度と誤読する | 視覚符号化宣言から生成可能。符号化がない場合は不要 / 適用: 視覚符号化が意味を担う場合 | 指定のencodingキーがnode/edgeにある時だけ非空legend要求。意味ありの潜在encoding全てを検出するわけではない | [references/reconstruction-review.md](../references/reconstruction-review.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## DiagramContract.nodes/edges

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `nodes/edges.color`<br>保存 | 条件付き | 色の違いがどのカテゴリ等を符号化するか | 色の装飾と意味を混同する | 純粋な装飾指定は制作コードで足りる。意味を持つ符号化のみモデルへ残す / 適用: カテゴリ等を符号化する場合のみ | これらキーの存在でlegend要求。値や意味自体はcheckerで未検査 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `nodes.fill`<br>保存 | 条件付き | 塗りの違いが何を意味するか | 塗りを意味ある区分と誤読する | 純粋な装飾指定は制作コードで足りる。意味を持つ符号化のみモデルへ残す / 適用: カテゴリ等を符号化する場合のみ | これらキーの存在でlegend要求。値や意味自体はcheckerで未検査 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `nodes/edges.line_style`<br>保存 | 条件付き | 線種がどの関係型・状態を表すか | 実線と破線の根拠強度や関係型を誤解する | 純粋な装飾指定は制作コードで足りる。意味を持つ符号化のみモデルへ残す / 適用: カテゴリ等を符号化する場合のみ | これらキーの存在でlegend要求。値や意味自体はcheckerで未検査 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `nodes.shape`<br>保存 | 条件付き | 形の違いがどの対象型を表すか | 異なる形を別の構成概念と推測する | 純粋な装飾指定は制作コードで足りる。意味を持つ符号化のみモデルへ残す / 適用: カテゴリ等を符号化する場合のみ | これらキーの存在でlegend要求。値や意味自体はcheckerで未検査 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `nodes.position`<br>保存 | 条件付き | 配置がどの尺度・群・順序を示すか | 近接や上下で支持されない関係を推測する | 純粋な装飾指定は制作コードで足りる。意味を持つ符号化のみモデルへ残す / 適用: カテゴリ等を符号化する場合のみ | これらキーの存在でlegend要求。値や意味自体はcheckerで未検査 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `nodes.x`<br>保存 | 条件付き | 横座標がどの尺度・位置を示すか | 座標差の意味を再現できない | 単にピクセル座標なら制作属性。尺度意味がある場合にだけモデルで保持 / 適用: カテゴリ等を符号化する場合のみ | これらキーの存在でlegend要求。値や意味自体はcheckerで未検査 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `nodes.y`<br>保存 | 条件付き | 縦座標がどの尺度・位置を示すか | 上下の意味・尺度を再現できない | 単にピクセル座標なら制作属性。尺度意味がある場合にだけモデルで保持 / 適用: カテゴリ等を符号化する場合のみ | これらキーの存在でlegend要求。値や意味自体はcheckerで未検査 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `edges.style`<br>保存 | 条件付き | 辺の表示規則がどの意味を担うか | 線の太さ等を支持されない強度と読む | color/line_styleと同じ符号化ならそれらから生成 / 適用: カテゴリ等を符号化する場合のみ | これらキーの存在でlegend要求。値や意味自体はcheckerで未検査 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## ChartContract

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `x_axis`<br>保存 | 維持 | 横軸はどの変数・条件を示すか | 結果と条件を取り違える | 横軸への対応は表示選択として保存 / 適用: 主張グラフで必要 | 両方object必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `y_axis`<br>保存 | 維持 | 縦軸はどの変数・結果を示すか | 変数の増減の意味を取り違える | 縦軸への対応は表示選択として保存 / 適用: 主張グラフで必要 | 両方object必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## ChartContract.axis

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `name`<br>保存 | 維持 | 軸で表す変数・条件は何か | プロットの増減が何の増減か不明になる | claim/dataの変数名から表示へ生成可能だが軸への対応は保存 / 適用: グラフに必要 | 両軸で非空文字列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `unit`<br>保存 | 条件付き | 軸値の尺度・単位は何か | 件数・割合・カテゴリを混同する | カテゴリ軸には物理単位は適用外、categoryの明示で意味を区別 / 適用: 数値尺度に必要、カテゴリでは尺度種別として条件付き | 両軸で非空文字列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## ChartContract

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `comparator`<br>保存 | 維持 | 何を対照として差・傾向を解釈するか | 結果の比較基準を隠して効果を過大評価する | 原資料の条件と共有なら生成可能。none_applicableも理由を残す / 適用: 比較主張で必要、非比較時は該当外を説明 | 全chartで非空文字列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `comparator_explanation`<br>保存 | 条件付き | 比較対象が該当しない理由は何か | none_applicableが比較基準欠落の隠蔽になる | 比較なしの説明はcomparator記述と一体化可能。新規独立レコード不要 / 適用: comparator=none_applicableの場合 | 現checkerはこの条件で必須。現在の文書は必要説明を記すがキー名を列挙していない | [references/figure-extraction.md](../references/figure-extraction.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `aggregation`<br>保存 | 維持 | 個々の値を平均・合計等でどうまとめたか | 集約レベル差を実質の差と誤読する | numeric/source dataの計算定義を参照可能。グラフ固有の集約は残す / 適用: 集約値のグラフに必要、非集約ならそう記す | 全chartで非空文字列必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `domain`<br>保存 | 維持 | 図に表示する数値範囲・カテゴリ集合は何か | 軸切断・カテゴリ省略による意味変化を見逃す | 観測dataのmin/maxと表示範囲は一致しないことがあるため単純導出しない / 適用: 表示範囲が判断に影響する場合 | 全chartでobject必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## ChartContract.domain

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `type`<br>保存 | 維持 | 連続・対数・カテゴリのどの尺度か | 倍率と差・名義順序を混同する | データ値だけから決められない描画の選択 / 適用: グラフの尺度解釈に必要 | continuous/log/category/categoricalのいずれか必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `domain.min`<br>保存 | 条件付き | 表示尺度の下端はどの値か | 軸の切断で差が過大に見えるか判断できない | データ極値とは別。描画と同じ宣言から生成 / 適用: 連続・対数範囲のみ | 該当typeで有限scalar必須、min<max、log正範囲 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `domain.max`<br>保存 | 条件付き | 表示尺度の上端はどの値か | 上端による切詰め・縮尺差を判断できない | データ極値とは別。描画と同じ宣言から生成 / 適用: 連続・対数範囲のみ | 該当typeで有限scalar必須、min<max、log正範囲 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `labels/values`<br>保存 | 条件付き | どのカテゴリを表示対象に含めたか | 省いたカテゴリと値の欠落を混同する | 表示対象集合として保存。元データから自動抽出だけでは意図的除外を説明できない / 適用: カテゴリ範囲のみ | category/categoricalではlabelsまたはvaluesの非空配列が必須 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `plot_version`<br>結合・運用 | 条件付き | どの版のプロットからスライドを作ったか | 修正前の主張で作った資料を公開する | プロット参照の版から生成。単一固定版でもhandoffには有用 / 適用: プロットと制作を同期する場合 | plot使用時deck列必須、EVC strict manifestでplotを要求 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## manifest / G4-PD

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `plot_row_id`<br>結合・運用 | 条件付き | どのプロット行を表示判断へ反映したか | 指摘を最初の影響行へ戻せない | slide→plotの一対一なら生成できる。splitでは複数ページが一行を共有 / 適用: プロットがある発表制作時 | plot supplied時manifest整合をplot checkerが検査。G4-PD自体は任意 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_storyline_plot.py](../scripts/check_storyline_plot.py) |

## manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `section_id`<br>結合・運用 | 統合・導出 | このページはどの節の問いへ寄与するか | 節単位の構成・順序の整合を見失う | plot_row→sectionで安定導出、手動二重入力不要 / 適用: 節構成を持つ発表時 | plot_required時deck列必須、plot checkerが照合 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_storyline_plot.py](../scripts/check_storyline_plot.py) |
| `evidence_block_id`<br>結合・運用 | 条件付き | どの根拠群・説明のまとまりに属するか | 方法・結果・境界の関連ページをまとめて修正しにくい | plot rowの既存根拠ブロックから生成。単一ページでは別の主体を追加しない / 適用: 根拠を複数ページで分担する場合 | plot_required時deck列必須、plot checker照合 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_storyline_plot.py](../scripts/check_storyline_plot.py) |
| `source_pointer`<br>保存 / 結合・運用 | 統合・導出 | 読者向け主張の出典を短い表示でどう示すか | 根拠ページの出典表示が曖昧になる | source_ids＋locatorから人が読める短文を生成。ID関係と表示文字列は役割が違う / 適用: 根拠ページで必要 | deck根拠classでは非空必須、EVC自体は未検査 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |
| `narrative_job`<br>保存 | 統合・導出 | このスライドは説明の流れで何を担うか | 見出しだけでページを作り説明が進まない | プロットの同属性から生成。reader_roleは図の仕事なので単純統合不可 / 適用: 発表ページで必要 | deck列必須。具体的な文章内容は未検査 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_storyline_plot.py](../scripts/check_storyline_plot.py) |
| `presenter_note`<br>保存 | 条件付き | 読み手への主張とは別に何を短く話すか | 話す内容と図の接続をその場で再構成する | プロット行の注記を正本にして生成。不要時not_neededで足りる / 適用: 口頭発表で補助が有用な場合 | plot checkerの適用条件に依存。EVC/deck単独は本文内容を判定しない | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_storyline_plot.py](../scripts/check_storyline_plot.py) |
| `rrm_focus`<br>確認観点 | 条件付き | 中心行の意味を変える主な研究読解の役割は何か | 探索・修正の索引がなくなるが既存claim/plotリンクで意味は回収可能 | 既存関係から復元できるなら別必須属性不要 / 適用: 索引を付けると作業が改善する場合のみ | 任意、EVC/deckは必須にしない | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `primary_visual_type`<br>保存 | 維持 | 読者向けの実物は原図・表・方法図等のどの形式か | 形の選択と計画の違いを観測しにくい | kindは意味検査の種類、こちらは制作形式。relation＋routeだけでは式/写真等を特定できない / 適用: 発表で形式を計画・観測する時 | deck全行で許容10値必須、source_figure routeは同値要求 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |
| `evidence_class`<br>保存 | 条件付き | 根拠・方法・境界・統合・表紙等のどのページ役割か | 根拠不要なページに重い検査、または根拠ページを免除する | narrative_jobと重なるがscope分岐に利用。プロットの役割から生成できる場合あり / 適用: 作業の検査対象を切る場合 | deck列必須、none/not_applicable可否と根拠検査を分岐 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |
| `citation_visible`<br>確認観点 | 維持 | 出典を読者に見える場所へ出す計画か | 注記にだけ出典を置いて読者の帰属が不明になる | 観測済み結果ではなく制作上の宣言。実物検査の結果から導出不可とするなら正本計画は一つ / 適用: 根拠ページで必要 | deck根拠classはtrue相当必須、実物でcitationを観測 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |
| `numeric`<br>確認観点 | 条件付き | 量的な解釈の条件を確認すべきページか | 定性的資料に分母を強制、または数値の尺度を確認しない | 単に数字を数えて導出すると年・IDも量と誤認。人のscope判断に意義 / 適用: 量的な主張の場合 | deck列必須、true時denominator_unit非空を要求。数値値の妥当性は未検査 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |
| `denominator_unit`<br>確認観点 / 保存 | 条件付き | 割合の分母と量の単位を読者が把握できるか | どの母集団の割合・どの尺度の量か読めない | 定量属性のうちその数量に適用する分母・単位・尺度を結合表示する。全数値に分母はなく、平均・係数では該当外と尺度等を示せる / 適用: その数量に適用し解釈に必要な分母・単位・尺度を示す場合 | deck numeric=trueで非空必須、分母と単位の両方があるかは機械未検査 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |
| `aggregation_level`<br>保存 | 条件付き | 個人・試行・研究などどの粒度で集約したか | 異なる対象粒度の結果を直接比較する | chart aggregationやnumeric recordの同じ粒度を参照・生成。意味を明示して対応させる / 適用: 集約や重複が解釈を変える場合 | deck列は必須だが値の非空・意味は検査しない | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |
| `caveat_visible`<br>確認観点 | 統合・導出 | 解釈を変える注意・境界を読者面へ表示するか | 限界が注記へ隠れる | boundary_visibility等と重複。可視性計画を既存G4-PDから生成する / 適用: 注意が意味を変える場合 | deck列必須だがcaveat_visibleの値を実物と照合していない | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |
| `internal_vocab_free`<br>確認観点 | 統合・導出 | 制作・工程語彙を読者面から除いたか | 内部IDと運用指示が説明文へ残る | 毎ページの固定yesの手入力は証拠にならない。制作条件を正本にし観測結果を別に保持 / 適用: 読者向け成果物の品質条件として必要 | deck根拠classではtrue相当を要求、実物語彙検出とは別 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |
| `min_body_pt`<br>確認観点 | 条件付き | この媒体・ページで選んだ文字サイズ下限を満たすか | 過度な縮小を検査時に判定できない | 全ページ同じならプロファイル/CLIの閾値から生成。ページ固有の例外だけ残す / 適用: 媒体別可読性の数値基準を選ぶ場合 | deck根拠行でfloat可を要求。観測ではrow値またはCLI floorを使う | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |
| `protected_terms`<br>確認観点 | 条件付き | 書出し・フォント変換で壊れてはならない用語は何か | 重要用語の文字落ちを見逃す | 普通の語すべてを登録すると冗長。技術語・記号など壊れるリスクがある部分のみ / 適用: 書出し時の用語欠損が重要な場合 | deck列必須、語群をPDF観測へ渡す。値は空可 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py) |

## G4-PD

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `claim_id`<br>結合・運用 | 条件付き | どの主張の読者向け図の仕事を決めたか | プロット注記の解釈判断が主張と結びつかない | 既存claim_refs/visual.claim_idsから単一対象を選ぶ。複数主張の場合の粒度を明記 / 適用: G4-PD注記がある場合 | この注記自体の機械必須検査なし | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `reader_visual_job`<br>保存 | 統合・導出 | 図が本文だけでは得られない何を検査させるか | 本文を繰り返すだけの図を残す | contract.reader_roleと同じ仕事なら一度記録して投影。原資料側candidate関係とは別 / 適用: 意味を担う図の読者設計で必要 | 機械必須検査なし。既存注記に保存できる | [references/figure-extraction.md](../references/figure-extraction.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `reader_layout_route`<br>保存 | 条件付き | 一枚通常・一枚密・複数枚のどれで読ませるか | 密度による分割が後工程の場当たり判断になる | ページ数やobject数からは意図を導出できない。常にreaderなら定数生成可 / 適用: 密な情報を分割するかが判断を変える場合 | この注記の3値をcheckerは検査しない | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `boundary_visibility`<br>確認観点 | 統合・導出 | 必要な境界を読者が見られるか | プロットの境界がレイアウトで消える | manifest.caveat_visibleと同じ意味なら生成。boundaryの内容と可視性は別 / 適用: 境界を図・ページへ残す場合 | 機械必須検査なし | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `meaning_changing_fields_visible`<br>確認観点 | 条件付き | 条件・単位・分母等を表示から落としていないか | 図を簡略化して主張の意味が変わる | 各semantic条件の読者表示を確認する注記で十分。全属性の別booleansを追加しない / 適用: 意味条件を省略・移動する配置時 | 機械必須検査なし | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `説明の進展への寄与（非スキーマ項目）`<br>確認観点 | 条件付き | この図で問いから次の問いへ何が進むか | 図が飾りか議論の根拠かを判断しにくい | narrative_job＋Nextから同じ答えが得られるなら独立記録不要 / 適用: 進展が曖昧な図を検討する場合 | 未検査、固定progression_deltaキーは定義されていない | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## element_map

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `表示要素（自然言語項目）`<br>保存 / 結合・運用 | 維持 | どの局所矢印・値・セルを確認するか | 具体的な修正対象が分からない | 図内の既存要素ID・座標・セル位置で足りる / 適用: 主張を担う再構成の全意味要素 | element_mapは新checkerスキーマではなく手動G6必須 | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `要素種類（自然言語項目）`<br>保存 / 結合・運用 | 維持 | 矢印・ノード・値・軸等のどの種別か | 種別に合った最低限の問いを選べない | 図式・表の要素種から生成できる時は別手入力不要 / 適用: 主張を担う再構成の全意味要素 | element_mapは新checkerスキーマではなく手動G6必須 | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `伝える主張・観測・関係（自然言語項目）`<br>保存 | 維持 | 当該要素がどの意味を伝えるか | 形の一致だけを確認して意味を見逃す | nodes.meaning/edges.relation/cell_meaningと同じ意味なら参照。要素ごとの追加解釈は保存 / 適用: 主張要素の支持判定に必要 | 手動、checkerは未検査 | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `relation_label`<br>保存 | 条件付き | other_explicitの関係を読者がどう読むか | 統計的関連などを関係語彙外として省く・因果に誤分類する | 制御relationだけでは不足時の補足。caption/legendへ生成可 / 適用: 関係型だけでは解釈が一意でない場合 | 手動。diagram checkerはrelation_labelを必須にしない | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `origin`<br>保存 | 維持 | 原資料保持・正規化・独自追加のどれか | 原資料に支持される独自追加を原著者の作成物と誤認する | 図全体のstatusと異なり混合要素の帰属を区別。source_supportから導出不可 / 適用: 主張を担う再構成要素で必要 | 手動G6、機械必須検査なし | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `source_support`<br>保存 / 結合・運用 | 維持 | どの文章・図・表・データがその要素を支持するか | もっともらしいが未支持の矢印を残す | source_idsとexact locatorだけでは解釈の支持内容が不足。originとは統合不可 / 適用: 全主張要素の根拠判定で必要 | 手動G6。現在checkerは図全体のsource joinsだけ | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `正確な要素根拠位置（自然言語項目）`<br>保存 | 維持 | 各矢印・数値の支持をどの箇所で確認するか | 図全体の出典だけで個別要素が支持されたと誤認する | 共通支持なら要素群でまとめ可。図全体locatorと異なる精度なので一律削除不可 / 適用: 主張を担う変換要素で必要 | 手動G6、機械未検査 | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `element.value.unit`<br>保存 / 確認観点 | 条件付き | この値は何の尺度・単位か | 異なる尺度の値を同じ結果として比較する | 全要素で同じなら図またはnumeric record参照で足りる。違う値は別行で保持 / 適用: 値の解釈に影響する該当属性のみ | element_mapは手動。numeric元記録は別担当、ここで新必須を作らない | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `element.value.denominator`<br>保存 / 確認観点 | 条件付き | この割合はどの母数を分母にするか | 割合の対象集合を誤認する | 同じ比率の分母なら図・numeric正本を参照できる。異なる分母は区別。平均や係数の標本数は分母と同一視せず方法・条件から確認する / 適用: 比率・割合・率など分母が数量の意味を説明する場合だけ必要。平均・係数への該当外は未報告と区別 | element_mapは手動。numeric元記録は別担当、ここで新必須を作らない | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `element.value.aggregation`<br>保存 / 確認観点 | 条件付き | この値はどの対象粒度・演算で集約したか | 試行単位と研究単位の値を同列に比較する | 全要素で同じなら図またはnumeric record参照で足りる。違う値は別行で保持 / 適用: 値の解釈に影響する該当属性のみ | element_mapは手動。numeric元記録は別担当、ここで新必須を作らない | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `element.value.time`<br>保存 / 確認観点 | 条件付き | どの時点・期間の値か | 異なる時期の値を同じ条件の結果として扱う | 全要素で同じなら図またはnumeric record参照で足りる。違う値は別行で保持 / 適用: 値の解釈に影響する該当属性のみ | element_mapは手動。numeric元記録は別担当、ここで新必須を作らない | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `element.value.condition`<br>保存 / 確認観点 | 条件付き | どの条件下の観測・導出か | 異条件を同じ効果として比較する | 全要素で同じなら図またはnumeric record参照で足りる。違う値は別行で保持 / 適用: 値の解釈に影響する該当属性のみ | element_mapは手動。numeric元記録は別担当、ここで新必須を作らない | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `element.value.uncertainty`<br>保存 / 確認観点 | 条件付き | この要素の値にどの幅・精度・未報告があるか | 区間や推定を確定値と誤認する | 全要素で同じなら図またはnumeric record参照で足りる。違う値は別行で保持 / 適用: 値の解釈に影響する該当属性のみ | element_mapは手動。numeric元記録は別担当、ここで新必須を作らない | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `導出入力・演算（自然言語項目）`<br>保存 | 条件付き | 表示値をどの引用値からどう計算したか | 増やした精度や正規化の誤りを検証できない | 既存計算/data recordにあるなら参照し同式を二重入力しない / 適用: 導出値を表示する場合 | 手動G6、機械未検査 | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `element review status（自然言語項目）`<br>確認観点 / 保存 | 条件付き | この要素は支持・由来を確認済みか | 一部未確認を図全体passedで隠す | 既存要素レビューの状態を参照し図全体状態と区別 / 適用: 未支持・未確認要素、全要素の確認範囲を示す場合 | 手動G6、機械未検査 | [references/figure-extraction.md](../references/figure-extraction.md)、[references/reconstruction-review.md](../references/reconstruction-review.md)、[references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `未解決の問い（自然言語項目）`<br>確認観点 / 保存 | 条件付き | どの支持・由来が未確定か | pendingだけで次に何を確認すべきか分からない | 既存review findingの問いを参照可 / 適用: 未支持・未確認要素、全要素の確認範囲を示す場合 | 手動G6、機械未検査 | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `repair（自然言語項目）`<br>確認観点 / 保存 | 条件付き | 支持されない要素をどう直すか | 指摘から実装への引継ぎが不明になる | 既存review findingの修正指示を参照可 / 適用: 未支持・未確認要素、全要素の確認範囲を示す場合 | 手動G6、機械未検査 | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## caption / visual_provenance

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `対応原図の有無（自然言語項目）`<br>保存 | 維持 | 同じ関係を原資料が図として報告しているか | 文章から作った解釈を原図の再構成として読ませる | routeだけでは原図を統合のbasisに使ったかと対応図有無を分けられない。scan/candidateから根拠付き生成 / 適用: 再構成・独自統合の帰属判断で必要 | 手動、機械はroute packetの形式しか検査しない | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `原図・再構成・文章由来・独自統合の分類（自然言語項目）`<br>保存 | 維持 | 読者へどの作成者のどの種の表現として示すか | 独自解釈を原資料の報告図と混同する | status/role/element originを正本にし読者向けの分類文は生成。routeだけでは不可 / 適用: 作成者の責任を分ける場合 | 手動role/caption review。機械のkind/routeは代替しない | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## caption

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `キャプションの根拠位置（自然言語項目）`<br>保存 | 維持 | 読者はどの図・文章・データに基づく表現と読むか | 監査を開かない読者が出所を確認できない | 情報源正本とelement_mapの支持位置の短い要約 / 適用: 図の複雑さに比例して必要 | 手動G6必須、checkerはキャプション内容を検証しない | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `キャプションの保持変更群（自然言語項目）`<br>保存 | 維持 | どの要素群を保持・変更・追加したか | 原図から変換した範囲を読者が区別できない | element_map/packetの変更群を短く生成 / 適用: 図の複雑さに比例して必要 | 手動G6必須、checkerはキャプション内容を検証しない | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `キャプションの関係説明（自然言語項目）`<br>保存 | 維持 | 自明でない矢印・ラベルを読者が何の関係と読むか | 統計的関連を因果と誤認する | relation/legendの読者要約を生成 / 適用: 図の複雑さに比例して必要 | 手動G6必須、checkerはキャプション内容を検証しない | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |
| `キャプションの誤りの帰属（自然言語項目）`<br>保存 | 維持 | 独自追加の誤りを誰の責任として読むか | 作成者の解釈誤りを原著者へ帰属する | originと変換範囲から読者向けの責任説明を生成 / 適用: 図の複雑さに比例して必要 | 手動G6必須、checkerはキャプション内容を検証しない | [references/reconstruction-review.md](../references/reconstruction-review.md)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py) |

## plot_split_handoff

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `slide_ids`<br>結合・運用 | 条件付き | 一つのプロット関係をどの複数ページで説明するか | splitを一つのplot rowへ結びたい場合に複数ページを列挙できない | プロットの既存使用関係から生成。単一ページでは既存slide_id/visual_idで足りる / 適用: 一つのプロット行で複数使用を追跡する場合のみ | plot checkerはslide_idまたはslide_idsを受け付ける。strictでは使用ページがリストに含まれ、全列挙ページがmanifestに現れることを検査 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_storyline_plot.py](../scripts/check_storyline_plot.py) |
| `visual_ids`<br>結合・運用 | 条件付き | 一つのプロット関係をどの読者使用で説明するか | 複数ページ・図を同じ関係として計画・監査する参照が弱くなる | プロットの既存使用関係から生成。単一ページでは既存slide_id/visual_idで足りる / 適用: 一つのプロット行で複数使用を追跡する場合のみ | plot checkerは列挙visual_idsがmanifestへ表現されることと、使用が該当plot rowに載ることをstrictで検査 | [references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/check_storyline_plot.py](../scripts/check_storyline_plot.py) |

## manifest

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `visuals`<br>結合・運用 | 条件付き | 一ページに含めた独立した視覚使用をどれも漏らさず契約・根拠・レビューへ対応づける | 旧単一図形式のみでは同一ページ複数原図の個別支持と契約を渡せない。代表図だけが検査される恐れ | 既存visual使用の包含関係の条件付き包絡。正本plot/contract/assetから生成し、独立概念・必須台帳・別IDを追加しない / 適用: 一ページ複数visual使用を渡す場合。単一図は旧平坦形式を維持 | 任意。宣言時はJSONオブジェクトの非空配列、TSVはJSONセル。ページ属性だけ継承し、異なるchild上書き・旧属性混在・再帰・重複visualを拒否 | [references/evidence-visual-contract.md](../references/evidence-visual-contract.md)、[references/presentation-build-contract.md](../references/presentation-build-contract.md)、[scripts/manifest_visuals.py](../scripts/manifest_visuals.py)、[scripts/check_evidence_visual_contract.py](../scripts/check_evidence_visual_contract.py)、[scripts/check_deck_quality.py](../scripts/check_deck_quality.py)、[scripts/check_storyline_plot.py](../scripts/check_storyline_plot.py)、[scripts/check_review_record.py](../scripts/check_review_record.py)、[tests/test_multi_visual_manifest.py](../tests/test_multi_visual_manifest.py) |
