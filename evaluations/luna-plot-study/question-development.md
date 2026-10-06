# 学術的な問いと資料集合の準備記録

このファイルは監督用です。Luna に渡す資料集合は `corpus/` の書誌情報と原文 PDF・全文抽出 txt に限定します。本ファイルの候補分類、採用理由、比較上の注意は制作入力に含めません。

## 出発点と確定した問い

出発点は次の関心でした。

> 長い文書集合への質問応答で、長いコンテキストは検索拡張生成(RAG)を代替できるか。回答の正確さ、根拠利用、計算コストを分けて、どの条件で検索・長文入力・併用が有用か理解したい。

公開一次論文を新規に探索した結果を踏まえ、監督者は次の問いと関心を確定しました。

> 長い文書集合を根拠に答えるLLMでは、検索して一部を渡す方法と、文書を長いコンテキストに入れる方法は、どの条件で置き換えられ、どの条件で組み合わせる意味があるのか。

> 回答の正しさ、根拠の利用、必要な計算資源を踏まえ、採用する方式を判断できる研究サーベイにしたい。

枚数、順序、論証、結論、採用する図は指定しません。研究ごとの QA 形式、引用評価、コスト定義の違いを資料提供側が答えとして整理して渡さず、Luna が論文から検討する課題とします。

## 問いを調整した理由

- 「長いコンテキスト」は、モデルが対応する窓長と、実際にどの資料を入力するかの方針の両方を指し得ます。確定した問いでは入力方針を明示しました。長文対応モデルを RAG の生成器に使う研究もあり、方式は必ずしも排他的ではありません。
- 「代替できるか」という二択では、集合全体が入力上限に収まる条件と、集合から一部を選ぶ必要がある条件が混ざります。「どの条件で」により、資料量と入力可能量を含めて検討できます。
- 質問に正しく答えること、答えが資料に支えられていること、必要な根拠が十分に示されることは、論文ごとに異なる方法で評価されます。根拠利用を扱う資料を独立に含めました。
- 「計算コスト」には入力トークン数、生成トークン数、推論料金、推論時間、検索や索引作成の負担、学習費用が含まれ得ます。確定した関心は「必要な計算資源」とし、単一の共通スコアへの換算は要求しません。
- 論文間にはモデル世代、事前学習・追加学習、データ集合、タスク、検索器、文書分割、入力順序の違いがあります。今回の資料群だけで、同一条件での普遍的な方式ランキングや現在の製品料金を確定することは目的にしません。

## 探索範囲と資料の状態

- 評価の時間基準は **2026-10-06** です。将来の論文を既刊扱いせず、保存した各版の年または投稿日を確認しました。
- 資料は arXiv、ACL Anthology および候補確認用の著者・公式会議ページから探索しました。採用セットの原文 PDF はすべて arXiv または ACL Anthology から取得しました。
- 15 件の独立した候補を調べ、10 件を採用しました。採用論文は PDF 本文を取得し、タイトル・著者を照合し、問いに関わる設定・評価・限界の記述を本文から確認しました。除外候補は公式一次ページの書誌・要旨を確認した段階であり、全文の詳細な検討は行っていません。
- 以前の評価用資料、抽出図、サーベイの章立て、要約、既成の論証を再利用していません。
- 「最新」や「網羅」を主張する選定ではありません。約 10 本で問いに関わる異なる実験・評価上の問題へ接続できることを優先しました。

主な検索語は `Retrieval Augmented Generation or Long Context`, `Long-Context LLMs Meet RAG`, `LaRA`, `In Defense of RAG`, `Lost in the Middle`, `RULER`, `LongBench v2`, `LongCite`, `BERGEN`, `Can Long-Context Language Models Subsume Retrieval`, `Retrieval meets Long Context`, `Benchmarking Large Language Models in Retrieval-Augmented Generation`, `Enabling Large Language Models to Generate Text with Citations`, `LongBench`, `NoLiMa` です。

## 候補からの選定

以下の並びと理由は監督者が資料選定を追跡するための記録です。Luna 用書誌はタイトルのアルファベット順にしています。

| 候補・一次資料 | 判断 | 選定理由 |
| --- | --- | --- |
| Li et al., *Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach* (EMNLP Industry 2024), https://aclanthology.org/2024.emnlp-industry.66/ | 採用 | 直接比較と Self-Route による方式併用を扱い、回答性能と費用の関係に接続できます。 |
| Yu et al., *In Defense of RAG in the Era of Long-Context Language Models* (arXiv 2024), https://arxiv.org/abs/2409.01666 | 採用 | 検索した部分を元の文書順に提示する OP-RAG を扱います。単純な RAG 実装の評価を RAG 全体の限界と一般化しないための資料です。 |
| Kuan Li et al., *LaRA: Benchmarking Retrieval-Augmented Generation and Long-Context LLMs - No Silver Bullet for LC or RAG Routing* (arXiv 2025), https://arxiv.org/abs/2502.09977 | 採用 | 資料・タスク・モデル・長さを横断して方式の差を扱い、同じ方針が常に有利という解釈を検討できます。 |
| Jin et al., *Long-Context LLMs Meet RAG: Overcoming Challenges for Long Inputs in RAG* (arXiv 2024), https://arxiv.org/abs/2410.05983 | 採用 | 検索結果を長い入力へ拡張する場合の負例、並べ替え、追加学習を扱います。検索と長文入力の併用の条件へ接続できます。 |
| Liu et al., *Lost in the Middle: How Language Models Use Long Contexts* (TACL 2024), https://aclanthology.org/2024.tacl-1.9/ | 採用 | 文書集合 QA と関連情報の位置を扱い、入力上限と実際の情報利用を区別できます。 |
| Hsieh et al., *RULER: What's the Real Context Size of Your Long-Context Language Models?* (COLM 2024 / arXiv), https://arxiv.org/abs/2404.06654 | 採用 | 窓長の公称値と、複数の合成課題で測る利用能力を区別できます。現実の QA と同じ測定ではないことも検討対象です。 |
| Bai et al., *LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks* (ACL 2025), https://aclanthology.org/2025.acl-long.183/ | 採用 | 長文の実課題と推論を扱います。選択式評価などの設定が自由回答 QA と同じではないため、評価の違いを検討できます。 |
| Zhang et al., *LongCite: Enabling LLMs to Generate Fine-grained Citations in Long-Context QA* (Findings ACL 2025), https://aclanthology.org/2025.findings-acl.264/ | 採用 | 長文 QA で根拠の示し方と評価を直接扱います。引用特化学習の効果は入力方式だけの効果と区別する必要があります。 |
| Rau et al., *BERGEN: A Benchmarking Library for Retrieval-Augmented Generation* (Findings EMNLP 2024), https://aclanthology.org/2024.findings-emnlp.449/ | 採用 | 検索器、再順位付け、生成器、評価方法を扱い、RAG の条件を具体化できます。長文全体入力との直接比較ではありません。 |
| Lee et al., *Can Long-Context Language Models Subsume Retrieval, RAG, SQL, and More?* (arXiv 2024), https://arxiv.org/abs/2406.13121 | 採用 | 文書集合そのものを入力する Corpus-in-Context と LOFT を扱い、長文モデルによる検索・QA に接続できます。SQL や画像等の結果をテキスト QA にそのまま転用しない検討が必要です。 |
| Xu et al., *Retrieval meets Long Context Large Language Models* (arXiv 2023 / ICLR 2024), https://arxiv.org/abs/2310.03025 | 除外 | 検索と窓長拡張の併用を扱う有用な候補ですが、追加学習を含む窓長拡張の比較と、今回の入力方針の比較を読み分ける負担があります。約 10 本の枠では Jin の併用研究を採用しました。 |
| Chen et al., *Benchmarking Large Language Models in Retrieval-Augmented Generation* (arXiv 2023 / AAAI 2024), https://arxiv.org/abs/2309.01431 | 除外 | RGB による RAG の基礎能力評価です。検索結果の負例・情報統合は Jin、検索構成の比較は BERGEN を採用し、枠を確保しました。 |
| Gao et al., *Enabling Large Language Models to Generate Text with Citations* (EMNLP 2023), https://aclanthology.org/2023.emnlp-main.398/ | 除外 | ALCE は引用品質の重要な基礎ですが、長文 QA と直接つながる LongCite を優先しました。初期採用案からの差し替えは監督者が承認しています。 |
| Bai et al., *LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding* (ACL 2024), https://aclanthology.org/2024.acl-long.172/ | 除外 | LongBench v2 の前身です。別のデータ集合を持つ独立論文ですが、同一系統のベンチマークだけで枠を二つ使わず、異なる問題を扱う研究を優先しました。 |
| Modarressi et al., *NoLiMa: Long-Context Evaluation Beyond Literal Matching* (arXiv 2025), https://arxiv.org/abs/2502.05167 | 除外 | 字面一致を超える検索の評価が有用です。今回は情報位置に Lost in the Middle、合成課題の広がりに RULER、実課題に LongBench v2 を採用し、長文評価の枠を増やしすぎないようにしました。 |

## 独立性と選択の幅の確認

採用 10 件は異なる研究です。会議版と arXiv 版を別論文として数えていません。LongCite、LongBench v2、LaRA の arXiv 初版と公開版も追加カウントしていません。書誌年は保存した版の年に合わせ、LongCite は Findings ACL 2025、Lost in the Middle は TACL 2024 としています。

選択には、長文全体入力の有用性を示す直接比較、RAG の工夫による利点を扱う研究、条件依存性を扱う比較、関連情報の位置・長さ・検索負例による不利な条件、引用の評価を含めました。片方の方式が有利という主張だけに偏ることを避けるための選定であり、各論文から制作側が導く結論は指定していません。

初期連絡で Jin の論文を *An Evaluation and Decision Flow* と呼んだ箇所は誤記でした。正確な題名は *Overcoming Challenges for Long Inputs in RAG*、保存した版は `arXiv:2410.05983v1` (2024-10-08) です。保存資料を ICLR 2025 の公開版と断定しません。

## 保存版と時間基準の確認

| ID | 保存した版 | PDF ページ数 | 2026-10-06 以前である根拠 |
| --- | --- | ---: | --- |
| bergen | Findings EMNLP 2024, `2024.findings-emnlp.449` | 24 | 公式書誌の年が 2024 |
| loft | `arXiv:2406.13121v1` | 29 | PDF ヘッダーが 2024-06-19 |
| op-rag | `arXiv:2409.01666v1` | 5 | PDF ヘッダーが 2024-09-03 |
| lara | `arXiv:2502.09977v2` | 22 | PDF ヘッダーが 2025-03-05 |
| long-context-meets-rag | `arXiv:2410.05983v1` | 34 | PDF ヘッダーが 2024-10-08 |
| longbench-v2 | ACL 2025, `2025.acl-long.183` | 26 | 公式書誌の年が 2025 |
| longcite | Findings ACL 2025, `2025.findings-acl.264` | 25 | 公式書誌の年が 2025 |
| lost-in-the-middle | TACL 2024, `2024.tacl-1.9` | 17 | 公式書誌の年が 2024 |
| self-route | EMNLP Industry 2024, `2024.emnlp-industry.66` | 13 | 公式書誌の年が 2024 |
| ruler | `arXiv:2404.06654v3`, PDF に COLM 2024 の表記 | 27 | PDF ヘッダーが 2024-08-06 |

## 取得・検証記録

通常のネットワーク実行では公開ホストの名前解決に失敗したため、許可された資料収集の範囲で昇格した `curl` により PDF を順次取得しました。書誌の確認と技術調査には web ツールを使用しました。

`pdftotext -layout -enc UTF-8` で全 10 本の全文を機械抽出し、`pdfinfo` でページ数とファイルの読取り可能性を確認しました。PDF 先頭の `%PDF-`、各 txt の非空性、最初のページの題名・著者を確認しました。PDF 本体には加工を加えていません。レイアウト抽出には文字欠落や段組み順の乱れがあり得るため、原文 PDF を併置しています。

LongBench v2 の初期取得 URL は別論文を返しました。タイトルの照合で検出し、公式一次ページで確認した `2025.acl-long.183.pdf` へ修正し、txt も再抽出しました。最終セットの題名は LongBench v2 と一致しています。

`corpus/bibliography.json` には全著者、題名、年、版、一次資料 URL、PDF URL、相対ファイル名、ページ数、PDF と txt の SHA-256 を保存しています。`corpus/README.md` は同じ中立的な書誌情報の一覧です。資料の合計は 10 PDF と 10 txt、PDF は 21,011,329 bytes です。候補分類、採用意図、抽出要約、図の選択、論証案を corpus 内に保存していません。

## 次工程への引き渡し

Luna 起動担当へコピー可能な範囲は `corpus/` 全体です。`question-development.md` はコピーしません。問いと関心の文面は監督者が確定したものを用い、枚数や構成を追加指定しません。3 件の試行、各試行への壁打ち、全件終了後の一般的なスキル改善は、資料収集担当の書き込み範囲外です。
