# 使用図版と出典

作成日：2026-10-07（JST）

## 図版の方針

スライドの4カードには、指定された各一次論文の Figure 1 から小範囲を切り出して掲載した。本文中の比較図は論文の結果図を別の研究へ流用したものではなく、各論文の方法・出力を同じ読み順に置いた制作者による整理である。数量性能の再描画や、異なる課題間の順位比較は行っていない。

図の使用は、研究内容の説明と比較のための引用である。切り抜き、スライド上のサイズ変更を除き、色・形状・ラベルの意味を変える編集はしていない。図版の利用が著者・出版社の包括的な再利用許諾を意味するものではない。

## 使用した原図

| スライド | 原資料の図・所在 | ローカル図版 | 切り出し（原PDFページの110 dpi PNGに対するpx座標） | 残した関係／用途 |
|---|---|---|---|---|
| Shap·E | Jun & Nichol, Figure 1, PDF p.2 | [shap_e_fig1_crop.png](figures/shap_e_fig1_crop.png) | x=145, y=130, w=650, h=360 | テキスト条件で得た形状例8件を示す。図全体のうち上2行だけを抜粋。 |
| Structured 3D Latents | Xiang et al., Figure 1, PDF p.1 | [trellis_fig1_crop.png](figures/trellis_fig1_crop.png) | x=90, y=350, w=760, h=420 | 画像・テキスト条件、複数形式、編集例を示す原図の関係を保持。 |
| Hunyuan3D 2.0 | Hunyuan3D Team, Figure 1, PDF p.2 | [hunyuan_fig1_crop.png](figures/hunyuan_fig1_crop.png) | x=165, y=258, w=605, h=382 | Hunyuan3D-DiTの形状生成とHunyuan3D-Paintのテクスチャ生成の構成を示す。 |
| Seed3D 1.0 | ByteDance Seed, Figure 1, PDF p.1 | [seed3d_fig1_crop.png](figures/seed3d_fig1_crop.png) | x=107, y=765, w=723, h=265 | 生成資産をロボット操作シミュレーションの場面へ配置する例を示す。 |

レンダリング元ページと取得した論文PDFは `audit/figure_crops/page_*.png`、`audit/source_pdfs/*.pdf` に保存した。スライド内の個別図注にも著者・年・図番号・PDFページを記した。

## 参考文献・一次資料

1. Heewoo Jun and Alex Nichol. “Shap-E: Generating Conditional 3D Implicit Functions.” arXiv:2305.02463 (2023). [論文・PDF](https://arxiv.org/abs/2305.02463) · [PDF](https://arxiv.org/pdf/2305.02463)
2. Jianfeng Xiang et al. “Structured 3D Latents for Scalable and Versatile 3D Generation.” CVPR 2025, arXiv:2412.01506. [論文・PDF](https://arxiv.org/abs/2412.01506) · [PDF](https://arxiv.org/pdf/2412.01506)
3. Hunyuan3D Team. “Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation.” arXiv:2501.12202 (2025). [論文・PDF](https://arxiv.org/abs/2501.12202) · [PDF](https://arxiv.org/pdf/2501.12202)
4. ByteDance Seed. “Seed3D 1.0: From Images to High-Fidelity Simulation-Ready 3D Assets.” arXiv:2510.19944 (2025). [論文・PDF](https://arxiv.org/abs/2510.19944) · [PDF](https://arxiv.org/pdf/2510.19944)

## 根拠と編集上の解釈

| 研究 | スライドに置いた出典報告 | スライド上の読み取り |
|---|---|---|
| Shap·E | 暗黙関数のパラメータを条件付き拡散で生成し、テクスチャ付きMeshおよびNeRFとしてレンダリングできる（要旨・方法、Fig. 1）。 | 「一つの関数表現から複数の描画形式へ」。 |
| Structured 3D Latents | 疎な3D格子と多視点の視覚特徴を組み合わせたSLATを生成し、Radiance Field、3D Gaussians、Meshへデコード。テキスト・画像条件と局所編集を提示（要旨、Fig. 1・7）。 | 「潜在表現の出力形式と編集を選べる」。 |
| Hunyuan3D 2.0 | 形状生成のHunyuan3D-DiTと、生成または既存Meshにも使えるテクスチャ合成のHunyuan3D-Paintを構成要素とする（要旨、Fig. 1）。 | 「幾何と外観の生成段を分ける」。 |
| Seed3D 1.0 | 単一画像から幾何・整合したテクスチャ・PBR材質を生成し、物理エンジンへ統合する用途を示す（要旨、Fig. 1・11）。 | 「出力物の下流利用を物理シミュレーションまで想定」。 |

「表現の選択幅」「生成後の接続先」は4研究を並べるための今回の整理軸であり、論文著者の分類ではない。課題、入力、データ、評価指標、モデル世代が一致する対照実験ではないため、優劣・因果的進歩の根拠にしない。
