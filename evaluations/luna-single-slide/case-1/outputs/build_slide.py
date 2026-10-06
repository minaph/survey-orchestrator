#!/usr/bin/env python3
"""Generate the editable SVG for the one-slide 3D generation research synthesis."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "slide.svg"

svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#F7F9FB"/><stop offset="1" stop-color="#EDF2F6"/></linearGradient>
 <filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="7" stdDeviation="12" flood-color="#183047" flood-opacity=".08"/></filter>
 <style>
 text{font-family:"Hiragino Sans","Noto Sans CJK JP",sans-serif;fill:#182A3C}
 .eyebrow{font-size:18px;font-weight:700;letter-spacing:2px;fill:#46627C}
 .title{font-size:48px;font-weight:700;letter-spacing:-.5px}
 .sub{font-size:22px;fill:#526579}
 .period{font-size:17px;font-weight:700;letter-spacing:1.2px}
 .paper{font-size:28px;font-weight:700}
 .line{font-size:19px;fill:#364C61}
 .label{font-size:16px;font-weight:700;letter-spacing:1px;fill:#64778A}
 .step{font-size:18px;font-weight:600}
 .source{font-size:16px;fill:#536679}
 .note{font-size:17px;fill:#536679}
 .on-dark{fill:#FFFFFF}
 .on-dark-soft{fill:#D2DEE8}
 .on-dark-muted{fill:#AEC2D5}
 </style>
</defs>
<rect width="1920" height="1080" fill="url(#bg)"/><rect width="1920" height="11" fill="#315A7D"/>
<text x="80" y="61" class="eyebrow">3D GENERATION / RESEARCH SNAPSHOT</text>
<text x="80" y="119" class="title">3D生成モデルは「表現」と「出口」の設計で分かれる</text>
<text x="80" y="161" class="sub">指定4研究を比較：何を直接生成し、どんな出力形式・利用先へつなぐか</text>
<text x="1840" y="64" text-anchor="end" class="note">2023–2025</text>

<!-- Four source-figure panels: the referenced images are cropped from each paper's Figure 1. -->
<g filter="url(#shadow)"><rect x="80" y="200" width="426" height="603" rx="20" fill="#FFF"/><rect x="526" y="200" width="426" height="603" rx="20" fill="#FFF"/><rect x="972" y="200" width="426" height="603" rx="20" fill="#FFF"/><rect x="1418" y="200" width="422" height="603" rx="20" fill="#FFF"/></g>
<rect x="80" y="200" width="426" height="8" rx="4" fill="#3873A8"/><rect x="526" y="200" width="426" height="8" rx="4" fill="#6573C2"/><rect x="972" y="200" width="426" height="8" rx="4" fill="#C27C39"/><rect x="1418" y="200" width="422" height="8" rx="4" fill="#3E8B78"/>

<!-- Shap-E -->
<g transform="translate(104 230)">
 <text class="period" fill="#3873A8">2023　/　暗黙関数</text><text y="39" class="paper">Shap·E</text>
 <rect x="0" y="54" width="378" height="158" rx="9" fill="#F5F8FA"/>
 <image href="figures/shap_e_fig1_crop.png" x="0" y="54" width="378" height="158" preserveAspectRatio="xMidYMid meet"/>
 <text y="231" class="label">直接生成するもの</text>
 <text y="261" class="line">条件付き拡散 → 暗黙関数のパラメータ</text>
 <path d="M8 283H370" stroke="#DCE5EC" stroke-width="2"/>
 <text y="316" class="label">出力・特徴</text>
 <text y="346" class="line">Mesh と NeRF の両方へ描画</text>
 <text y="388" class="line">関数表現から複数形式へ。</text>
 <text y="434" class="source">図：Jun &amp; Nichol (2023), Fig. 1</text>
 <text y="459" class="source">arXiv:2305.02463, p.2</text>
</g>

<!-- Structured latents -->
<g transform="translate(550 230)">
 <text class="period" fill="#6573C2">2024 / CVPR 2025　・　構造化潜在</text><text y="39" class="paper">Structured 3D Latents</text>
 <rect x="0" y="54" width="378" height="158" rx="9" fill="#F7F7FB"/>
 <image href="figures/trellis_fig1_crop.png" x="0" y="54" width="378" height="158" preserveAspectRatio="xMidYMid meet"/>
 <text y="231" class="label">直接生成するもの</text>
 <text y="261" class="line">二段階Flow → 疎構造＋局所特徴（SLAT）</text>
 <path d="M8 283H370" stroke="#DCE5EC" stroke-width="2"/>
 <text y="316" class="label">出力・特徴</text>
 <text y="346" class="line">Gaussians / Radiance Field / Mesh</text>
 <text y="372" class="line">出力形式の選択と局所編集</text>
 <text y="414" class="line">潜在表現を複数形式へデコード。</text>
 <text y="448" class="source">図：Xiang et al. (2025), Fig. 1</text>
 <text y="473" class="source">arXiv:2412.01506, p.1</text>
</g>

<!-- Hunyuan -->
<g transform="translate(996 230)">
 <text class="period" fill="#B66C2D">2025　/　形状＋テクスチャ</text><text y="39" class="paper">Hunyuan3D 2.0</text>
 <rect x="0" y="54" width="378" height="158" rx="9" fill="#FBF6F0"/>
 <image href="figures/hunyuan_fig1_crop.png" x="0" y="54" width="378" height="158" preserveAspectRatio="xMidYMid meet"/>
 <text y="231" class="label">直接生成するもの</text>
 <text y="261" class="line">形状 DiT ＋ 専用 Paint モデル</text>
 <path d="M8 283H370" stroke="#DCE5EC" stroke-width="2"/>
 <text y="316" class="label">出力・特徴</text>
 <text y="346" class="line">高解像度テクスチャ付き3D資産</text>
 <text y="388" class="line">幾何と外観を分けて生成。</text>
 <text y="434" class="source">図：Hunyuan3D Team (2025), Fig. 1</text>
 <text y="459" class="source">arXiv:2501.12202, p.2</text>
</g>

<!-- Seed3D -->
<g transform="translate(1442 230)">
 <text class="period" fill="#3E8B78">2025　/　シミュレーション用途</text><text y="39" class="paper">Seed3D 1.0</text>
 <rect x="0" y="54" width="374" height="158" rx="9" fill="#F3F8F6"/>
 <image href="figures/seed3d_fig1_crop.png" x="0" y="54" width="374" height="158" preserveAspectRatio="xMidYMid meet"/>
 <text y="231" class="label">直接生成するもの</text>
 <text y="261" class="line">単一画像 → 幾何・テクスチャ・PBR</text>
 <path d="M8 283H366" stroke="#DCE5EC" stroke-width="2"/>
 <text y="316" class="label">出力・特徴</text>
 <text y="346" class="line">物理エンジン向け資産・シーン</text>
 <text y="388" class="line">下流のシミュレーションへ接続。</text>
 <text y="434" class="source">図：ByteDance Seed (2025), Fig. 1</text>
 <text y="459" class="source">arXiv:2510.19944, p.1</text>
</g>

<!-- synthesis -->
<rect x="80" y="830" width="1760" height="108" rx="18" fill="#17324A"/>
<text x="112" y="868" class="on-dark-muted" font-size="17" font-weight="700" letter-spacing="1">横断して見える設計軸</text>
<text x="112" y="909" class="on-dark" font-size="25" font-weight="700">表現の選択幅</text>
<text x="354" y="909" class="on-dark-soft" font-size="21">Shap·E / Structured 3D Latents</text>
<path d="M807 851V918" stroke="#486177" stroke-width="2"/>
<text x="844" y="909" class="on-dark" font-size="25" font-weight="700">生成後の接続先</text>
<text x="1100" y="909" class="on-dark-soft" font-size="21">Hunyuan3D：外観制作　｜　Seed3D：物理シミュレーション</text>
<text x="80" y="976" class="note">この比較は設計焦点の整理です。入力・課題・評価条件が異なるため、品質順位や因果的な進歩を示しません。</text>
<text x="80" y="1005" class="source">出典：Jun &amp; Nichol, “Shap-E” (2023), arXiv:2305.02463　・　Xiang et al., “Structured 3D Latents” (CVPR 2025), arXiv:2412.01506</text>
<text x="80" y="1032" class="source">Hunyuan3D Team, “Hunyuan3D 2.0” (2025), arXiv:2501.12202　・　ByteDance Seed, “Seed3D 1.0” (2025), arXiv:2510.19944</text>
</svg>'''

OUT.write_text(svg, encoding="utf-8")
print(f"Wrote {OUT}")
