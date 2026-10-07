# デザイン資料の採用範囲

この対応表は、`cross-media-design-decision-support` の資料登録簿から、文献サーベイの発表と配布に役立つ内容を選んだものです。Webの部品仕様、ポスターの物理寸法、ブランド資産を、投影スライドの共通規則として流用しません。外部資料はデザイン判断の参考であり、調査対象分野の根拠件数には含めません。

公式の6ページの本文を2026年10月7日（日本時間）に取得し、以下の採用範囲と照合しました。

## 本文を確認して採用した内容

| 資料 | 採用する内容 | このスキルでの使い方と限界 |
| --- | --- | --- |
| デジタル庁デザインシステム：タイポグラフィ | 文字の役割と階層、読みやすいまとまりを考える | 見出し・主根拠・補足・出典の役割を分ける。Web用の文字サイズや余白値を投影の合格値にはしない |
| Carbon：Chart anatomy・Data visualization overview | 読みたい関係に合う図の選択、軸・凡例・ラベル・文脈の構成 | 比較、推移、分布、関係を別の型として扱い、条件と不確実性を保持する。UI部品やブランドの見た目をそのまま移さない |
| GOV.UK：Layout | 内容の主従に応じた配置 | 主根拠と補足の領域を分ける。Webのグリッド幅を固定スライドへそのまま適用しない |
| PLOS：Ten Simple Rules for a Good Poster Presentation | 読み手を想定し、主題と重要な結果へ内容を絞る | 冒頭で問いと重要性が分かるようにする。ポスターの観察距離・文字寸法・閲覧時間を口頭発表へ移さない |
| W3C：WCAGのUse of Colorの解説 | 色だけを情報の手掛かりにしない | 群名、直接ラベル、記号、線種を併用する。Webの適合基準を根拠なく投影品質の保証としない |

テンプレートの分類・配置・架空事例は、本スキルの目的に合わせて独自に作成します。上の資料が、同じ16種類の型や配置を提唱しているという意味ではありません。外部の図、アイコン、ブランド資産を転載する前提にもしていません。

### 参照先

- [DADS：タイポグラフィ](https://design.digital.go.jp/dads/foundations/typography/)
- [Carbon：Chart anatomy](https://carbondesignsystem.com/data-visualization/chart-anatomy/)
- [Carbon：Data visualization overview](https://carbondesignsystem.com/data-visualization/overview/)
- [GOV.UK：Layout](https://design-system.service.gov.uk/styles/layout/)
- [PLOS：Ten Simple Rules for a Good Poster Presentation](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.0030102)
- [W3C：Understanding Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

採用する資料の仕様・利用条件が成果物へ影響する場合は、その制作時にも原資料を確認します。この対応表は、各サイトの全ページや資産の利用条件を検証した記録ではありません。

## 媒体が該当するときだけ参照する資料

| 登録資料 | 使う条件 | 今回の扱い |
| --- | --- | --- |
| W3C CSS Paged Media・CSS Color Adjustment | HTMLから配布用PDFや印刷物を制作する | ページ寸法・改ページ・印刷色の挙動を確認する際の参照先。画面表示だけで印刷結果を保証しない |
| WCAG 2.2のその他の達成基準 | HTML配布版・Web公開版でアクセシビリティを評価する | 実装した構造・操作・可変幅に関係する範囲を選ぶ。静的スライドへフォームや操作対象の検査を持ち込まない |
| DADS・GOV.UK・USWDS・Material・Fluent・PrimerのUI部品 | 検索可能な文献一覧や対話的な付録を別途作る | 現在の静的なスライド型へUI一式を導入しない |

条件付き資料の入口は [CSS Paged Media](https://www.w3.org/TR/css-page-3/)、[CSS Color Adjustment](https://www.w3.org/TR/css-color-adjust-1/)、[WCAG 2.2](https://www.w3.org/TR/WCAG22/) です。採用しない資料の現行仕様まで確認済みという意味ではありません。

## 今回は採用しないもの

Material Symbols、Fluent System Icons、Primer Octicons、デジタル庁のイラストは、具体的に必要な概念や操作を補う場合に検討できます。ただし、研究の比較・方法・結果を一般的なアイコンで代替したり、余白を埋める装飾として導入したりする理由にはなりません。今回のテンプレートでは、これらの装飾資産は使いません。提供されたMIRU資料からの図の抜粋は、研究紹介の情報構成を検討する実例として別に扱い、[分析プロファイル](miru-style-profile.md)に直接の出所と確認範囲を示します。

Appleのマーケティング資産、デジタル庁のロゴ、デジタルマーケットプレイスのブランド運用は、現在の文献サーベイの問いや根拠を伝えるための要件ではないため採用しません。ブランドや配布先が具体的に指定された案件では、その条件として改めて確認します。

## テンプレートへの反映

[サーベイ発表の分析](survey-design-analysis.md)では、主張・根拠・補足・参照の順序と空間配分を判断します。[テンプレート集](survey-slide-templates.md)では、問い、概念、調査過程、分類、原図、比較、推移、不確実性、反証、不足、統合、結論、参照先という異なる情報の役割を、異なる配置として示します。

型の採用後も、出典の支持、意味の境界、原図との対応を先に確認します。簡素な見た目は、調査の限界や反証を消す理由にはなりません。デザインの形成と、完成物を実際に確認した結果は分けて記録してください。
