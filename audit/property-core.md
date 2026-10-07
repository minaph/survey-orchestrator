# 根拠・プロット・レビューの項目別監査

対象は239監査行です。属性、包絡、既存の記録区分、自然言語で確認する観点を含みます。新しい必須項目を提案する表ではありません。監査全体の採否と限界は [総括](../PROPERTY_AUDIT.md) を参照してください。

「維持」は意味を保つ判断であり、全案件で独立列や独立レコードを必須にする意味ではありません。「削除候補」は独立した入力・正本を減らす判断です。既存値を失わず参照・導出・統合する方法を、重複・適用条件の欄に示します。現チェッカーの要求と意味上の必要性は別欄です。所在は監査時のファイルを示し、改訂で移動する行番号には依存しません。

## source/report

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `source_id`<br>結合・運用 | 維持 | どの報告を参照したか | 同名文書や改訂版を取り違え、根拠参照が不安定になる | URLで代替できる一件案件もあるが、複数参照・改名では安定IDが有効 / 適用: 条件：複数報告・固定参照 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `canonical_id`<br>結合・運用 | 削除候補 | 同じworkを報告する文書群はどれか | work_idとの対応が保存済みなら独自の意味は失われない | 原意はsame workの報告群。work_idと同じ群なら別名参照・導出できる。URL表記揺れという別概念へ再定義しない / 適用: 任意：既存データ互換や外部識別子対応時 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `url_or_doi`<br>保存 | 維持 | 元報告へ再アクセスできるか | 出典の確認・引用・取得を再現できなくなる | source_idだけでは出所を導けない。DOIとURLは代替・併記可能 / 適用: 意味上：取得可能な出所または同等の参照手掛かり | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `version`<br>保存 | 条件付き | どの版の結果を使ったか | プレプリントと確定版の訂正・値の違いが混ざる | DOIが版を一意に特定する場合は参照で代替可能 / 適用: 条件：版差が意味・再現に影響 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `retrieved_at`<br>保存 | 条件付き | いつ参照可能だった報告を取得したか | 可変Webや消失・更新資料の当時状態を再現しづらい | 不変の刊行物の発行時点とは別。取得ログの参照で代替可 / 適用: 条件：可変資料・更新・監査時点が必要 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `source_type`<br>保存/確認観点 | 条件付き | 領域研究・背景・方法資料等のどの役割か | 工程資料を分野の根拠・件数へ混ぜる | work.design_or_typeは研究設計であり出典役割と異なる / 適用: 条件：異種資料の採用・件数・責任区別 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `locator`<br>保存 | 統合・導出 | 報告全体の補足所在はどこか | 抽出位置がevidenceにある場合には喪失なし。全体の参照区間が必要な場合のみ補足が失われる | 抽出位置としてはevidence.locatorと同義で重複。具体的抽出の正本はevidenceへ / 適用: 任意：報告全体の補足所在 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |

## work/study

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `work_id`<br>結合・運用 | 維持 | 複数報告が同じ研究・論証か | 報告件数が研究件数へ混ざり再掲で支持を水増しする | canonical_idと同群なら一つの正本。報告一件だけでも論証単位と文書単位が異なる場合がある / 適用: 条件：研究単位の集計・多報告・複数根拠 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `identity`<br>保存 | 条件付き | 何を一つの研究・論証と判断したか | 同じ題名の別研究や複数実験の境界判断を説明できない | sample/method/reportsから要約できるが、同一性の判断自体は根拠に基づく記述 / 適用: 条件：同一性・単位に曖昧さ | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `design_or_type`<br>保存/確認観点 | 条件付き | どの設計・論証の型が何を支えるか | 因果・記述・概念論証の評価基準を選びづらい | methodsの説明から読める場合は短い分類と説明を一箇所で管理できる / 適用: 条件：設計差が評価・推論を変える | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `reports[]`<br>結合・運用 | 統合・導出 | 同じ研究の報告群はどれか | 報告群の対応自体を消すと版・重複の確認ができない | 報告からworkへの正本の対応関係があれば逆引き可。抽出済みevidenceのみから導くと未抽出報告を失う / 適用: 意味上：報告群の対応。物理的逆引きリストは任意 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `sample_or_corpus`<br>保存 | 条件付き | どの集団・コーパス・単位についての研究か | 転用・比較の可否や標本の違いを判断できない | methods説明に統合可能だが複数結果の共有文脈として継承すると記述負担を抑えられる / 適用: 条件：対象・標本が主張を限定 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `methods`<br>保存 | 統合・導出 | 研究全体で共有する方法は何か | 複数結果ごとに同じ方法説明を繰り返す負担が増える | evidence.method_or_basisとは共通文脈と結果固有差分として分担。差分がなければ参照でよい / 適用: 条件：複数結果に共有する方法・方法が推論を限定 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |

## evidence

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `evidence_id`<br>結合・運用 | 維持 | どの抽出結果を複数の主張が使うか | 結果と支持命題の参照が不安定になり再利用時に再抽出する | 一件の根拠を一件の主張へ埋込む小案件では独立IDを省ける / 適用: 条件：複数根拠・再利用・監査参照 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `work_id`<br>結合・運用 | 統合・導出 | この結果はどの研究・論証に属するか | 同研究の複数結果と独立研究の結果を区別できない | source→work対応が確定していれば導出可。複数workを含む報告では結果別の対応が必要 / 適用: 条件：報告と研究が一対一でない・研究単位集計 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `source_ids[]`<br>結合・運用 | 維持 | 抽出した観察・論証をどの報告が記載するか | 同研究の異なる版の結果を裏付けと誤認する | work.reports[]は候補報告群であり、実際に使った出典を導けない / 適用: 意味上：抽出結果の出所 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `locator`<br>保存/結合・運用 | 維持 | 出典のどの箇所がこの観察を支えるか | 引用の支持範囲を確認できず全論文を読み直す | source.locatorの抽出位置はここへ集約。evidenceの再掲を同一観察として照合可能 / 適用: 意味上：具体的な支持箇所 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `construct`<br>保存/確認観点 | 条件付き | 何の概念についての結果か | 信頼・依存等の異なる構成概念を同じ列で比較しやすい | workの共有概念やresult説明から継承可。操作・結果で意味が変わる場合は結果別に保持 / 適用: 条件：概念差が比較・解釈を変える | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `method_or_basis`<br>保存 | 統合・導出 | この結果を得た手順・論証根拠は何か | 結果固有の分析・尺度・比較条件を研究全体の方法と誤認する | work.methodsへの参照と結果固有の差分を保持。全文の三重複写は不要 / 適用: 条件：結果の意味や強さを変える方法 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `condition_or_comparator`<br>保存/確認観点 | 条件付き | どの条件・何との比較で成立したか | 比較条件の異なる数値を同等に扱い転用を強める | 共通条件の継承可。ただし根拠から条件へ辿れる必要がある / 適用: 条件：比較・条件が意味を限定 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `result_or_argument`<br>保存 | 維持 | 情報源は何を観察・論証したか | 結果と調査側の解釈を分離できない | claim_textと同文でも出典が述べたという責任は別。正本の参照で同文の管理を減らせる / 適用: 意味上：根拠の内容 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `null_or_counterexample`<br>保存/確認観点 | 条件付き | 主張を弱める結果・反例はあるか | 確認済みの反証を落とす、または未確認を不存在と誤認する | result_or_argumentの中で明示可能。独立欄は反証探索・横断比較に有効な場合のみ / 適用: 条件：反証・null・探索済み情報状態が判断を変える | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `limitation`<br>保存/確認観点 | 条件付き | この情報源・結果の限界は何か | 未測定・標本限界を見失い主張を強める | transferabilityやclaim境界と内容が重なる場合は正本参照。源の限界と調査の適用境界は区別 / 適用: 条件：意味を変える限界・不明点 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `transferability`<br>確認観点/保存 | 統合・導出 | 現在の調査対象へ転用できる条件は何か | 情報源の対象と調査の対象の違いを評価できない | limitation/claim.boundary_conditionsへ統合可能。ただし調査への適用判断であり源の結果ではない / 適用: 条件：文脈・集団・課題を跨ぐ主張 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |

## claim

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `claim_id`<br>結合・運用 | 維持 | どの命題を根拠・図・プロットが参照するか | 主張の修正・再利用時に支持対象を取り違える | 小さな自由記述案件は位置参照で代替可能。長期・複数成果物では安定IDが有効 / 適用: 条件：複数参照・継続改訂 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `claim_text`<br>保存 | 統合・導出 | 調査が支持・限定する正確な命題は何か | 主張を消すと根拠を何のために比較するか不明になる | reader_wordingやmanager_interpretationと同命題なら正本一箇所。表現・責任・範囲が異なるときだけ分ける / 適用: 意味上：命題。三つの本文を常時別保存する必要はない | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `claim_type`<br>確認観点/保存 | 条件付き | 記述・比較・因果・規範・方法のどの論理形式か | 因果・規範に必要な追加根拠の確認をしづらい | 命題の表現から分類を読める場合は任意。曖昧な形式・横断レビューなら独立分類が有効 / 適用: 条件：論理形式が受入基準を変える | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `claim_role`<br>保存/確認観点 | 条件付き | 情報源の報告・方法評価・研究間パターン・解釈・推奨の責任は誰にあるか | 調査側の解釈を出典結果として見せやすい | claim_typeとは異なる。文・出典関係で責任を明示できても解釈等は現定義で条件付き記載 / 適用: 条件：survey_interpretation/recommendation/曖昧なcross_study_pattern | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `evidence_ids[]`<br>結合・運用 | 維持 | どの具体的な根拠がこの命題を支持するか | 広い文献引用だけで段落全体を裏付けたように見える | 引用側に正本の支持関係があれば逆引き可。source_idsだけでは支持箇所と関係を代替できない / 適用: 意味上：主張と具体的根拠の関係 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `counterevidence_ids[]`<br>結合・運用/確認観点 | 条件付き | どの根拠が主張を否定・限定するか | 反証を支持と同列の引用として混ぜる | evidence関係の支持/限定の説明へ統合可能。確認済みの反証を消さない / 適用: 条件：中心主張の反証・探索状況が重要 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `boundary_conditions[]`<br>保存/確認観点 | 条件付き | 主張はどの範囲・条件で成立するか | 源の結果からより広い命題へ飛躍する | 根拠の限界・条件を参照できるが、複数根拠から導いた主張固有の境界は単純な和集合でない / 適用: 条件：主張の意味・強さを変える境界 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `certainty`<br>保存/確認観点 | 条件付き | この根拠群が命題をどれほど確かに支えるか | 件数の多さを確実性と同一視し不確実な中心回答を断定する | 単一研究のquality/riskと異なり、根拠群・命題の評価。本文に統合可 / 適用: 条件：中心・高リスク命題・確実性評価を行う調査 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `manager_interpretation`<br>保存 | 統合・導出 | 出典から主張へどの追加命題・橋渡しを採用したか | 源の観察と調査側の推論を混同する | claim_textに橋渡しが明示され同じ内容なら複写不要。追加の理由・推論・対案が必要な場合のみ別記述 / 適用: 条件：出典直接報告にない解釈の説明 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `reader_wording`<br>保存 | 統合・導出 | 読者にどの表現で伝えるか | 読者向けの限定・言い換えが正確な命題とどう違うかを確認しづらい | claim_textと同文なら一箇所管理。成果物から導出可能な現表示と意図する表現を区別 / 適用: 条件：正本命題と読者向け表現が異なる | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |

## numeric属性群

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `numeric`<br>確認観点/導出 | 統合・導出 | 数値属性が適用されるか | 欠測と定性的な該当外を区別しづらい | 構造化数値型や根拠説明から導出可。既存boolは適用確認の任意の印 / 適用: 条件：定量/定性混在、適用可否が曖昧 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `numerator`<br>保存 | 条件付き | 比率・割合の分子は何か | 分母だけでは比率の元の件数を確認できない | 比率と分母だけから丸め前件数を常に復元できない。単独係数・連続値には該当しない / 適用: 条件：比率・割合・件数の組で意味を説明する量 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `denominator`<br>保存 | 条件付き | 比率・割合・率の対象母数は何か | 集団サイズ・重複・割合の意味を失う | 全quant必須ではない。回帰係数、温度、単独平均などに分母を製造しない / 適用: 条件：比率・割合・率、又は標本数が意味を変える | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `unit`<br>保存 | 条件付き | 何の単位・尺度の数値か | 異単位の値を比較し意味を取り違える | 変数の共有定義から継承可。標準化係数など無次元も意味を保持 / 適用: 条件：量を解釈する尺度・単位 | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `aggregation_level`<br>保存/確認観点 | 条件付き | 人・試行・研究等のどの単位で集計したか | 疑似反復・研究数の水増し・平均化を取り違える | workの標本単位からは結果固有の集計水準を常に導けない / 適用: 条件：集計や重複が意味を変える | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |
| `uncertainty`<br>保存/確認観点 | 条件付き | 推定値の区間・ばらつき・測定不確かさは何か | 点推定を確実な差として扱う | claim.certaintyは根拠群の判断であり数値の区間とは異なる。plotの不確実性とは参照で共有 / 適用: 条件：推定・ばらつき・不確かさが意味を変える | 専用coreレコード検査なし。図・manifestの同名属性検査をcoreの必須性へ転用しない | [references/evidence-model.md](../references/research/evidence-model.md) |

## storyline_plot

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `plot_version`<br>結合・運用 | 維持 | 制作・レビューはどの版の構成を対象としたか | 古いレビューを更新後の物語に適用する | レビューの同名キーは同じ版の参照。版IDまたは確定スナップショットへ一本化 / 適用: 条件：改訂・制作・正式レビューの結合 | scripts/check_storyline_plot.py:114-117; strict manifestは189-192で一致要求 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `plot_scope`<br>保存/確認観点 | 維持 | 参考物の構成か調査の主張か | 参考物を分野根拠として誤結合する | ファイルの明示スコープから導出可能だが持出しに強い区別 / 適用: 条件：複数対象・正式manifest結合 | scripts/check_storyline_plot.py:118-121 全モードで定義域、strict manifest target_survey要求 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `plot_status`<br>保存/結合・運用 | 維持 | 仮案・検証済み・統合等のどの作業局面か | 初期仮説を最終回答として制作する | 行のsource_stateやレビューstatusとは責任が違う。最新状態は工程結果から導出し当時判断は版と保持 / 適用: 条件：複数局面・正式制作 | scripts/check_storyline_plot.py:122-125 全モードで定義域、strict verified/synthesis要求 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `rows（別名slides/items/plot）`<br>結合・運用 | 維持 | どの行群が一つのプロットを構成するか | JSON上の行集合を特定できない | 別名は同じ配列の代替で多重保持しない。Markdown表なら包絡列不要 / 適用: 条件：構造化プロット入力 | scripts/check_storyline_plot.py:45-54,126-129 空でない配列、非object行不許可 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `audience`<br>保存 | 統合・導出 | 誰の理解・判断のための構成か | 複数読者で用語・密度・説明の判断が変わる | G0タスク設定と同じなら参照/継承し二重管理しない / 適用: 条件：タスクと異なる読者・単独持出し | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `central_question`<br>保存 | 統合・導出 | 全体で何へ答えるか | 節が問いへ収束するか判断できない | G0の問いと同値なら正本一つ。各節/行質問とは範囲が異なる / 適用: 意味上：調査の主問い。独立コピーは任意 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `central_takeaway`<br>保存 | 統合・導出 | 現在支持できる全体回答は何か | 最終統合の主張範囲を確認できない | 中心claimへの参照で同命題コピーを減らす。初期の仮説と確定claimの責任は区別 / 適用: 意味上：全体回答または未確定の説明 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `review_concept`<br>保存/確認観点 | 条件付き | 誰にどの変化を、どの統合と境界で示すか | 構造化欄だけでは初見レビューの背景を読む負担が増える | audience/central_question/central_takeaway/範囲をまとめた短い説明。第二の結論欄にしない / 適用: 任意：形成レビューの理解支援 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `plot_row_id（別名row_id/id）`<br>結合・運用 | 維持 | 改訂しても同じ説明行を追えるか | スライドの並替えで指摘・図・根拠の参照が壊れる | slide_idとは構成行と出力ページの違い。一件対応なら運用上同値にできるが独立意味は条件付き / 適用: 条件：反復改訂・正式manifest結合 | scripts/check_storyline_plot.py:134-145 全モードで非空・一意要求 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `section_id（別名sectionId）`<br>結合・運用 | 条件付き | どの節に属し、何を累積するか | 節を跨ぐブロックの重複や局所回答を追いづらい | フラットな一節資料なら同じ値の運用キーで十分。独立節レコードを増やす必要はない / 適用: 条件：複数節・正式検査 | scripts/check_storyline_plot.py:135-157 全モード非空、blockは一section、manifest一致 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `section_question`<br>保存 | 統合・導出 | 節の下位質問は何か | 複数行の共通目的をBottomから再構成する負担が増える | 単一行節ではTと同義。節ごとの一箇所へ集約・継承可能 / 適用: 条件：節が複数行を束ねる・局所問いが読めない | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `section_answer`<br>保存 | 統合・導出 | 節全体で何を答えたか | 複数根拠の局所統合を単一行Bottomと誤認する | 単一行節のBottomと同値ならコピー不要。節単位の正本へ集約 / 適用: 条件：複数行の局所回答を明示する必要 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `transition_question`<br>保存 | 統合・導出 | なぜ次の節へ進むか | 節間の推論飛躍を診断できない | 節末Nextが同内容なら二重欄不要。複数Nextを統合した移行時のみ別記載 / 適用: 条件：Nextだけでは節間移行が説明できない | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `section_purpose`<br>確認観点/保存 | 条件付き | 節の役割がnarrative_jobから分かるか | 役割を明示する価値がある場合だけ情報が失われる | 既存定義でnarrative_job不足時のみ。問い・回答で明らかなら削除できる / 適用: 条件：narrative_jobでは不足 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `slide_id（slide_ids/slideId/slideIds）`<br>結合・運用 | 条件付き | プロット行をどの出力ページへ展開したか | 構成とレンダリングを照合できない | 行とページが一対一でも並替え・分割時は役割差がある。複数IDは同じ対応関係の配列 / 適用: 条件：発表資料の出力との結合。G0/非発表では不要 | scripts/check_storyline_plot.py:198-205 strict manifestはslide_id又はslide_ids必要 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `evidence_block_id（別名evidenceBlockId）`<br>結合・運用 | 条件付き | 複数行がどの研究・比較・統合操作を共有するか | 研究カード/結果/境界等の一括修正と独立研究計数が難しくなる | 一行一根拠ならclaim/work/行のグループと同値で独立レコード不要。比較ブロックは複数workを扱える / 適用: 条件：意味上の共有・展開。現検査では全行 | scripts/check_storyline_plot.py:135-157 全モード非空、manifest一致 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `T（title/question）`<br>保存 | 維持 | 読者がここで知る必要は何か | 行の目的・質問を説明できない | 出力題名と同内容なら参照/生成。headingのみの行では固有の認知目的でよい / 適用: 意味上：行が答える問い・役割 | scripts/check_storyline_plot.py:158-168 strict非空 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `B（body）`<br>保存 | 維持 | 何を行い、観察し、推論したか | 回答の根拠を説明できない | evidence/claimの長文コピーではなく行の必要な説明。元結果の正本は根拠に保持 / 適用: 条件：読者に必要な説明。表紙等は役割を記す | scripts/check_storyline_plot.py:158-168 strict非空 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `Bottom（bottom/takeaway）`<br>保存 | 統合・導出 | この根拠から境界付きで何が答えられるか | 事実の列挙だけになり調査としての判断が不明 | 一行claim.reader_wordingと同値なら正本参照。行の結論と節/全体結論は異なることがある / 適用: 条件：説明の局所回答 | scripts/check_storyline_plot.py:158-168 strict非空 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `Figure（figure_relation/figureRelation）`<br>保存/確認観点 | 維持 | 本文だけでは確認できないどの関係を図が示すか | 候補図の有用性や本文との重複を説明できない | Figureとfigure_relationは同義の保存別名。両方を独立維持しない / 適用: 条件：意味を担う図。図なしは不要理由を一度示す | scripts/check_storyline_plot.py:158-168 strict非空、代替キー受理 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `Next（next_question/nextQuestion）`<br>保存 | 条件付き | この回答からなぜ次の問いへ進むか | 読者の接続・残る問いを説明できない | transition_questionと同義の節末は一箇所。next_research_actionは作業であり通常は別 / 適用: 条件：接続・最後の残る問いに役割がある | scripts/check_storyline_plot.py:158-168 strict非空。終端に機械上の文字列は必要 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `narrative_job`<br>確認観点/保存 | 条件付き | この行は定義・方法・比較・統合等の何を担うか | タイトルから役割が読めない複雑な構成で修正の種類が曖昧になる | T/B/Bottomから明らかなら独立欄不要。reader_roleとはエピステミック責任の違い / 適用: 条件：役割の明示が設計/修復を変える | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `presenter_note`<br>保存 | 条件付き | 何へ注目し、どこまで推論し、次へどう接ぐか | 発表時の注目誘導・留保が不足する | 全文台本やBの言換えなら不要。発表に固有の働きがあるときだけ / 適用: 条件：発表時の説明に必要、非発表では不要 | 検査なし。条件付きのプロジェクト契約以外は欠如を機械不合格にしない | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `reader_role`<br>確認観点/結合・運用 | 統合・導出 | 文献紹介か調査独自統合か | 正本がvisual/manifestにあれば削除しても役割は保持 | 図の経路許可に関わる役割はmanifest/visualの正本から参照。plot独立コピーは無用 / 適用: 任意：制作への転記・派生表示 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `evidence_class`<br>確認観点/結合・運用 | 削除候補 | この行/図は何の根拠クラスか | 意味の定義がないため独自に失う判断を確認できない | plot本文に意味やnarrative_job/reader_roleとの差が定義されていない。manifest分類の参照で足りる / 適用: 任意：既存manifestの派生表示のみ | plot固有の分類を新設して正当化しない | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `claim_refs[]（claim_ids/claimIds）`<br>結合・運用 | 維持 | この行がどの主張を用いるか | 複数ページの主張修正と証拠追跡が不安定になる | B/Bottomの文言から一般知識で一致推測せず、固定関係を保持。小案件は出典付き文章で代替 / 適用: 条件：主張付き資料・複数参照 | scripts/check_storyline_plot.py:206-211 strictでmanifest.claim_idsを含む必要 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `source_refs[]（source_ids/sourceIds）`<br>結合・運用 | 統合・導出 | この行の出所はどの報告か | claimがない方法・引用・背景行の出所を失う | 全てがclaim→evidence→sourceで辿れる場合は導出可。直接引用や背景源だけは別関係を保持 / 適用: 条件：直接出典。支援claimだけなら導出 | scripts/check_storyline_plot.py:212-217 strictでmanifest.source_idsを含む必要 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `visual_ids[]（visualIds）`<br>結合・運用 | 維持 | この行がどの図を採用するか | 図を差替え・分割すると行と図の対応が壊れる | Figureは意味の説明、visual_idsは同一性で別。manifestが対応正本なら逆引き可 / 適用: 条件：図付き資料・生成結合 | scripts/check_storyline_plot.py:218-220 strictでmanifest.visual_idを含む必要 | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `source_state`<br>確認観点/保存 | 条件付き | この行の根拠は未確認・アクセス不可・検証済みか | 未確認のプロットを確定回答と誤認する | 関連根拠の状態から単純には導けない混在行がある。正本参照又は行固有の保留理由 / 適用: 条件：探索中・混在・アクセス問題 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `boundary`<br>保存/確認観点 | 統合・導出 | 読者に見えるこの行の結論範囲は何か | 主張の適用条件を見失う | claim.boundary_conditions/evidence.limitationの正本を継承、行で限定をさらに変える場合のみ別保存 / 適用: 条件：意味を変える境界 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `uncertainty`<br>保存/確認観点 | 統合・導出 | この行の不確実性・未確認事項は何か | 暫定回答を確定主張に見せる | 定量uncertainty、claim.certainty、根拠の不明情報を参照。異なる意味は区別して表示 / 適用: 条件：回答の強さを変える不確実性 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `visual_candidate`<br>結合・運用 | 削除候補 | どの図候補がこの行を支え得るか | 候補台帳への参照があれば独自の意味は失われない | visual_ids/Figure/候補台帳との独立役割が未定義。候補の正本へ参照し複製レコードを削除 / 適用: 任意：候補への参照が必要な探索局面 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `source_visual_route`<br>結合・運用 | 統合・導出 | 採用図は原図・再構成等のどの経路か | visual正本がある場合意味の喪失なし | visual契約/manifestに経路正本。plotは参照/制作時導出で整合 / 適用: 任意：経路の派生表示 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `rrm_focus`<br>確認観点 | 条件付き | どの読解観点が次の判断を変えるか | 検索・修復の焦点が有用な場合のみ明示の利点を失う | T/B/根拠の関係で焦点が分かる場合は不要。六つの完了欄へしない / 適用: 任意：検索・修復・読者向け設計に寄与 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `transfer_note`<br>保存/確認観点 | 削除候補 | 境界以外に何の転用判断を保持するか | 現在の定義では独自に失う意味を特定できない | boundary/claim.boundary_conditions/evidence.transferabilityと同内容。本文に追加役割の定義なし / 適用: 任意：既存記録の読出し別名 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `unresolved_question`<br>確認観点/保存 | 条件付き | 現在の回答を確定するために何が未解決か | 必要な検索・収集の焦点を失う | Nextが読者の次問の場合は意味が異なる。同じ調査問なら一箇所管理 / 適用: 条件：未解決の問いが回答を変える | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `next_research_action`<br>保存/結合・運用 | 統合・導出 | 不足を埋めるために次に何をするか | 問いが残っても検索・抽出・検証へ進めない | 管理者の作業依頼へ参照可能。Nextは読者の接続であり行動とは別 / 適用: 条件：調査途中・更新。節/ブロックで共有可 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |
| `g4p_verdict`<br>保存/結合・運用 | 維持 | 進行・修正・縮小・停止のどれを選ぶか | 形成レビューの次の動きをformal passへ誤写する | 正式plot_review.statusとは意味と工程が異なる。既存変更記録の一箇所で保持 / 適用: 条件：G4-P実施時 | 検査なし | [references/storyline-plot.md](../references/presentation/storyline-plot.md) |

## review_record

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `plot_review`<br>結合・運用/保存 | 維持 | どの構成版についてレビューしたか | 構成と読者表示の判断責任が曖昧になる | 一つのレビュー文書内の章として統合可。独立ファイル/別エージェントは不要 / 適用: 条件：構成付き資料の正式レビュー | scripts/check_review_record.py:182-186 全モードでobject必要 | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `reader_review`<br>結合・運用/保存 | 維持 | 読者として表示・理解を確認したか | 意味上正確でも読者が読めない資料を公開する | plot_reviewと同じ担当・scopeでも判定対象は異なる。文書/記録を一つにできる / 適用: 条件：読者向け成果物の正式レビュー | scripts/check_review_record.py:183-189 全モードでobject必要 | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `deterministic`<br>保存/結合・運用 | 維持 | 必要な形式検査を実施して合格したか | 当該観点の未完・阻害を総合の高得点で相殺しやすい | 実際の検査結果へ参照。statusをコピーして合格の証拠としない / 適用: 条件：当該観点が適用される成果物 | scripts/check_review_record.py:245-258 object/status必須、strict passed | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `semantic`<br>保存/結合・運用 | 維持 | 出典が読者の命題を支え概念の境界が妥当か | 当該観点の未完・阻害を総合の高得点で相殺しやすい | plot/readerと観点が重なるが独立した意味上の阻害を相殺しないため一判定を要約する / 適用: 条件：当該観点が適用される成果物 | scripts/check_review_record.py:245-258 object/status必須、strict passed | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `fidelity`<br>保存/結合・運用 | 維持 | 原図・再構成・転用が出典の関係を保持するか | 当該観点の未完・阻害を総合の高得点で相殺しやすい | semanticの下位観点に統合可能だが対象図の比較結果を参照して独立阻害を守る / 適用: 条件：当該観点が適用される成果物 | scripts/check_review_record.py:245-258 object/status必須、strict passed/not_required/not_applicable | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `visual_review`<br>保存/結合・運用 | 維持 | 実レンダリングで図・文字・関係が読めるか | 当該観点の未完・阻害を総合の高得点で相殺しやすい | reader_reviewとの重複がある。表示観察の結果への参照で個別手順を重複しない / 適用: 条件：当該観点が適用される成果物 | scripts/check_review_record.py:245-258 object/status必須、strict passed/not_required/not_applicable | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `release`<br>導出/結合・運用 | 統合・導出 | 全適用条件の状態が公開条件を満たすか | 要素状態があれば同じ集約結果を再計算できる | 文書では論理積として定義される派生値。手入力の独立状態は矛盾リスク / 適用: 条件：正式公開判定・現検査入力 | scripts/check_review_record.py:190-194 必須、strict passed;259-265 component未解決との矛盾を検査 | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## plot_review/reader_review

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `status`<br>保存/結合・運用 | 維持 | 当該版と範囲を公開できると判断したか | 個別指摘の件数だけでは未完・阻害を判別できない | 局所verdictの最大値だけで自動導出しない。中心性・修正完了を踏まえた当時判断 / 適用: 条件：正式レビューの公開判断 | scripts/check_review_record.py:207-212 passed/pending/blocked、strict passed | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `scope`<br>結合・運用/保存 | 維持 | 何を確認した評価か | 対象外ページへ合格を拡張する | 構成/表示が同じ範囲なら一箇所の共有scopeを再利用できるが、別範囲を上書きしない / 適用: 意味上：評価の適用範囲 | scripts/check_review_record.py:67-70 object必須 | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `findings`<br>保存/結合・運用 | 条件付き | どの観点で何が問題・十分と判断されたか | 修復と異議の対象を追跡できない | 全合格項目のstrong行は不要。実質的指摘・根拠・変更判断を既存変更記録へまとめられる / 適用: 条件：意味的判断・問題・修復を記録。空配列可 | scripts/check_review_record.py:120-123 省略は[]、arrayなら可 | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## plot_review

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `plot_version`<br>結合・運用 | 維持 | 現行構成と同じ版の評価か | 旧版の合格で新構成を公開する | storyline_plot.plot_versionの参照で同じ値。版を複製せず対象版を参照 / 適用: 条件：構成版との結合 | scripts/check_review_record.py:213-220 非空、期待版との一致 | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## plot_review/reader_review.scope

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `coverage`<br>保存/確認観点 | 維持 | 全件か事前標本か | 標本レビューを全件合格として見せる | checked集合と母集団から導出可だが全件/標本の計画を記録する場合は当時の方針 / 適用: 条件：範囲の解釈・正式検査 | scripts/check_review_record.py:74-78 all/sample必須 | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `rows（plot_row_ids）`<br>結合・運用 | 統合・導出 | どの構成行を確認したか | 複数出力ページを束ねる構成の確認範囲が不明になる | manifestの行-page対応から導出可。一対一の全件なら列挙を生成し二重入力しない / 適用: 条件：構成レビュー・行固有の指摘 | scripts/check_review_record.py:79-80 plot_review非空; all strictは対象全行含有 | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `pages（slide_ids）`<br>結合・運用 | 統合・導出 | どのレンダリング済みページを見たか | 実際に見ていない分割ページへ評価を適用する | rowsから一意に展開できれば生成可。ただし部分ページの確認は自動補完で全件へ拡張しない / 適用: 条件：表示・ページ付き指摘・正式検査 | scripts/check_review_record.py:81-82 両review非空; all strictは全page含有 | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `items（claim_or_visuals）`<br>結合・運用 | 条件付き | どのclaim/visualを確認範囲としたか | 一部の項目評価を全ての主張・図へ拡張する | scope.rows/pagesから当該pageの全項目を調べた場合だけ導出。findingsは不具合だけで全確認範囲を導けない / 適用: 条件：claim_or_visualで指摘する場合 | scripts/check_review_record.py:73,98-100,147-152 scope.itemsとexpected_itemsへの所属 | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## plot_review.scope

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `central_rows`<br>結合・運用/確認観点 | 条件付き | 標本にも必ず含む中心経路はどれか | 通常標本だけ見て中心の誤りを見逃す | central claim/plot経路から参照可能。全件時は不要 / 適用: 条件：標本の構成レビュー | scripts/check_review_record.py:101-106 strict sample plot_reviewで非空かつrows部分集合 | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## finding

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `row`<br>結合・運用 | 条件付き | 指摘はどの構成行に属するか | 行の並替えで修正対象が失われる | claim_or_visualとの代替。pageから一意なら生成、同時二入力は不要 / 適用: 条件：rowで対象を指定するとき | scripts/check_review_record.py:132-154 rowとclaim_or_visualは非空一方だけ | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `claim_or_visual`<br>結合・運用 | 条件付き | 指摘はどの主張・図を対象にするか | 複数pageを跨ぐ意味・図の修正が不安定になる | rowの代替として指定。複数対象を一つの混合ID欄で示す意味は項目型と確認 / 適用: 条件：itemで対象を指定するとき | scripts/check_review_record.py:132-152 rowと排他、scope.itemsとexpected_items所属 | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `page`<br>結合・運用 | 条件付き | どの出力箇所で問題が現れたか | 分割行・複数表示の局所問題を修復できない | 一対一rowならmanifestから生成。非発表文書は節/段落のlocatorへ自由記述し、このcheckerを適用しない / 適用: 条件：発表の局所指摘 | scripts/check_review_record.py:128-131,155-158 全finding非空かつscope.pages所属 | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `question`<br>確認観点/保存 | 維持 | どの意味・理解の問いを評価したか | verdictだけでは何に対する判断か分からない | 実際の観察・根拠・判断をquestionと修復文の文脈で説明することは可能。問いだけで評価根拠が残るとは限らない / 適用: 意味上：評価の観点と判断の理由が読める記述 | scripts/check_review_record.py:128-131,159-160 全finding非空 | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `verdict`<br>保存 | 維持 | その項目は十分・脆弱・阻害のどれか | 修正優先度・中心経路の未完判断ができない | 修正文から読める場合もあるが、局所評価と全体statusは違う / 適用: 条件：局所findingを作る | scripts/check_review_record.py:161-162 strong/adequate/fragile/blocked | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `repair`<br>保存/結合・運用 | 条件付き | 何を直すか、直す必要がないか | 指摘から実装へ渡す内容が不明になる | 既存作業依頼への参照で同じ修復文を再保存しない。問題なしならnone / 適用: 条件：修復が必要。合格項目にはnoneでよい | scripts/check_review_record.py:163-164 全finding非空、none受理 | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `recheck`<br>保存/確認観点 | 条件付き | 修復後・変更後に何を再確認するか | 当てずっぽうの修復で同じ問題が残る | 全ての合格観察に同じ定型を埋める必要なし。変更・修復時は有効、無修復は不要の理由を一度 / 適用: 条件：修復・意味を変える改訂後の確認 | scripts/check_review_record.py:165-166 全finding非空。none/not_needed等非空は形式上受理 | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## reader_review

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `score`<br>導出/保存 | 削除候補 | 複数案や版の品質をどの共通尺度で要約するか | 比較目的がない案件では公開可否も意味も失わない | dimensionsの点から正規化導出可。固定100点/配点の較正根拠なし。単なる数値化なら削除 / 適用: 任意：利用者が比較尺度を必要とし基準を合意した場合 | scripts/check_review_record.py:267-275 存在時だけfinite0..100、省略はstrictでも警告のみ | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `denominator`<br>導出/保存 | 統合・導出 | 正規化の元の適用配点合計はいくつか | 採点をしている場合だけ適用外軸の比較が不透明になる | 適用dimensions配点から導出。定量根拠のdenominatorとは別の意味 / 適用: 条件：scoreを記録する場合のみ | scripts/check_review_record.py:271-273 score存在時positive finite必須 | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `dimensions`<br>確認観点/保存 | 条件付き | どの読者品質軸が弱いか | 数値を消しても観点別の質的理由を残せば判断は失わない | 6観点の質的findingへ統合可。固定配点の別レコードは不要 / 適用: 任意：観点別の比較・評価を記録 | 検査なし。現checkerはdimensionsのキー・和・配点を検査しない | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## reader_review.dimensions

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `visual`<br>確認観点 | 条件付き | 図の役割・可読性が理解を助けるか | 図があるだけで十分と判定しやすい | 観点自体はfindingの理由に残せる。独立の点数は比較目的があるときだけ / 適用: 条件：当該観点が読者の利用に関わる | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `narrative`<br>確認観点 | 条件付き | 局所回答が結論へ累積するか | 根拠の列挙で統合したことにする | 観点自体はfindingの理由に残せる。独立の点数は比較目的があるときだけ / 適用: 条件：当該観点が読者の利用に関わる | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `navigation`<br>確認観点 | 条件付き | 現在位置・移行が読めるか | 読者の接続の問題を意味誤りと混同する | 観点自体はfindingの理由に残せる。独立の点数は比較目的があるときだけ / 適用: 条件：当該観点が読者の利用に関わる | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `transfer`<br>確認観点 | 条件付き | 境界内で結果を利用できるか | 転用の理解・判断の不足を見失う | 観点自体はfindingの理由に残せる。独立の点数は比較目的があるときだけ / 適用: 条件：当該観点が読者の利用に関わる | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `evidence_fit`<br>確認観点 | 条件付き | 主張と根拠表示が適合するか | 美観を根拠の十分さと混同する | 観点自体はfindingの理由に残せる。独立の点数は比較目的があるときだけ / 適用: 条件：当該観点が読者の利用に関わる | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `accessibility`<br>確認観点 | 条件付き | 対象読者が投影・共有後に読めるか | 制作環境だけで読める資料を公開する | 観点自体はfindingの理由に残せる。独立の点数は比較目的があるときだけ / 適用: 条件：当該観点が読者の利用に関わる | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## deterministic component

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `status`<br>保存/結合・運用 | 維持 | 必要な形式検査を実施して合格したか | 同上の観点が未完か区別できない | 同じ意味のflat statusはcomponent.statusの別名。まとめた報告から導出できるのは形式検査だけ / 適用: 条件：正式レビュー包絡の要素 | scripts/check_review_record.py:245-258 object/status必須、strict passed | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## semantic component

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `status`<br>保存/結合・運用 | 維持 | 出典が読者の命題を支え概念の境界が妥当か | 同上の観点が未完か区別できない | 同じ意味のflat statusはcomponent.statusの別名。まとめた報告から導出できるのは形式検査だけ / 適用: 条件：正式レビュー包絡の要素 | scripts/check_review_record.py:245-258 object/status必須、strict passed | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## fidelity component

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `status`<br>保存/結合・運用 | 維持 | 原図・再構成・転用が出典の関係を保持するか | 同上の観点が未完か区別できない | 同じ意味のflat statusはcomponent.statusの別名。まとめた報告から導出できるのは形式検査だけ / 適用: 条件：正式レビュー包絡の要素 | scripts/check_review_record.py:245-258 object/status必須、strict passed/not_required/not_applicable | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## visual_review component

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `status`<br>保存/結合・運用 | 維持 | 実レンダリングで図・文字・関係が読めるか | 同上の観点が未完か区別できない | 同じ意味のflat statusはcomponent.statusの別名。まとめた報告から導出できるのは形式検査だけ / 適用: 条件：正式レビュー包絡の要素 | scripts/check_review_record.py:245-258 object/status必須、strict passed/not_required/not_applicable | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## deterministic検査記録

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `deterministic_status`<br>導出/結合・運用 | 統合・導出 | 検査が完了し阻害があるか | 実行結果と要素statusがあれば追加情報なし | deterministic.statusと同意味の別名。正本の結果へ参照し二重管理しない / 適用: 任意：検査結果の既存形式への対応 | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `checks_run`<br>結合・運用 | 統合・導出 | どの検査を実行したか | 未実施を合格と誤認する | 検査ログから導出・参照可 / 適用: 条件：形式検査の実施範囲 | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `required_checks`<br>確認観点/結合・運用 | 統合・導出 | 今回必要な検査を満たしたか | 実行済み少数検査だけで全検証完了とする | タスク/契約の必要検査から参照。実行済みからは導けない / 適用: 条件：検査適用性の判断 | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `failures`<br>保存/導出 | 統合・導出 | どの形式条件が失敗したか | 修復対象を特定できない | チェッカーの出力へ参照。正式レビューに全ログを複写しない / 適用: 条件：形式的失敗がある | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `warnings`<br>保存/導出 | 統合・導出 | 阻害ではないが何が未確認・要注意か | 検査の限界を合格から読めなくなる | チェッカー出力へ参照。failureとの分類を維持 / 適用: 条件：警告がある | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `coverage`<br>結合・運用 | 条件付き | 実施範囲の集計をどこで確認できるか | ログへ参照がなければ検査の対象範囲が分からない | formal review.scopeと確認対象が同じなら正本参照。意味レビューと形式検査は範囲を混ぜない / 適用: 条件：形式検査の範囲記録 | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## 項目レビュー

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `semantic_status`<br>保存/確認観点 | 条件付き | 個別項目の意味に問題があるか | 全体合格だけでは項目の未解決を追えない | 同意味の個別finding.verdictと正式適用statusは目的が異なる。図系正本を参照 / 適用: 条件：項目ごとの状態で修復管理する場合 | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `fidelity_status`<br>保存/確認観点 | 条件付き | 個別図の出典忠実性が未完か | 全体比較の未完箇所を探しづらい | 図系の比較結果・正本状態へ参照。意味評価で代替しない / 適用: 条件：出典忠実性の項目管理 | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `visual_review_status`<br>保存/確認観点 | 条件付き | 個別表示を確認したか | 未観察の図を全体評価から合格にする | 図系正本を参照。レビュー実施・版との対応なしにpassedを複写しない / 適用: 条件：個別表示・比較レビュー | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## deterministic検査記録.coverage

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `population`<br>保存/結合・運用 | 統合・導出 | 全確認対象の集合は何か | coverageの対象外が不明 | 現plot/manifestの当該版へ参照で集合を特定 / 適用: 条件：標本・全件の対象集合 | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `target`<br>保存/確認観点 | 条件付き | どの対象を検査予定としたか | 実施範囲の不足を見つけられない | 全件ではpopulationと同じ、標本では事前計画 / 適用: 条件：予定と実施を区別 | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `checked`<br>保存/結合・運用 | 統合・導出 | 実際に何を検査したか | 予定しただけの項目を確認済みにする | 実行ログ/レビューscopeから導出可 / 適用: 条件：実施の範囲 | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `denominator`<br>導出 | 統合・導出 | coverageの基準母数は何件か | 件数だけから母集団が異なる検査を比較する | population/target集合の件数を明示した定義で導出。score分母/数量分母と別 / 適用: 条件：網羅率・件数の要約を行う | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `seed`<br>結合・運用 | 条件付き | 無作為標本を同じ条件で再現できるか | 無作為抽出を再現しづらい | 全件・判断抽出では不要。採択集合も保持すれば旧標本そのものは再現可 / 適用: 条件：無作為標本を用いる | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |
| `exclusions`<br>保存/確認観点 | 条件付き | 何を何故確認対象外にしたか | 危険な項目を都合よく対象外へ移す | 空配列を強制する必要なし。範囲方針・除外理由へ一箇所で記述 / 適用: 条件：除外が意味・母集団を変える | 検査なし | [references/review-rubric.md](../references/workflow/review-rubric.md) |

## 調査抽出の既存補助属性

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `publication_status`<br>保存/確認観点 | 条件付き | 査読前・正式出版等のどの報告状態か | 版を同じ質・確実性で扱う | source.versionから常に導出できない。源の種別・書誌説明に統合可 / 適用: 条件：公表状態が採否・評価を変える | 専用の当該属性検査なし | [references/survey-methods.md](../references/research/survey-methods.md) |
| `design`<br>保存/確認観点 | 統合・導出 | どの研究設計が結果を支えるか | 設計別の推論限界を誤る | work.design_or_typeの同義別名として一箇所管理 / 適用: 条件：設計差が判断に寄与 | 専用の当該属性検査なし | [references/survey-methods.md](../references/research/survey-methods.md) |
| `context`<br>保存/確認観点 | 条件付き | どの場面で測定・議論されたか | 異なる課題・文化・利用状況を同等扱いする | work/sample/methods・evidence.conditionの説明へ統合できる / 適用: 条件：文脈が主張の転用を変える | 専用の当該属性検査なし | [references/survey-methods.md](../references/research/survey-methods.md) |
| `system_or_population`<br>保存 | 統合・導出 | どのシステム・集団を対象にしたか | 異なる対象の結果を同じ効果と扱う | work.sample_or_corpus/identityやevidence.constructから継承可能 / 適用: 条件：対象差が意味を変える | 専用の当該属性検査なし | [references/survey-methods.md](../references/research/survey-methods.md) |
| `construct_definition`<br>保存 | 統合・導出 | その研究の構成概念は何を意味するか | 同名概念の異なる定義を併合する | evidence.constructの説明に統合可能。独立の定義レコードを全研究へ作らない / 適用: 条件：概念同名異義・境界比較 | 専用の当該属性検査なし | [references/survey-methods.md](../references/research/survey-methods.md) |
| `manipulation_or_measure`<br>保存 | 統合・導出 | どの操作・測定で概念を観測可能にしたか | 心的言語と哲学的スタンスを混同する | work.methods/evidence.method_or_basisの具体的内容として継承・差分保持 / 適用: 条件：操作化が解釈を変える | 専用の当該属性検査なし | [references/survey-methods.md](../references/research/survey-methods.md) |
| `outcome`<br>保存/確認観点 | 条件付き | 何の結果変数を測定したか | 信頼・主体性・非難等を同じ結果として比較する | construct/measure/resultの関係内で明確なら別列不要。介入側constructと結果変数は区別 / 適用: 条件：複数概念の関係を比べる | 専用の当該属性検査なし | [references/survey-methods.md](../references/research/survey-methods.md) |
| `evidence_location`<br>結合・運用 | 削除候補 | どの箇所が抽出内容を支えるか | locatorが保持されていれば固有の喪失なし | evidence.locatorと同義。既存別名参照以外の独立管理は不要 / 適用: 任意：旧形式への対応 | 専用の当該属性検査なし | [references/survey-methods.md](../references/research/survey-methods.md) |
| `inclusion_status`<br>結合・運用/保存 | 条件付き | 候補を採用・除外・保留のどれにしたか | 未評価・アクセス不能を除外と誤認、検索件数を再現できない | 採用集合から採用は導けるが除外/保留の判断は導けない。候補の既存作業記録に保持 / 適用: 条件：再現可能なスクリーニング・保留が必要 | 専用の当該属性検査なし | [references/survey-methods.md](../references/research/survey-methods.md) |

## reference observations/profile

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `observations`<br>保存 | 維持 | 実物から何を確認したか | 設計上の推測を観測値と混ぜる | 参考物のsource記録に観察欄として統合可。独立ファイルは不要 / 適用: 条件：参考物から設計を学ぶ | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `profile`<br>保存/確認観点 | 維持 | 対象読者・媒体へ何を採用するか | 原物の観察を普遍ルールへ変える | observationsとは種類が異なるが同じMarkdown内の別節でよい / 適用: 条件：再利用する設計上の選択 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `参考物の版`<br>保存/結合・運用 | 統合・導出 | どの資料の版を分析したか | 後続改訂との表示差・計測差を取り違える | source.versionの参照で一箇所管理 / 適用: 条件：参考物分析の追跡 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `対象箇所`<br>結合・運用 | 維持 | どのpage/文字block/図形/移行を観察したか | どの観察を元に採用したか説明できない | evidence.locator相当の自由記述に統合可能。部分ごとに独立sourceを作らない / 適用: 条件：具体的観察・採用判断 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `資料種別`<br>確認観点/保存 | 統合・導出 | スライド・論文・走査PDF等のどれか | 観測可否や転用できる規則を間違える | source.source_typeと同値なら参照 / 適用: 条件：資料種別が抽出・転用を変える | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `想定読者`<br>保存/確認観点 | 条件付き | 原物は誰を読者として作られたか | 専門家向けの省略を初学者資料へ持ち込む | 対象調査のaudienceとは異なる値になり得る。原物から不明なら不明と記す / 適用: 条件：読者差が転用判断を変える | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `媒体`<br>保存/確認観点 | 条件付き | 投影・紙・画面等どの媒体で利用したか | サイズ・情報密度の違いを無視して採用する | 資料種別だけでは利用媒体を導けない。タスク設定と同値なら参照 / 適用: 条件：媒体差が表示判断を変える | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `ページ数`<br>導出/保存 | 統合・導出 | 参考物の量と分析範囲はどれほどか | 全ページ確認の範囲を見積れない | PDF/スライドから安定導出。全資料で固定属性を手入力しない / 適用: 条件：分析範囲の管理 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `寸法`<br>保存/導出 | 条件付き | どの画面/紙面の寸法か | 表示上の位置・密度・文字サイズの転用を間違える | 原ファイルのメタデータから取得・参照 / 適用: 条件：表示・配置の比較 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `縦横比`<br>導出 | 統合・導出 | 媒体の横長/縦長はどの程度か | 寸法があれば同じ情報は再現できる | 寸法の比から導出。独立に手入力しない / 適用: 任意：表示用の派生値 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `文字ブロック`<br>保存/結合・運用 | 条件付き | どの内容がどのまとまりで配置されているか | 文字量だけでは階層・視線を比較できない | 抽出結果の参照。各blockに独立モデルレコードを強制しない / 適用: 条件：配置の分析 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `明示文字サイズ`<br>保存/導出 | 条件付き | 実際の原物に何ptと指定されているか | 見かけの文字高を実指定サイズと誤認する | PPTX等から取得可能、走査PDFでは未取得・推定と区別 / 適用: 条件：信頼できる計測・転用検討 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `位置`<br>保存/導出 | 条件付き | 文字/図の配置関係はどこか | 余白・近接・ナビゲーションの観察を説明できない | bbox・レンダーから取得、概略説明で足りる場合は全座標記録不要 / 適用: 条件：配置が採用理由を支える | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `色（観察）`<br>保存 | 条件付き | 実際に何色をどこで使ったか | 強調役割を根拠なしに一般化する | 色の役割という解釈とは別。原物の設定・実表示から確認 / 適用: 条件：色が設計判断を変える | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `画像数`<br>導出 | 条件付き | 画像がどの程度使われているか | 数の集計をしている場合だけ要約が失われる | 原ファイルから取得可。図の意味・有用性は数から導けない / 適用: 任意：分布計測が設計比較に寄与する場合 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `図形数`<br>導出 | 条件付き | 図形がどの程度使われているか | 数の集計をしている場合だけ要約が失われる | 抽出から取得可。カード大量でも根拠豊富とは言えない / 適用: 任意：分布計測が設計比較に寄与する場合 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `フッター/ページ番号`<br>保存/確認観点 | 条件付き | 現在位置・出典をどこに示したか | 位置づけ・出所対応の採用理由が不明 | 同じpage footer内でも出典とページ番号の役割は別として説明 / 適用: 条件：ナビゲーション・出典配置の分析 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `出典フッター頻度`<br>導出 | 統合・導出 | 重要pageに出典がどれだけ表示されるか | 計測比較時の網羅性が不明になる | footer観察とpage集合から導出。全文の引用件数では代替できない / 適用: 任意：出典配置の比較 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `節への再入場`<br>保存/確認観点 | 条件付き | どの節で目次へ戻り移行理由を示すか | ナビゲーションがあるだけで有用と認定する | プロットのtransition/Nextに観察と解釈を分けて統合可 / 適用: 条件：構成比較 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `文字類似性`<br>導出/確認観点 | 条件付き | 連続pageで本文がどれほど反復するか | 定型反復の計測比較ができない | 抽出テキストから計算可、重複の意味/良し悪しは導けない / 適用: 任意：局所反復の分析が必要 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `余白（観察）`<br>保存/導出 | 条件付き | 何の周りにどれだけ空間があるか | 図を読む空間と根拠不足の空白を同一視する | 位置/bbox/dimensionsから概算可、説明の機能は別の解釈 / 適用: 条件：余白が採用の判断に寄与 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `構成の流れ`<br>保存/確認観点 | 統合・導出 | 問い・回答をどの順で繋いだか | 配置から論証の蓄積を説明できない | reference_scopeのプロットへ統合可。別の構成台帳不要 / 適用: 条件：物語の採用判断 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `進行速度`<br>確認観点/保存 | 条件付き | 局所説明に何ページ/時間を使ったか | 密度・読者負担の違いを把握しづらい | page配分は数えられるが実際の発表時間は資料だけから導けない / 適用: 条件：ペースの採用検討 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `局所反復`<br>確認観点/保存 | 条件付き | 同じ枠を保ち何の情報関係を変えたか | 比較を助ける反復と単調な反復を区別しない | 文字類似性だけでは判断不可。プロットの差分と役割で説明 / 適用: 条件：反復の採否 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `節の位置づけ`<br>確認観点/保存 | 統合・導出 | 節が全体のどこにあり何を累積するか | 章立ての見かけだけをコピーする | reference plotのsection_question/answerへ統合 / 適用: 条件：構成の採用 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `主張と図の関係`<br>確認観点/保存 | 統合・導出 | 図はどの関係を観察可能にするか | 装飾を根拠図として転用する | reference plot.Figureへ統合。領域claimのevidenceへ自動変換しない / 適用: 条件：意味を担う図の採用 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `引用位置`<br>保存/確認観点 | 条件付き | 読者が主張と出所を対応できるか | 参考文献一覧が長いだけで出典が追えると誤認する | footer/caption/notesなどの観察を束ねる。独立座標記録不要 / 適用: 条件：引用の表現を転用 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `図の表現規則`<br>確認観点/保存 | 条件付き | 複数図で何の符号とラベルを共有するか | 単一図の色や形を普遍規則として拡張する | 原物の観察を参照しprofileの規則へ条件付き採用 / 適用: 条件：視覚語彙の採用 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `配置が反復する理由（解釈）`<br>確認観点/保存 | 統合・導出 | 反復は比較・理解をどう助けるか | 座標の反復を意味ある理由と混同する | 局所反復観察と同じ記録に解釈を分けて記述 / 適用: 条件：反復を採用する判断 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `強調色の意味（解釈）`<br>確認観点/保存 | 統合・導出 | 色は注目・警告・分類等の何を伝えるか | 色を同じ意味に見せたまま役割を変える | 観察された色と役割の解釈は別。profileの規則へ一箇所で保存 / 適用: 条件：色の意味を転用する | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `根拠と装飾の区別（解釈）`<br>確認観点 | 統合・導出 | 原物の要素は何の観察を支えるか | 装飾を根拠表示として採用する | Figure/job説明と統合可。画像数だけでは判定不能 / 適用: 条件：要素の採否 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `節間の接続（解釈）`<br>確認観点/保存 | 統合・導出 | なぜその順が読者の問いに答えるか | 見かけの順番だけを固定する | reference plot.Next/transitionへ統合 / 適用: 条件：構成の転用 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |

## reference profile記録区分

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `観察した計測値`<br>保存/確認観点 | 統合・導出 | 実物で確認した値は何か | 推定を実測と呼ぶ | 上のobservationsへの参照・一箇所管理 / 適用: 条件：観察がある | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `解釈した設計上の選択`<br>保存/確認観点 | 維持 | 観測内容をどの意味で説明したか | 採用判断を源の事実として見せる | 観察と解釈を同じ文書内でラベル分離 / 適用: 条件：設計の解釈を行う | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `転用する規則と適用条件`<br>保存/確認観点 | 維持 | 対象作業へ何をどの条件で採用するか | 原物の値を普遍規則にする | 規則と条件は一組で保持。タスク設定へ参照 / 適用: 条件：採用する設計規則 | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `参考物固有の既定値`<br>保存/確認観点 | 条件付き | 参考物の既定値を対象で使うか | プロファイル値を共通公開閾値にする | 観察値と同じ場合は参照。対象task採用値とは区別 / 適用: 条件：具体的値を持つプロファイル | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `転用しない内容・権利保護された内容`<br>保存/確認観点 | 条件付き | 何をどの理由で採用対象外にするか | 適用範囲と権利・文脈の問題を失う | 除外内容と採用範囲へまとめ、全ての候補に空欄を作らない / 適用: 条件：除外・制限が実際にある | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |
| `未決の問い`<br>保存/確認観点 | 統合・導出 | どの採用条件をまだ確認していないか | 未確認を採用可として固定する | task/plotのunresolved_questionへ統合可 / 適用: 条件：不明点が判断を変える | 専用の当該属性検査なし | [references/reference-analysis.md](../references/presentation/reference-analysis.md) |

## MIRU採用観点（schemaではない）

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `構成・現在位置・締めくくり`<br>確認観点 | 条件付き | 対象読者の問いを累積できるか | 原物の順だけをコピーする | plotで必要な問い/回答を記述しprofileは任意の採用参考 / 適用: 条件：当該参考スタイルを意図的に使う | 専用の当該属性検査なし | [references/miru-style-profile.md](../references/presentation/miru-style-profile.md) |
| `局所反復の枠と進行差分`<br>確認観点 | 条件付き | 何を保ち何を変えて比較可能にするか | 反復回避だけで無意味な配置変更をする | plotの行差分・narrative_job/Figureへ統合可 / 適用: 条件：局所的な比較を提示 | 専用の当該属性検査なし | [references/miru-style-profile.md](../references/presentation/miru-style-profile.md) |
| `画面・文字・余白・見出し・ページ番号`<br>確認観点 | 条件付き | 媒体と読者に適した表示か | 参照の見た目を普遍的release値にする | 参考物の観察/対象taskのトークンへ参照。ここから固定必須欄を作らない / 適用: 条件：媒体に合うスタイルを採用 | 専用の当該属性検査なし | [references/miru-style-profile.md](../references/presentation/miru-style-profile.md) |
| `赤い強調の役割`<br>確認観点 | 条件付き | 色がどの注目・警告を担うか | カテゴリ・状態・装飾へ意味なく流用する | 色トークンとprofile採用理由を一箇所管理 / 適用: 条件：赤い強調を採用 | 専用の当該属性検査なし | [references/miru-style-profile.md](../references/presentation/miru-style-profile.md) |
| `主張・図表・出典の近接`<br>確認観点 | 条件付き | 読者が観察と出所を対応できるか | 離れた参考文献一覧で出所表示を代替する | 主張/Figureの関係とcitation配置へ統合 / 適用: 条件：根拠ページの配置 | 専用の当該属性検査なし | [references/miru-style-profile.md](../references/presentation/miru-style-profile.md) |
| `原図の色の保持`<br>確認観点 | 条件付き | 色が出典の意味を担うか | 出典由来の分類や条件を色変更で歪める | 忠実性の正本を参照しprofileの別検査台帳を作らない / 適用: 条件：原図の色が意味を担う | 専用の当該属性検査なし | [references/miru-style-profile.md](../references/presentation/miru-style-profile.md) |
| `本文の短縮・分割`<br>確認観点 | 条件付き | 小文字化前に構成を変えるか | 可読性を損なう縮小を既定にする | 制作/視覚確認の判断に統合 / 適用: 条件：可読性が不足 | 専用の当該属性検査なし | [references/miru-style-profile.md](../references/presentation/miru-style-profile.md) |
| `転用範囲と除外`<br>確認観点 | 条件付き | どの構成選択を対象分野へ持ち込むか | 原物の領域論証を対象の根拠とする | profile採用条件とtask設定へ参照 / 適用: 条件：スタイル転用 | 専用の当該属性検査なし | [references/miru-style-profile.md](../references/presentation/miru-style-profile.md) |

## HCI根拠の確認観点

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `説明の基盤`<br>確認観点/保存 | 条件付き | 行動を何の観点で説明しているか | physical/design/intentionalと帰属先が混ざる | evidence.constructと操作化の説明で保持可。概念区別は残す / 適用: 条件：説明スタンスを調べる | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `帰属先`<br>確認観点/保存 | 条件付き | 誰/何へ原因・責任を帰属させたか | 同説明の異なる帰属先の効果を併合する | 説明の基盤とは別軸。結果変数の対象記述へ組込可能 / 適用: 条件：帰属を比較 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `研究ごとのプロンプト・操作・符号化規則`<br>確認観点/保存 | 条件付き | 提示語彙や測定定義は何か | 研究操作と哲学的スタンスを同一視する | work.methods/evidence.method_or_basisを参照し別hci台帳を不要にする / 適用: 条件：概念対応/フレーミング効果を解釈 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |

## HCIの結果変数の意味（schemaではない）

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `信頼`<br>確認観点 | 条件付き | システムへの信頼を測ったか | 行動依存・正確性と混同する | 実際に測定したoutcome/construct/measureへ格納し、未測定変数を全行へ追加しない / 適用: 条件：この結果変数を測定・論証した研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `適切に調整された依存`<br>確認観点 | 条件付き | 能力・リスクに応じた利用行動を測ったか | 信頼態度と同一視する | 実際に測定したoutcome/construct/measureへ格納し、未測定変数を全行へ追加しない / 適用: 条件：この結果変数を測定・論証した研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `理解`<br>確認観点 | 条件付き | 説明対象の理解を測ったか | 予測の正答だけで理解を認定する | 実際に測定したoutcome/construct/measureへ格納し、未測定変数を全行へ追加しない / 適用: 条件：この結果変数を測定・論証した研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `予測`<br>確認観点 | 条件付き | 対象の次行動を予測できたか | 理解・心の帰属へ短絡する | 実際に測定したoutcome/construct/measureへ格納し、未測定変数を全行へ追加しない / 適用: 条件：この結果変数を測定・論証した研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `主体性`<br>確認観点 | 条件付き | どの主体性の知覚/判断を測ったか | 実際の自律性・責任に読み替える | 実際に測定したoutcome/construct/measureへ格納し、未測定変数を全行へ追加しない / 適用: 条件：この結果変数を測定・論証した研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `統制`<br>確認観点 | 条件付き | 誰の統制・制御可能性を測ったか | 原因帰属・責任の成立を自動推論する | 実際に測定したoutcome/construct/measureへ格納し、未測定変数を全行へ追加しない / 適用: 条件：この結果変数を測定・論証した研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `因果的責任`<br>確認観点 | 条件付き | 原因寄与をどこへ帰属したか | 規範的責任へ飛躍する | 実際に測定したoutcome/construct/measureへ格納し、未測定変数を全行へ追加しない / 適用: 条件：この結果変数を測定・論証した研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `非難`<br>確認観点 | 条件付き | 誰に非難を向ける判断か | 因果寄与や修復義務と同じ指標にする | 実際に測定したoutcome/construct/measureへ格納し、未測定変数を全行へ追加しない / 適用: 条件：この結果変数を測定・論証した研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `功績`<br>確認観点 | 条件付き | 誰に成果の帰属/賞賛を向けたか | 非難と対称な同一尺度と決める | 実際に測定したoutcome/construct/measureへ格納し、未測定変数を全行へ追加しない / 適用: 条件：この結果変数を測定・論証した研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `説明義務`<br>確認観点 | 条件付き | 誰に説明を求めるか | 原因寄与・非難との区別を失う | 実際に測定したoutcome/construct/measureへ格納し、未測定変数を全行へ追加しない / 適用: 条件：この結果変数を測定・論証した研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `修復義務`<br>確認観点 | 条件付き | 誰に修復を求めるか | 道徳的地位・非難との区別を失う | 実際に測定したoutcome/construct/measureへ格納し、未測定変数を全行へ追加しない / 適用: 条件：この結果変数を測定・論証した研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |

## HCIの心的概念の意味（schemaではない）

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `知能`<br>確認観点 | 条件付き | 知的能力の知覚を測ったか | 感情・経験と一つのmind scoreにする | 測定・論証した概念だけをconstruct/outcomeに記述。全ての独立欄は不要 / 適用: 条件：この概念を対象とする研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `経験`<br>確認観点 | 条件付き | 経験能力の知覚を測ったか | 知能・意識と同一視する | 測定・論証した概念だけをconstruct/outcomeに記述。全ての独立欄は不要 / 適用: 条件：この概念を対象とする研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `感情`<br>確認観点 | 条件付き | 情動の知覚を測ったか | 心全体や感覚能力と同一視する | 測定・論証した概念だけをconstruct/outcomeに記述。全ての独立欄は不要 / 適用: 条件：この概念を対象とする研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `意識`<br>確認観点 | 条件付き | 意識の知覚/判断を測ったか | 心的言語の効果から存在を認定する | 測定・論証した概念だけをconstruct/outcomeに記述。全ての独立欄は不要 / 適用: 条件：この概念を対象とする研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `自律性`<br>確認観点 | 条件付き | どの自主性の判断を測ったか | 主体性の言語効果から自律性を証明する | 測定・論証した概念だけをconstruct/outcomeに記述。全ての独立欄は不要 / 適用: 条件：この概念を対象とする研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `感覚能力`<br>確認観点 | 条件付き | 感覚・苦痛等の能力判断を測ったか | 知能・経験と同じ尺度にする | 測定・論証した概念だけをconstruct/outcomeに記述。全ての独立欄は不要 / 適用: 条件：この概念を対象とする研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `道徳的地位`<br>確認観点 | 条件付き | どの道徳的扱いの判断を測ったか | 主体性・因果帰属から規範的地位を推論する | 測定・論証した概念だけをconstruct/outcomeに記述。全ての独立欄は不要 / 適用: 条件：この概念を対象とする研究 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |

## HCI帰属の条件・境界（schemaではない）

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `文脈`<br>確認観点/保存 | 統合・導出 | どの使用・社会的文脈か | 違う文脈の帰属を普遍化 | survey.context/work/evidenceの共有文脈へ参照 / 適用: 条件：観察・論証の意味を変える場合 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `役割`<br>確認観点/保存 | 統合・導出 | 参加者・利用者・開発者等のどの役割か | 同じ対象でも立場の違う責任判断を併合 | sample/contextの説明へ統合 / 適用: 条件：観察・論証の意味を変える場合 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `予見可能性`<br>確認観点/保存 | 統合・導出 | 結果を予見できたか | 責任判断の条件を落とす | 操作・条件の定義へ統合 / 適用: 条件：観察・論証の意味を変える場合 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `統制可能性`<br>確認観点/保存 | 統合・導出 | 誰が結果を統制できたか | 因果・道徳的責任の帰属条件を落とす | 測定outcomeと条件操作の両方で意味を分け保持 / 適用: 条件：観察・論証の意味を変える場合 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `情報`<br>確認観点/保存 | 統合・導出 | 参加者に何の情報が与えられたか | 語彙効果と知識差を取り違える | prompt/methodsへ統合 / 適用: 条件：観察・論証の意味を変える場合 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `結果の肯定的・否定的な性質`<br>確認観点/保存 | 統合・導出 | どの成否・利得・損失の文脈か | 非難と功績を単純な対称効果にする | condition/outcomeの文脈へ統合 / 適用: 条件：観察・論証の意味を変える場合 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `文化`<br>確認観点/保存 | 統合・導出 | どの文化的背景・集団か | 特定集団の帰属を一般化 | sample/contextへ参照 / 適用: 条件：観察・論証の意味を変える場合 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `専門性`<br>確認観点/保存 | 統合・導出 | どの専門経験・知識があるか | 専門家/初心者の効果差を落とす | sample_or_corpusやcontextへ参照 / 適用: 条件：観察・論証の意味を変える場合 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `反復的な相互作用`<br>確認観点/保存 | 統合・導出 | 初回か継続利用か、どの期間か | 初回フレーミングの効果を長期利用へ一般化 | methods/time conditionへ統合 / 適用: 条件：観察・論証の意味を変える場合 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `根拠が扱う判断の種類`<br>確認観点/保存 | 統合・導出 | 説明基盤/帰属/心的知覚/因果/規範/行動のどれか | 責任の因果・規範・行動を混同 | construct/outcome/claim_type/claim_roleの説明へ統合 / 適用: 条件：観察・論証の意味を変える場合 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `三スタンス分類から漏れる内容`<br>確認観点/保存 | 統合・導出 | 社会技術・組織・混合等をどう扱うか | 分類で捨てた内容を存在しないとする | construct_definition・limitationへ統合 / 適用: 条件：観察・論証の意味を変える場合 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |
| `符号化担当者・参加者への語彙提示`<br>確認観点/保存 | 統合・導出 | 分類語彙を誰にどう与えたか | 誘導された判断を自然な分類として扱う | methods/promptへ統合 / 適用: 条件：観察・論証の意味を変える場合 | 専用の当該属性検査なし | [references/hci-stance-attribution.md](../references/research/hci-stance-attribution.md) |

## managementの作業依頼・運用観点

| 項目・役割 | 判断 | 答える問い | 除いた場合の影響 | 重複・導出・適用条件 | 現チェッカー | 根拠の所在 |
| --- | --- | --- | --- | --- | --- | --- |
| `成果物ごとの責任者`<br>結合・運用 | 維持 | 誰が最終責任を担うか | 共有作業で整合・終了判断が抜ける | タスクの既存ownerへ一箇所。WBS/RACIの別台帳は任意 / 適用: 条件：複数担当の協働 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `WBS`<br>結合・運用 | 条件付き | 複雑な作業分解を誰がどの範囲で担うか | 単純案件では失う意味なし | 既存作業依頼と工程で明らかなら不要 / 適用: 任意：複雑な案件 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `RACI`<br>結合・運用 | 条件付き | 責任・承認・相談・連絡を区別する必要があるか | 役割境界が単純なら失う意味なし | 責任者・協働契約の説明と同じなら重複 / 適用: 任意：複雑な責任境界 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `担当者ID`<br>結合・運用 | 条件付き | どの実装/レビュー結果を誰が返したか | 複数担当の問題を差戻しにくい | tool履歴・依頼ownerへ参照。領域根拠ではない / 適用: 条件：複数担当・差戻し追跡 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `ハッシュ`<br>導出/結合・運用 | 統合・導出 | 同じ成果物版か | 別の生成状態の検証結果を混ぜる | 既存artifact/監査のhashを参照・計算。作業者ごと複写不要 / 適用: 条件：成果物同一性・正式検証 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `レビュー状態`<br>保存/結合・運用 | 統合・導出 | どの作業が確認済み/未完か | 未確認の結果を統合する | formal review/plot statusへ参照、異なる工程状態を同値としない / 適用: 条件：受け渡し判断 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `制作記録`<br>保存/結合・運用 | 統合・導出 | どの入力でどの版を作ったか | 再現・差戻しの範囲が不明 | production/buildの正本へ参照。独立worker台帳を増やさない / 適用: 条件：成果物を制作する案件 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `作業`<br>保存/確認観点 | 維持 | 担当者が答える bounded question/成果物は何か | 担当が論旨・範囲を勝手に広げる | scopeと一つの依頼文に統合可 / 適用: 条件：委任する場合 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `入力ファイル・URL`<br>結合・運用 | 維持 | 正確に何を読む/書くか | 別版・別sourceを解釈する | source/asset/plotへの既存参照を使う / 適用: 条件：委任の入力同一性 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `検索式`<br>保存 | 統合・導出 | どの検索を行うか | 結果の再現性と領域境界を失う | protocol検索式の参照でよい / 適用: 条件：検索を委任 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `日付範囲`<br>保存/確認観点 | 統合・導出 | どの期間を対象にするか | 最新候補や古い資料の混入でcoverageを変える | task/protocolの参照でよい / 適用: 条件：期間制約をもつ委任 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `スキーマ`<br>結合・運用 | 統合・導出 | どの定義・形式で返すか | 用語やキーを担当ごとに増やす | 既存evidence/plot定義版を参照し再コピーしない / 適用: 条件：構造化出力を委任 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `担当plot_row_ids`<br>結合・運用 | 条件付き | どの行だけ変更できるか | 他担当の行を上書きする | plot_row_idの存在とassigned ownerは別意味。一依頼の範囲に記述 / 適用: 条件：プロット編集を委任 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `担当evidence_block_ids`<br>結合・運用 | 条件付き | どの共有根拠ブロックを扱うか | 担当が共有条件・主張を勝手に変える | ブロックID参照と所有範囲を同じ依頼で示す / 適用: 条件：ブロック単位の委任 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `解消するRRM上の不足`<br>確認観点 | 条件付き | どの意味関係が次の判断を変えるか | 目的のない抽出で六欄を埋める | 作業の問いから明らかなら独立欄不要 / 適用: 条件：不足の明示が結果を変える | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `情報源の品質`<br>確認観点 | 統合・導出 | 採用できるsourceの条件は何か | レビュー基準と違う資料が返る | protocol品質条件の参照 / 適用: 条件：source採用を委任 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `除外条件`<br>確認観点 | 統合・導出 | どの候補を対象外にするか | 担当ごとにcoverageを変える | protocolの採否条件へ参照 / 適用: 条件：検索/採否を委任 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `単位`<br>確認観点 | 統合・導出 | どの対象を一件・比較単位とするか | 報告と研究の件数が混ざる | evidence-modelの単位を参照 / 適用: 条件：抽出・集計を委任 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `出力`<br>結合・運用/保存 | 維持 | どの出典付き結果を返すか | 統合で出典・不確実性が不足する | source/work/evidenceの正本への変更。別のworker evidence台帳は不要 / 適用: 条件：委任する場合 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `終了条件`<br>確認観点/結合・運用 | 維持 | 何を満たせば bounded task完了か | 不足が残ったまま返す・無制限に調査する | タスクのacceptance/checkを参照・一箇所管理 / 適用: 条件：委任する場合 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `管理者へ返す事項`<br>確認観点/保存 | 条件付き | 曖昧さ・アクセス不能・矛盾・範囲問題をどう扱うか | workerが勝手に解決して意味を変える | 未解決証拠はevidence/claimへ置き、依頼側には参照を返す / 適用: 条件：委任で問題が発生 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |
| `go/revise/narrow/stop`<br>保存/結合・運用 | 統合・導出 | 受け渡し後にどう進めるか | formal passと混同・差戻し先が不明 | G4-Pならg4p_verdictと同判断を二重管理せず変更記録へ参照 / 適用: 条件：明示的受け渡し判断 | 専用の当該属性検査なし | [references/management-workflow.md](../references/workflow/management-workflow.md) |

