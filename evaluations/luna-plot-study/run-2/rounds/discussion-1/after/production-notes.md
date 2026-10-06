# 制作メモ・改稿履歴

## 改稿で変えた論証

| 変更前 | 変更後 | 理由・原典で確認したこと |
|---|---|---|
| 全体質問・複数箇所比較ならLCを先に試す、と一般条件のように提示 | LCを「有力な比較対象」とし、勝者を先取りしない。LongBench v2とLaRAの研究内比較で支持と限界を同じ節に配置 | LongBench v2 §4.2/Fig.4では、512-token chunkのtop-Nを元文書順に連結したRAGがQwen2.5で32K時に全文128Kを+4.1ポイント上回る一方、GPT-4oでは128K RAGが最良でも全文入力に−0.6ポイント。LaRA Table 2ではComparisonのLC−RAG平均差が32K +15.22、128K +14.30ポイントだが、Overallは32K +2.40から128K −3.68へ変わる。図表・本文のモデル群傾向と課題別傾向を分けた。 |
| LongBench v2をタスク背景だけに使用 | §4.2/Fig.4を中心根拠に採用 | Fig.4はRAG retrieval baselineと同一モデルの全文128K入力を直接比べる。RAG構成全般の評価ではないため、比較条件も明記した。 |
| Self-Route Fig.3を二段階方式のフロー図として扱い、同程度と要約 | §4.2の本文で方式を説明し、Fig.3(a)(b)はtop-k性能／token比曲線として使用。Table 1の同一行・同一Avg列で性能差とtoken比を対応 | Table 1 (Contriever) のLC→Self-Route Avgとtoken比はGemini 49.70→46.41 (−3.29ポイント), 38.39%; GPT-4O 48.67→48.89 (+0.22), 61.40%; GPT-3.5-Turbo 32.07→35.32 (+3.25), 38.85%。「comparable」は著者評価、これらは表の観察、許容損失は利用側が決める品質要件として分離した。 |
| Self-Route失敗分析の節参照が§5.4 | §5.2・Fig.4 (PDF p.6 / 印刷頁886) に訂正 | §5.2がunanswerable例の分類と失敗分布。§5.4はsynthetic data analysisだった。棒は件数でデータセットごとに総数が異なるため失敗率と誤読しない注記を追加。 |
| Jin et al.の取得数・hard negatives・三方策とOP-RAGを一枚の候補群として記載 | Jin et al. §3.3/Fig.3(b–d)でgold passageを固定してhard negativesを増やす診断に限定。三方策は本編図に含めず、OP-RAGを独立した同条件結果ページへ分離 | Figure 3のNQ実験はGemma2-9B-Chat、Mistral-Nemo-12B-Instruct、Gemini-1.5-Proを使い、retriever由来別のhard negativesが増すと正答率が低下。これは全文LCとの直接比較ではなくRAG生成段の失敗機序。OP-RAG Table 1は別研究・別データなので混ぜず、同じLlama3.1-70BのEn.QA結果を単独で示す。 |
| OP-RAGの値を本文由来の候補として留保 | Table 1のEn.QA列・F1/Tokensに限定して採用 | Llama3.1-70B全文入力117K tokensはF1 34.26、OP-RAGは16K/24K/48Kで44.43/45.45/47.25。351問のEn.QA内の結果として限定した。 |

## Self-Routeで解消できていない記載差

本文の評価説明とTable 1のAvg表示は、性能値・answerable率に差がある。本文はGeminiの性能低下を2.2%、GPT-4Oを47.04→46.83と記載するが、Table 1のAvgはGemini −3.29ポイント、GPT-4O +0.22ポイント。Geminiのanswerable率は本文に81.74%、Table 1に76.78%。本文のtoken比38.6%とTable 1の38.39%のような丸め差もある。またFig. 3／Appendix Table 7のk-ablationはLC upper bound 45.53を掲げ、Table 1 Avgとは異なる集計である。分母や集計法から対応関係を確認できなかったため、どれかを誤植と推測しない。プロットではFig. 3のk曲線とTable 1のモデル別費用・品質行を別表示し、同一行のTable 1値だけを性能差とtoken比の対として使う。本文・表・k-ablationの不一致を開示し、運用上の許容損失をこの論文の「comparable」だけから設定しない。

## 原典確認・検証

- 目視確認した原PDFページ：LongBench v2 p.8 (Fig.4)、LaRA p.6 (Table 2)・p.16 (Fig.6)、Self-Route pp.4–6 (Table 1/Fig.3/Fig.4)、Long-Context LLMs Meet RAG p.6 (Fig.3)、OP-RAG pp.3–4 (Fig.3/Table 1)。図の軸、凡例、本文説明、図番号・ページをプロット記述と照合した。
- LaRA Fig.6はLocation / Reasoningのみ（位置を32Kで5/3分割、128Kで10/6分割）で、Comparison優位の根拠ではない。ComparisonはTable 2のComparison列とAvg GAP行を参照する。
- 対象は`corpus/bibliography.json`の10報。ほかのrun、supervisor record、評価記録は参照していない。
- 変更後の`plot.md`は15枚。各スライドにT/B/Bottom/Figure/Next/出典を置き、出典図表の役割と条件を記した。

## 未解決事項と制作上の境界

- Self-Route本文／Table 1間の性能差・answerable%差は未解決。改訂後も本文値と表値を統合しない。
- Self-Routeのtoken比、OP-RAGのtokensはモデル入力tokenの指標で、retriever費用、インデックス構築、レイテンシ、総API/GPU費用を含む共通のend-to-end原価比較ではない。
- LaRAの結果は2326問・4 task type・GPT-4o評価・記載モデル・32K/128K条件に限られる。モデル群差をモデルサイズの因果効果とみなさない。
- LongBench v2 Fig.4のretrieval baselineはベンチマーク論文内の一構成であり、長文文書QA一般の代表性は保証しない。
- Jin et al. hard-negative実験はNQの合成設定でgold passageを固定するため、現実の複数証拠・multi-hop検索へ直接一般化しない。
- 日本語・ドメイン固有資料での再検証、費用・遅延・引用支持率の同条件比較は未実施。
- 本改稿は原PDFの該当図表を目視照合したプロット改訂。素材の切り抜き、権利・利用経路の確定、スライド組版・レンダリングは実施していない。
