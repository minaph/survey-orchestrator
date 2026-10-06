# 出典・根拠

調査日：2026-10-07。ユーザー指定の3論文を一次資料（CVF Open Access版）で確認した。追加の文献候補探索は行っていない。

1. Jeong Joon Park, Peter Florence, Julian Straub, Richard Newcombe, Steven Lovegrove. “DeepSDF: Learning Continuous Signed Distance Functions for Shape Representation.” *Proceedings of CVPR*, 2019, pp. 165–174. [CVF論文ページ](https://openaccess.thecvf.com/content_CVPR_2019/html/Park_DeepSDF_Learning_Continuous_Signed_Distance_Functions_for_Shape_Representation_CVPR_2019_paper.html) · [PDF](https://openaccess.thecvf.com/content_CVPR_2019/papers/Park_DeepSDF_Learning_Continuous_Signed_Distance_Functions_for_Shape_Representation_CVPR_2019_paper.pdf)
   - 根拠：要旨と§3（符号付き距離、内側は負・外側は正、表面はゼロ等値面）、§4（形状クラスの表現、補間・補完）。
2. Lars Mescheder, Michael Oechsle, Michael Niemeyer, Sebastian Nowozin, Andreas Geiger. “Occupancy Networks: Learning 3D Reconstruction in Function Space.” *Proceedings of CVPR*, 2019, pp. 4460–4470. [CVF論文ページ](https://openaccess.thecvf.com/content_CVPR_2019/html/Mescheder_Occupancy_Networks_Learning_3D_Reconstruction_in_Function_Space_CVPR_2019_paper.html) · [PDF](https://openaccess.thecvf.com/content_CVPR_2019/papers/Mescheder_Occupancy_Networks_Learning_3D_Reconstruction_in_Function_Space_CVPR_2019_paper.pdf)
   - 根拠：要旨と図1（空間を離散化する既存表現と、分類器の連続決定境界を表面とする方式の対比）、§3、単一画像・ノイズを含む点群・粗い voxel 入力からの再構成実験の記述。
3. Zhiqin Chen, Hao Zhang. “Learning Implicit Fields for Generative Shape Modeling.” *Proceedings of CVPR*, 2019, pp. 5939–5948. [CVF論文ページ](https://openaccess.thecvf.com/content_CVPR_2019/html/Chen_Learning_Implicit_Fields_for_Generative_Shape_Modeling_CVPR_2019_paper.html) · [PDF](https://openaccess.thecvf.com/content_CVPR_2019/papers/Chen_Learning_Implicit_Fields_for_Generative_Shape_Modeling_CVPR_2019_paper.pdf)
   - 根拠：要旨、図2、§§3–4（IM-NETは点座標と形状特徴を入力し、形状の内外値を出力する暗黙場デコーダ。IM-AE / IM-GANを含む生成・再構成での利用）。学習時の形状と推論時のサンプル解像度の説明も確認。

## 使用図・来歴

- 納品図：[`figures/mescheder-fig1.png`](figures/mescheder-fig1.png)
- 原資料：Mescheder et al. (2019), Fig. 1, 論文1ページ目（CVF PDF）。図注は「既存表現が出力空間を異なる仕方で離散化する一方、同論文は分類器の連続決定境界を3D表面とみなす」という対比を示す。
- 取得・加工：CVFの一次資料PDFを取得し、1ページ目を300 dpiで描画。余白と本文を切り、図1のパネルと元のパネル名（Voxel / Point / Mesh / Ours）を含む範囲を切り抜いた。描き直し、色変更、要素追加は行っていない。切り抜き後の図をスライド左上へ配置し、すぐ下とスライド末尾で帰属を表示。
- 権利・来歴：CVFページは著作権が著者または権利者に留保されると明記している。引用・掲示の適法性や公開先の利用条件をこの制作で独立判定したわけではない。公開・再配布の前に利用先の条件を確認すること。
- 残り2論文の方法図は転載していない。各モデルの説明はスライド下段の文と出典表示に対応する。図だけから3論文の全差異が読み取れるとは主張しない。
