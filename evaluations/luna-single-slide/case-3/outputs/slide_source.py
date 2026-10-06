#!/usr/bin/env python3
"""Build a one-slide editable SVG and export-ready PNG/PDF."""
from base64 import b64encode
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INK = "#183346"
TEXT = "#253B49"
MUTED = "#5C707A"
BG = "#F4F7F6"
WHITE = "#FFFFFF"
TEAL = "#07877E"
BLUE = "#4B70B4"
CORAL = "#D36C52"
PALE = "#E4F2EF"
LINE = "#D8E2E0"
FONT = "'Hiragino Kaku Gothic ProN','PlemolJP',sans-serif"

def t(x, y, s, size=18, color=TEXT, weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}px" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(s)}</text>')

def r(x, y, w, h, color, radius=14, stroke="none", sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{color}" stroke="{stroke}" stroke-width="{sw}"/>'

def build_svg():
    fig = b64encode((ROOT / "figures/mescheder-fig1.png").read_bytes()).decode("ascii")
    e = []
    e += ['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">',
          r(0,0,1600,900,BG,0), r(0,0,12,900,TEAL,0),
          t(66,52,"3D SHAPE REPRESENTATION   /   CVPR 2019",14,TEAL,700),
          t(66,108,"表面を「場の境界」として表す",42,INK,700),
          t(68,147,"同じ連続場の考え方から、3つの代表モデルを位置づける",20,MUTED),
          # The source figure is retained without redrawing or modification.
          r(65,176,695,343,WHITE,17,LINE,1.5),
          f'<image x="83" y="190" width="659" height="311" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{fig}"/>',
          t(84,544,"原図：Mescheder et al., Fig. 1。右端が連続場の決定境界。",14,MUTED),
          # Core definition and boundary distinction
          r(791,176,743,343,WHITE,17,LINE,1.5),
          t(823,216,"共通の考え方",16,TEAL,700),
          t(823,270,"各点 x ∈ ℝ³ で場の値を評価",23,INK,700),
          t(823,323,"表面 S = { x | fθ(x, z) = τ }",25,INK,700),
          t(823,366,"z：形状コード／特徴　　τ：境界のしきい値",16,MUTED),
          f'<path d="M825 406 H1495" stroke="{LINE}" stroke-width="1.5"/>',
          t(823,443,"Occupancy / IM-NET：内外を分ける分類境界",17,TEXT,600),
          t(823,476,"DeepSDF：符号付き距離のゼロ面（τ = 0）",17,TEXT,600),
          t(823,503,"場を連続的に表現し、必要な位置で問い合わせる。",15,MUTED),
          # Model comparison cards
          r(65,575,468,216,WHITE,16,LINE,1.4), r(65,575,468,7,BLUE,4),
          t(88,615,"Occupancy Networks",22,INK,700),
          t(88,649,"占有を表す分類場",16,BLUE,700),
          t(88,684,"連続な決定境界を表面とする。",16,TEXT),
          t(88,714,"画像・点群・粗い voxel から3D再構成。",15,TEXT),
          t(88,765,"Mescheder et al. · CVPR 2019 · pp. 4460–4470",12,MUTED),
          r(566,575,468,216,WHITE,16,LINE,1.4), r(566,575,468,7,CORAL,4),
          t(589,615,"DeepSDF",22,INK,700),
          t(589,649,"符号付き距離場",16,CORAL,700),
          t(589,684,"距離の絶対値と内外の符号を学ぶ。",16,TEXT),
          t(589,714,"形状クラスの表現・補間・部分形状補完。",15,TEXT),
          t(589,765,"Park et al. · CVPR 2019 · pp. 165–174",12,MUTED),
          r(1067,575,467,216,WHITE,16,LINE,1.4), r(1067,575,467,7,TEAL,4),
          t(1090,615,"IM-NET（Chen & Zhang）",22,INK,700),
          t(1090,649,"形状条件付きの暗黙場デコーダ",16,TEAL,700),
          t(1090,684,"座標と形状特徴から内外値を出力。",16,TEXT),
          t(1090,714,"IM-AE / IM-GAN の生成・再構成に利用。",15,TEXT),
          t(1090,765,"Chen & Zhang · CVPR 2019 · pp. 5939–5948",12,MUTED),
          # Synthesis, limitation and complete visible attributions
          r(65,812,1469,48,PALE,12),
          t(86,842,"要点",14,TEAL,700),
          t(145,842,"共通点は「連続場 → 境界抽出」；違いは場の値と、形状を得る経路。",17,INK,700),
          t(68,883,"注意：場を任意位置で評価できることは、有限解像度で抽出するメッシュの精度を保証しない。図は原図、式とモデル要約は論文本文に基づく。",12,MUTED),
          '</svg>']
    return "\n".join(e)

if __name__ == "__main__":
    (ROOT / "slide.svg").write_text(build_svg(), encoding="utf-8")
