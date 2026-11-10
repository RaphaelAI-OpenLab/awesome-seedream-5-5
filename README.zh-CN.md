<!-- 由 scripts/build.py 生成，请编辑 content/ 内的数据。 -->

[![Seedream 5.5 提示词与案例合集](assets/header.svg)](https://raphael.app/?utm_source=github&utm_medium=repository&utm_campaign=seedream_5_5)

# Seedream 5.5 提示词与案例合集

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![Stars](https://img.shields.io/github/stars/RaphaelAI-OpenLab/awesome-seedream-5-5?style=social)](https://github.com/RaphaelAI-OpenLab/awesome-seedream-5-5) [![Validate](https://github.com/RaphaelAI-OpenLab/awesome-seedream-5-5/actions/workflows/validate.yml/badge.svg)](https://github.com/RaphaelAI-OpenLab/awesome-seedream-5-5/actions/workflows/validate.yml) [![MIT](https://img.shields.io/badge/code-MIT-lightgrey)](LICENSE)

[English](README.md) · [简体中文](README.zh-CN.md)

由 Raphael 整理的图片与编辑案例库。官方展示、作者自报结果与本仓库编写的练习提示词分别标记。

**59 个来源案例 · 8 个分类 · 8 份原创练习配方 · 3 条已核对社媒来源（2 份不同素材）**

案例未由本仓库独立复现。仓库只保存缩放后的单帧预览，完整图片、GIF 与视频链接至原始地址；第三方媒体及其预览的版权归原权利人。

[浏览案例](#cases) · [练习提示词](#recipes) · [社媒原帖](#social) · [投稿](CONTRIBUTING.md) · [来源与核验](docs/SOURCES.md)

## 模型与入口

Seedream 5.5 的官方发布日期为 **2026-11-09**。能力和入口以[官方模型页](https://seed.bytedance.com/en/seedream5_5)与[中文发布说明](https://seed.bytedance.com/zh/blog/more-realistic-images-more-stable-editing-across-100-rounds-introducing-seedream-5-5)为准。

[访问 Raphael](https://raphael.app/?utm_source=github&utm_medium=repository&utm_campaign=seedream_5_5)。这是品牌主页链接；本仓库尚未核实 Raphael 是否提供 Seedream 5.5，也不提供模型 API 或权重。

## 收录口径

| 项目 | 数量 |
| --- | ---: |
| 官方来源案例 | 20 |
| 作者自报案例 | 39 |
| 仓库内完整原始提示词 | 14 |
| 独立复现案例 | 0 |
| 来源核对日期 | 2026-11-10 |

同一案例的多轮图片不重复计数；重复社媒视频不增加案例总数。来源页中的展示说明不等于实际完整生成提示词。

<a id="categories"></a>
## 按分类浏览

| 分类 | 案例数 |
| --- | ---: |
| [多轮与局部编辑](#multi-turn-editing) | 5 |
| [透明素材](#rgba-assets) | 9 |
| [人像](#portraits) | 2 |
| [摄影与纪实](#photography) | 20 |
| [室内与空间](#interiors) | 1 |
| [文字与排版](#typography) | 11 |
| [信息图与界面](#infographics) | 4 |
| [角色与贴纸](#characters) | 7 |

<a id="cases"></a>
## 全部案例

<a id="multi-turn-editing"></a>
### 多轮与局部编辑

#### [人像连续编辑](cases/official-portrait-editing/README.zh-CN.md)

<a href="cases/official-portrait-editing/README.zh-CN.md"><img src="assets/previews/official-portrait-editing.jpg" alt="人像连续编辑" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-portrait-editing/README.zh-CN.md)

#### [静物连续编辑](cases/official-still-life-editing/README.zh-CN.md)

<a href="cases/official-still-life-editing/README.zh-CN.md"><img src="assets/previews/official-still-life-editing.jpg" alt="静物连续编辑" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-still-life-editing/README.zh-CN.md)

#### [国画连续编辑](cases/official-ink-painting-editing/README.zh-CN.md)

<a href="cases/official-ink-painting-editing/README.zh-CN.md"><img src="assets/previews/official-ink-painting-editing.jpg" alt="国画连续编辑" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-ink-painting-editing/README.zh-CN.md)

#### [纸条局部编辑](cases/quantslant-note-edit/README.zh-CN.md)

<a href="cases/quantslant-note-edit/README.zh-CN.md"><img src="assets/previews/quantslant-note-edit.jpg" alt="纸条局部编辑" width="420" loading="lazy" /></a>

作者自报 · Piotr Olszewski / QUANTSLANT · [原始来源](https://quantslant.com/seedream-5-5-features-pricing-benchmarks/) · [详情与提示词状态](cases/quantslant-note-edit/README.zh-CN.md)

#### [连续修改 30 轮的 LLM 原理图](cases/socialx-llm-diagram-edits/README.zh-CN.md)

<a href="cases/socialx-llm-diagram-edits/README.zh-CN.md"><img src="assets/previews/socialx-llm-diagram-edits-01.jpg" alt="连续修改 30 轮的 LLM 原理图" width="420" loading="lazy" /></a>

作者自报 · dongxi_nlp · [原始来源](https://x.com/dongxi_nlp/status/2120031669893939524) · [详情与提示词状态](cases/socialx-llm-diagram-edits/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 作者表示对同一张 LLM 原理图连续修改了三十轮。

<a id="rgba-assets"></a>
### 透明素材

#### [火烈鸟图层](cases/official-flamingo-layer/README.zh-CN.md)

<a href="cases/official-flamingo-layer/README.zh-CN.md"><img src="assets/previews/official-flamingo-layer.jpg" alt="火烈鸟图层" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-flamingo-layer/README.zh-CN.md)

#### [雪鸮微距](cases/official-owl-macro/README.zh-CN.md)

<a href="cases/official-owl-macro/README.zh-CN.md"><img src="assets/previews/official-owl-macro.jpg" alt="雪鸮微距" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-owl-macro/README.zh-CN.md)

#### [雨衣角色](cases/quantslant-raincoat-character/README.zh-CN.md)

<a href="cases/quantslant-raincoat-character/README.zh-CN.md"><img src="assets/previews/quantslant-raincoat-character.jpg" alt="雨衣角色" width="420" loading="lazy" /></a>

作者自报 · Piotr Olszewski / QUANTSLANT · [原始来源](https://quantslant.com/seedream-5-5-features-pricing-benchmarks/) · [详情与提示词状态](cases/quantslant-raincoat-character/README.zh-CN.md)

> 作者报告伞面呈乳白色，半透明材质表现存在局限。

#### [香水瓶透明背景素材](cases/social-dheepan-amber-perfume/README.zh-CN.md)

<a href="cases/social-dheepan-amber-perfume/README.zh-CN.md"><img src="assets/previews/social-dheepan-amber-perfume.jpg" alt="香水瓶透明背景素材" width="420" loading="lazy" /></a>

作者自报 · Dheepanratnam · [原始来源](https://x.com/Dheepanratnam/status/2119775195573481859) · [详情与提示词状态](cases/social-dheepan-amber-perfume/README.zh-CN.md)

> 来自公开整理站的作者归因图片与提示词，未在本仓库独立复现。图像为缩小版，非原始导出。 这张 JPEG 不能证明原始 Alpha 透明度。

#### [街头模特透明背景素材](cases/social-dheepan-streetwear-cutout/README.zh-CN.md)

<a href="cases/social-dheepan-streetwear-cutout/README.zh-CN.md"><img src="assets/previews/social-dheepan-streetwear-cutout.jpg" alt="街头模特透明背景素材" width="420" loading="lazy" /></a>

作者自报 · Dheepanratnam · [原始来源](https://x.com/Dheepanratnam/status/2119775195573481859) · [详情与提示词状态](cases/social-dheepan-streetwear-cutout/README.zh-CN.md)

> 来自公开整理站的作者归因图片与提示词，未在本仓库独立复现。图像为缩小版，非原始导出。 这张 JPEG 不能证明原始 Alpha 透明度。

#### [双风格透明角色素材](cases/socialx-transparent-character/README.zh-CN.md)

<a href="cases/socialx-transparent-character/README.zh-CN.md"><img src="assets/previews/socialx-transparent-character-01.jpg" alt="双风格透明角色素材" width="420" loading="lazy" /></a>

作者自报 · KakiponzuX · [原始来源](https://x.com/KakiponzuX/status/2119979776651710778) · [详情与提示词状态](cases/socialx-transparent-character/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 缩略图无法证明原始Alpha透明度。 插画与写实风格透明度测试；作者报告部分输出丢失 alpha，棋盘格图片是合成预览。 原帖公开了透明背景提示词后缀，但未提供完整身份设定指令。

#### [玻璃水母灯](cases/socialx-glass-jellyfish-lamp/README.zh-CN.md)

<a href="cases/socialx-glass-jellyfish-lamp/README.zh-CN.md"><img src="assets/previews/socialx-glass-jellyfish-lamp-01.jpg" alt="玻璃水母灯" width="420" loading="lazy" /></a>

作者自报 · ahmetmertugrul · [原始来源](https://x.com/ahmetmertugrul/status/2119920477535719739) · [详情与提示词状态](cases/socialx-glass-jellyfish-lamp/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 缩略图无法证明原始Alpha透明度。 原帖附提示词的玻璃灯透明素材示例；仅凭展示图不能验证文件的 alpha 通道。

#### [磨砂亚克力板透明素材](cases/social-dheepan-frosted-acrylic/README.zh-CN.md)

<a href="cases/social-dheepan-frosted-acrylic/README.zh-CN.md"><img src="assets/previews/social-dheepan-frosted-acrylic-01.jpg" alt="磨砂亚克力板透明素材" width="420" loading="lazy" /></a>

作者自报 · Dheepanratnam · [原始来源](https://x.com/Dheepanratnam/status/2119775195573481859) · [详情与提示词状态](cases/social-dheepan-frosted-acrylic/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 缩略图无法证明原始Alpha透明度。

#### [铬金属流体丝带透明素材](cases/social-dheepan-chrome-ribbon/README.zh-CN.md)

<a href="cases/social-dheepan-chrome-ribbon/README.zh-CN.md"><img src="assets/previews/social-dheepan-chrome-ribbon-01.jpg" alt="铬金属流体丝带透明素材" width="420" loading="lazy" /></a>

作者自报 · Dheepanratnam · [原始来源](https://x.com/Dheepanratnam/status/2119775195573481859) · [详情与提示词状态](cases/social-dheepan-chrome-ribbon/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 缩略图无法证明原始Alpha透明度。

<a id="portraits"></a>
### 人像

#### [妆发连续编辑](cases/official-beauty-editing/README.zh-CN.md)

<a href="cases/official-beauty-editing/README.zh-CN.md"><img src="assets/previews/official-beauty-editing.jpg" alt="妆发连续编辑" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-beauty-editing/README.zh-CN.md)

#### [雀斑人像](cases/quantslant-freckled-portrait/README.zh-CN.md)

<a href="cases/quantslant-freckled-portrait/README.zh-CN.md"><img src="assets/previews/quantslant-freckled-portrait.jpg" alt="雀斑人像" width="420" loading="lazy" /></a>

作者自报 · Piotr Olszewski / QUANTSLANT · [原始来源](https://quantslant.com/seedream-5-5-features-pricing-benchmarks/) · [详情与提示词状态](cases/quantslant-freckled-portrait/README.zh-CN.md)

<a id="photography"></a>
### 摄影与纪实

#### [酒吧白猫](cases/official-bar-cat/README.zh-CN.md)

<a href="cases/official-bar-cat/README.zh-CN.md"><img src="assets/previews/official-bar-cat.jpg" alt="酒吧白猫" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-bar-cat/README.zh-CN.md)

#### [紫黄街景](cases/official-purple-yellow-street/README.zh-CN.md)

<a href="cases/official-purple-yellow-street/README.zh-CN.md"><img src="assets/previews/official-purple-yellow-street.jpg" alt="紫黄街景" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-purple-yellow-street/README.zh-CN.md)

#### [风中街拍](cases/official-windy-street/README.zh-CN.md)

<a href="cases/official-windy-street/README.zh-CN.md"><img src="assets/previews/official-windy-street.jpg" alt="风中街拍" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-windy-street/README.zh-CN.md)

#### [小酒馆](cases/official-bistro/README.zh-CN.md)

<a href="cases/official-bistro/README.zh-CN.md"><img src="assets/previews/official-bistro.jpg" alt="小酒馆" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-bistro/README.zh-CN.md)

#### [雨后倒影](cases/official-rain-reflections/README.zh-CN.md)

<a href="cases/official-rain-reflections/README.zh-CN.md"><img src="assets/previews/official-rain-reflections.jpg" alt="雨后倒影" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-rain-reflections/README.zh-CN.md)

#### [黄昏火车站](cases/quantslant-railway-station/README.zh-CN.md)

<a href="cases/quantslant-railway-station/README.zh-CN.md"><img src="assets/previews/quantslant-railway-station.jpg" alt="黄昏火车站" width="420" loading="lazy" /></a>

作者自报 · Piotr Olszewski / QUANTSLANT · [原始来源](https://quantslant.com/seedream-5-5-features-pricing-benchmarks/) · [详情与提示词状态](cases/quantslant-railway-station/README.zh-CN.md)

#### [日本熟食店三模型对比](cases/social-genel-japanese-deli/README.zh-CN.md)

<a href="cases/social-genel-japanese-deli/README.zh-CN.md"><img src="assets/previews/social-genel-japanese-deli.jpg" alt="日本熟食店三模型对比" width="420" loading="lazy" /></a>

作者自报 · genel_ai · [原始来源](https://x.com/genel_ai/status/2119786434567827504) · [详情与提示词状态](cases/social-genel-japanese-deli/README.zh-CN.md)

> 来自公开整理站的作者归因图片与提示词，未在本仓库独立复现。图像为缩小版，非原始导出。 此图是三模型比较拼图，Seedream 5.5 为左侧列。

#### [肤质表现测试](cases/socialx-skin-texture-test/README.zh-CN.md)

<a href="cases/socialx-skin-texture-test/README.zh-CN.md"><img src="assets/previews/socialx-skin-texture-test-01.jpg" alt="肤质表现测试" width="420" loading="lazy" /></a>

作者自报 · oden_ai_ai · [原始来源](https://x.com/oden_ai_ai/status/2120015332530393282) · [详情与提示词状态](cases/socialx-skin-texture-test/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 作者分享的图片测试，关注模型对皮肤质感的表现。

#### [四模型人像测试](cases/socialx-four-model-portrait/README.zh-CN.md)

<a href="cases/socialx-four-model-portrait/README.zh-CN.md"><img src="assets/previews/socialx-four-model-portrait-01.jpg" alt="四模型人像测试" width="420" loading="lazy" /></a>

作者自报 · 94vanAI · [原始来源](https://x.com/94vanAI/status/2119938579078238370) · [详情与提示词状态](cases/socialx-four-model-portrait/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 原帖为多模型对比，部分图片来自其他模型，需按原帖标签区分。 作者注明第一张为 Seedream，其后为 ChatGPT、Gemini、Grok，同时讨论优点与局限。

#### [同提示词纹理对比](cases/socialx-same-prompt-texture/README.zh-CN.md)

<a href="cases/socialx-same-prompt-texture/README.zh-CN.md"><img src="assets/previews/socialx-same-prompt-texture-01.jpg" alt="同提示词纹理对比" width="420" loading="lazy" /></a>

作者自报 · PowerUpInvest · [原始来源](https://x.com/PowerUpInvest/status/2119971057650262386) · [详情与提示词状态](cases/socialx-same-prompt-texture/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 作者与 GPT Image 2.6 进行图像质感对比；型号归属以原帖说明为准。

#### [三模型出图对比](cases/socialx-three-model-output/README.zh-CN.md)

<a href="cases/socialx-three-model-output/README.zh-CN.md"><img src="assets/previews/socialx-three-model-output-01.jpg" alt="三模型出图对比" width="420" loading="lazy" /></a>

作者自报 · Yuziyyaa · [原始来源](https://x.com/Yuziyyaa/status/2119991511433814093) · [详情与提示词状态](cases/socialx-three-model-output/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 原帖为多模型对比，部分图片来自其他模型，需按原帖标签区分。 作者按图片顺序标注 GPT Images 2.6、Seedream 5.0 Pro、Seedream 5.5。

#### [窗光胶片感人像](cases/socialx-window-light-portrait/README.zh-CN.md)

<a href="cases/socialx-window-light-portrait/README.zh-CN.md"><img src="assets/previews/socialx-window-light-portrait-01.jpg" alt="窗光胶片感人像" width="420" loading="lazy" /></a>

作者自报 · nima2qisi2 · [原始来源](https://x.com/nima2qisi2/status/2119983938383106432) · [详情与提示词状态](cases/socialx-window-light-portrait/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 使用窗光与胶片风格的人像组图，原帖包含作者提示词。

#### [复古电影静帧](cases/socialx-vintage-cinema/README.zh-CN.md)

<a href="cases/socialx-vintage-cinema/README.zh-CN.md"><img src="assets/previews/socialx-vintage-cinema-01.jpg" alt="复古电影静帧" width="420" loading="lazy" /></a>

作者自报 · ChrisGwinnLA · [原始来源](https://x.com/ChrisGwinnLA/status/2119979699464286506) · [详情与提示词状态](cases/socialx-vintage-cinema/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 单篇原帖中的四张复古风图片，合并计为一组案例。

#### [Seedream 与 MiniMax H3 静帧对比](cases/socialx-h3-frame-comparison/README.zh-CN.md)

<a href="cases/socialx-h3-frame-comparison/README.zh-CN.md"><img src="assets/previews/socialx-h3-frame-comparison-01.jpg" alt="Seedream 与 MiniMax H3 静帧对比" width="420" loading="lazy" /></a>

作者自报 · JSFILMZ0412 · [原始来源](https://x.com/JSFILMZ0412/status/2119889824274640957) · [详情与提示词状态](cases/socialx-h3-frame-comparison/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 原帖为多模型对比，部分图片来自其他模型，需按原帖标签区分。 作者说明为未经后期处理的两张 2K 静帧；另发的 H3 视频不计为 Seedream 成果。

#### [精灵人像材质测试](cases/socialx-elf-material-study/README.zh-CN.md)

<a href="cases/socialx-elf-material-study/README.zh-CN.md"><img src="assets/previews/socialx-elf-material-study-01.jpg" alt="精灵人像材质测试" width="420" loading="lazy" /></a>

作者自报 · nanyuan0412 · [原始来源](https://x.com/nanyuan0412/status/2119879195115332042) · [详情与提示词状态](cases/socialx-elf-material-study/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 皮肤、布料与光线的单图测试；作者明确表示尚未深度测试连续编辑。

#### [冬季人像对比](cases/socialx-winter-portrait-comparison/README.zh-CN.md)

<a href="cases/socialx-winter-portrait-comparison/README.zh-CN.md"><img src="assets/previews/socialx-winter-portrait-comparison-01.jpg" alt="冬季人像对比" width="420" loading="lazy" /></a>

作者自报 · 0kncn · [原始来源](https://x.com/0kncn/status/2119878902344823069) · [详情与提示词状态](cases/socialx-winter-portrait-comparison/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 原帖为多模型对比，部分图片来自其他模型，需按原帖标签区分。 作者用相同人像要求对比 GPT Image 2.5、Seedream 5.5 与 Nano Banana 2.1。

#### [写实图像组](cases/socialx-photoreal-image-set/README.zh-CN.md)

<a href="cases/socialx-photoreal-image-set/README.zh-CN.md"><img src="assets/previews/socialx-photoreal-image-set-01.jpg" alt="写实图像组" width="420" loading="lazy" /></a>

作者自报 · uixmax · [原始来源](https://x.com/uixmax/status/2119894564073054374) · [详情与提示词状态](cases/socialx-photoreal-image-set/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 作者的四图写实效果测试，保留为一组来源案例。

#### [人像模型顺序对照](cases/socialx-three-model-portrait-order/README.zh-CN.md)

<a href="cases/socialx-three-model-portrait-order/README.zh-CN.md"><img src="assets/previews/socialx-three-model-portrait-order-01.jpg" alt="人像模型顺序对照" width="420" loading="lazy" /></a>

作者自报 · foretyyt · [原始来源](https://x.com/foretyyt/status/2119894502588452933) · [详情与提示词状态](cases/socialx-three-model-portrait-order/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 原帖为多模型对比，部分图片来自其他模型，需按原帖标签区分。 作者标注图一为 Seedream 5.5，图二 Image 2.5，图三 Nano Banana 2.1。

#### [与 GPT Image 2.6 同要求对比](cases/socialx-gpt26-same-brief/README.zh-CN.md)

<a href="cases/socialx-gpt26-same-brief/README.zh-CN.md"><img src="assets/previews/socialx-gpt26-same-brief-01.jpg" alt="与 GPT Image 2.6 同要求对比" width="420" loading="lazy" /></a>

作者自报 · arito_si · [原始来源](https://x.com/arito_si/status/2119890337699364975) · [详情与提示词状态](cases/socialx-gpt26-same-brief/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 原帖为多模型对比，部分图片来自其他模型，需按原帖标签区分。 作者说明以相同提示词组测试 Seedream 5.5 与 GPT Image 2.6。

#### [蓝调时刻的渔夫](cases/socialx-blue-hour-fisherman/README.zh-CN.md)

<a href="cases/socialx-blue-hour-fisherman/README.zh-CN.md"><img src="assets/previews/socialx-blue-hour-fisherman-01.jpg" alt="蓝调时刻的渔夫" width="420" loading="lazy" /></a>

作者自报 · ahmetmertugrul · [原始来源](https://x.com/ahmetmertugrul/status/2119922071916757233) · [详情与提示词状态](cases/socialx-blue-hour-fisherman/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 冷色环境光与暖灯混合的纪实风格人像；原帖提供提示词。

<a id="interiors"></a>
### 室内与空间

#### [室内连续编辑](cases/official-interior-editing/README.zh-CN.md)

<a href="cases/official-interior-editing/README.zh-CN.md"><img src="assets/previews/official-interior-editing.jpg" alt="室内连续编辑" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-interior-editing/README.zh-CN.md)

<a id="typography"></a>
### 文字与排版

#### [透明艺术字与材质](cases/official-yarn-lettering/README.zh-CN.md)

<a href="cases/official-yarn-lettering/README.zh-CN.md"><img src="assets/previews/official-yarn-lettering.jpg" alt="透明艺术字与材质" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-yarn-lettering/README.zh-CN.md)

#### [莎士比亚报刊](cases/official-shakespeare-newspaper/README.zh-CN.md)

<a href="cases/official-shakespeare-newspaper/README.zh-CN.md"><img src="assets/previews/official-shakespeare-newspaper.jpg" alt="莎士比亚报刊" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/blog/more-realistic-images-more-stable-editing-across-100-rounds-introducing-seedream-5-5) · [详情与提示词状态](cases/official-shakespeare-newspaper/README.zh-CN.md)

#### [波兰语菜单](cases/quantslant-polish-menu/README.zh-CN.md)

<a href="cases/quantslant-polish-menu/README.zh-CN.md"><img src="assets/previews/quantslant-polish-menu.jpg" alt="波兰语菜单" width="420" loading="lazy" /></a>

作者自报 · Piotr Olszewski / QUANTSLANT · [原始来源](https://quantslant.com/seedream-5-5-features-pricing-benchmarks/) · [详情与提示词状态](cases/quantslant-polish-menu/README.zh-CN.md)

#### [波兰语全字母句](cases/quantslant-polish-pangram/README.zh-CN.md)

<a href="cases/quantslant-polish-pangram/README.zh-CN.md"><img src="assets/previews/quantslant-polish-pangram.jpg" alt="波兰语全字母句" width="420" loading="lazy" /></a>

作者自报 · Piotr Olszewski / QUANTSLANT · [原始来源](https://quantslant.com/seedream-5-5-features-pricing-benchmarks/) · [详情与提示词状态](cases/quantslant-polish-pangram/README.zh-CN.md)

#### [报纸文字错误样本](cases/quantslant-newspaper-errors/README.zh-CN.md)

<a href="cases/quantslant-newspaper-errors/README.zh-CN.md"><img src="assets/previews/quantslant-newspaper-errors.jpg" alt="报纸文字错误样本" width="420" loading="lazy" /></a>

作者自报 · Piotr Olszewski / QUANTSLANT · [原始来源](https://quantslant.com/seedream-5-5-features-pricing-benchmarks/) · [详情与提示词状态](cases/quantslant-newspaper-errors/README.zh-CN.md)

> 作者报告存在文字错误；保留为局限样本。

#### [杂志封面字形](cases/social-dheepan-magazine-cover/README.zh-CN.md)

<a href="cases/social-dheepan-magazine-cover/README.zh-CN.md"><img src="assets/previews/social-dheepan-magazine-cover.jpg" alt="杂志封面字形" width="420" loading="lazy" /></a>

作者自报 · Dheepanratnam · [原始来源](https://x.com/Dheepanratnam/status/2119767938173387065) · [详情与提示词状态](cases/social-dheepan-magazine-cover/README.zh-CN.md)

> 来自公开整理站的作者归因图片与提示词，未在本仓库独立复现。图像为缩小版，非原始导出。

#### [雨夜多语种招牌](cases/social-dheepan-rainy-storefront/README.zh-CN.md)

<a href="cases/social-dheepan-rainy-storefront/README.zh-CN.md"><img src="assets/previews/social-dheepan-rainy-storefront.jpg" alt="雨夜多语种招牌" width="420" loading="lazy" /></a>

作者自报 · Dheepanratnam · [原始来源](https://x.com/Dheepanratnam/status/2119767938173387065) · [详情与提示词状态](cases/social-dheepan-rainy-storefront/README.zh-CN.md)

> 来自公开整理站的作者归因图片与提示词，未在本仓库独立复现。图像为缩小版，非原始导出。

#### [护肤品包装小字](cases/social-dheepan-skincare-label/README.zh-CN.md)

<a href="cases/social-dheepan-skincare-label/README.zh-CN.md"><img src="assets/previews/social-dheepan-skincare-label.jpg" alt="护肤品包装小字" width="420" loading="lazy" /></a>

作者自报 · Dheepanratnam · [原始来源](https://x.com/Dheepanratnam/status/2119767938173387065) · [详情与提示词状态](cases/social-dheepan-skincare-label/README.zh-CN.md)

> 来自公开整理站的作者归因图片与提示词，未在本仓库独立复现。图像为缩小版，非原始导出。

#### [夜间电子乐活动海报](cases/social-dheepan-night-signal-poster/README.zh-CN.md)

<a href="cases/social-dheepan-night-signal-poster/README.zh-CN.md"><img src="assets/previews/social-dheepan-night-signal-poster.jpg" alt="夜间电子乐活动海报" width="420" loading="lazy" /></a>

作者自报 · Dheepanratnam · [原始来源](https://x.com/Dheepanratnam/status/2119767938173387065) · [详情与提示词状态](cases/social-dheepan-night-signal-poster/README.zh-CN.md)

> 来自公开整理站的作者归因图片与提示词，未在本仓库独立复现。图像为缩小版，非原始导出。

#### [跨版本密集文字对比](cases/socialx-dense-text-comparison/README.zh-CN.md)

<a href="cases/socialx-dense-text-comparison/README.zh-CN.md"><img src="assets/previews/socialx-dense-text-comparison-01.jpg" alt="跨版本密集文字对比" width="420" loading="lazy" /></a>

作者自报 · 94vanAI · [原始来源](https://x.com/94vanAI/status/2120007470898913320) · [详情与提示词状态](cases/socialx-dense-text-comparison/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 原帖为多模型对比，部分图片来自其他模型，需按原帖标签区分。 比较 Seedream 5.5、5.0 Pro 与 GPT Image 多个版本，请按原帖标注辨认结果。

#### [深海生物图鉴信息图](cases/socialx-deep-sea-field-guide/README.zh-CN.md)

<a href="cases/socialx-deep-sea-field-guide/README.zh-CN.md"><img src="assets/previews/socialx-deep-sea-field-guide-01.jpg" alt="深海生物图鉴信息图" width="420" loading="lazy" /></a>

作者自报 · ahmetmertugrul · [原始来源](https://x.com/ahmetmertugrul/status/2119915956365369596) · [详情与提示词状态](cases/socialx-deep-sea-field-guide/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 虚构生物图鉴页，组合标注、数据表和科学插图；原帖有提示词。

<a id="infographics"></a>
### 信息图与界面

#### [贪吃蛇界面](cases/official-snake-interface/README.zh-CN.md)

<a href="cases/official-snake-interface/README.zh-CN.md"><img src="assets/previews/official-snake-interface.jpg" alt="贪吃蛇界面" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-snake-interface/README.zh-CN.md)

#### [手表界面](cases/official-watch-interface/README.zh-CN.md)

<a href="cases/official-watch-interface/README.zh-CN.md"><img src="assets/previews/official-watch-interface.jpg" alt="手表界面" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-watch-interface/README.zh-CN.md)

#### [蝴蝶信息图](cases/official-butterfly-infographic/README.zh-CN.md)

<a href="cases/official-butterfly-infographic/README.zh-CN.md"><img src="assets/previews/official-butterfly-infographic.jpg" alt="蝴蝶信息图" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/blog/more-realistic-images-more-stable-editing-across-100-rounds-introducing-seedream-5-5) · [详情与提示词状态](cases/official-butterfly-infographic/README.zh-CN.md)

#### [咖啡信息图](cases/quantslant-coffee-infographic/README.zh-CN.md)

<a href="cases/quantslant-coffee-infographic/README.zh-CN.md"><img src="assets/previews/quantslant-coffee-infographic.jpg" alt="咖啡信息图" width="420" loading="lazy" /></a>

作者自报 · Piotr Olszewski / QUANTSLANT · [原始来源](https://quantslant.com/seedream-5-5-features-pricing-benchmarks/) · [详情与提示词状态](cases/quantslant-coffee-infographic/README.zh-CN.md)

<a id="characters"></a>
### 角色与贴纸

#### [奔跑角色](cases/official-running-character/README.zh-CN.md)

<a href="cases/official-running-character/README.zh-CN.md"><img src="assets/previews/official-running-character.jpg" alt="奔跑角色" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-running-character/README.zh-CN.md)

#### [贴纸组合](cases/official-sticker-sheets/README.zh-CN.md)

<a href="cases/official-sticker-sheets/README.zh-CN.md"><img src="assets/previews/official-sticker-sheets.jpg" alt="贴纸组合" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-sticker-sheets/README.zh-CN.md)

#### [毛绒角色](cases/official-plush-characters/README.zh-CN.md)

<a href="cases/official-plush-characters/README.zh-CN.md"><img src="assets/previews/official-plush-characters.jpg" alt="毛绒角色" width="420" loading="lazy" /></a>

官方展示 · ByteDance Seed · [原始来源](https://seed.bytedance.com/en/seedream5_5) · [详情与提示词状态](cases/official-plush-characters/README.zh-CN.md)

#### [角色设定表版本对比](cases/socialx-character-sheet-comparison/README.zh-CN.md)

<a href="cases/socialx-character-sheet-comparison/README.zh-CN.md"><img src="assets/previews/socialx-character-sheet-comparison-01.jpg" alt="角色设定表版本对比" width="420" loading="lazy" /></a>

作者自报 · EEJ_OOXO · [原始来源](https://x.com/EEJ_OOXO/status/2119780326117716281) · [详情与提示词状态](cases/socialx-character-sheet-comparison/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 原帖为多模型对比，部分图片来自其他模型，需按原帖标签区分。 与 Seedream 5.0 Pro 的角色设定表对比，原帖讨论分栏一致性和输出文件。

#### [角色真人化测试](cases/socialx-photoreal-conversion/README.zh-CN.md)

<a href="cases/socialx-photoreal-conversion/README.zh-CN.md"><img src="assets/previews/socialx-photoreal-conversion-01.jpg" alt="角色真人化测试" width="420" loading="lazy" /></a>

作者自报 · nanyuan0412 · [原始来源](https://x.com/nanyuan0412/status/2119949010698137603) · [详情与提示词状态](cases/socialx-photoreal-conversion/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 作者分享的双图角色真人化测试，明确标注 Seedream 5.5。

#### [角色重创作测试](cases/socialx-character-recreation/README.zh-CN.md)

<a href="cases/socialx-character-recreation/README.zh-CN.md"><img src="assets/previews/socialx-character-recreation-01.jpg" alt="角色重创作测试" width="420" loading="lazy" /></a>

作者自报 · haungpower · [原始来源](https://x.com/haungpower/status/2119852896544325859) · [详情与提示词状态](cases/socialx-character-recreation/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 作者标注为重创作的角色一致性测试，参考细节以原帖为准。

#### [Nature Unseen 概念系列](cases/socialx-nature-unseen/README.zh-CN.md)

<a href="cases/socialx-nature-unseen/README.zh-CN.md"><img src="assets/previews/socialx-nature-unseen-01.jpg" alt="Nature Unseen 概念系列" width="420" loading="lazy" /></a>

作者自报 · AI_Timemachine · [原始来源](https://x.com/AI_Timemachine/status/2119930302508286194) · [详情与提示词状态](cases/socialx-nature-unseen/README.zh-CN.md)

> 已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。 作者使用 Seedream 5.5 重做既有概念系列；四张组图只计一次。

<a id="recipes"></a>
## 原创练习提示词

以下配方由本仓库编写，尚未用 Seedream 5.5 执行。它们不对应上方样张的原始输入。每份包含中英文指令和验收项。

| 配方 | 状态 |
| --- | --- |
| [单一区域编辑](templates/targeted-edit.md) | 原创，未执行 |
| [三轮连续编辑](templates/edit-chain.md) | 原创，未执行 |
| [独立透明素材](templates/transparent-asset.md) | 原创，未执行 |
| [半透明材质测试](templates/material-transparency.md) | 原创，未执行 |
| [自然纪实摄影](templates/documentary-photo.md) | 原创，未执行 |
| [固定文案海报](templates/copy-locked-poster.md) | 原创，未执行 |
| [角色一致性设定](templates/character-sheet.md) | 原创，未执行 |
| [步骤信息图](templates/instruction-infographic.md) | 原创，未执行 |

<a id="social"></a>
## 社媒原始素材

通过 X 官方公开嵌入接口与公开 syndication 响应核对账号、版本和媒体地址。保留原帖及原图/视频链接，不复制帖文全文。

### ByteDance Seed · @ByteDanceSeed_

[![ByteDance Seed](assets/previews/social-2119717948470546446.jpg)](https://x.com/ByteDanceSeed_/status/2119717948470546446)

[原始帖子](https://x.com/ByteDanceSeed_/status/2119717948470546446) · [原始媒体](https://video.twimg.com/amplify_video/2119716100359548928/vid/avc1/1920x1080/yijLvq8WlsqxbemL.mp4)

### Dreamina AI · @dreamina_ai

[![Dreamina AI](assets/previews/social-2119751497282125949.jpg)](https://x.com/dreamina_ai/status/2119751497282125949)

[原始帖子](https://x.com/dreamina_ai/status/2119751497282125949) · [原始媒体](https://pbs.twimg.com/media/HWredl_bAAAkfEk.jpg)

[补充社媒研究（含待核实线索）](docs/SOCIAL-CASES-2026-11-10.md)

[新增 5 个创作者社媒案例（原始媒体待补）](docs/SOCIAL-SHOWCASE-2026-11-10-BATCH2.md)

## 本地维护

```bash
python3 scripts/build.py
python3 scripts/validate.py
python3 scripts/search.py RGBA
```

可选：`python3 scripts/check_media.py` 检查本地预览，需安装 ffmpeg；`python3 scripts/refresh_previews.py` 联网刷新缩放代表帧预览，不打包原始媒体。

## 贡献与许可

按[投稿说明](CONTRIBUTING.md)提供原帖、明确版本证据和提示词状态。版权问题请[提交问题](https://github.com/RaphaelAI-OpenLab/awesome-seedream-5-5/issues/new?template=report-problem.yml)。

代码与原创文档适用 [MIT](LICENSE)；第三方提示词与媒体保留各自权利。README 组织方式参考 [GPT Image 2.6 仓库](https://github.com/RaphaelAI-OpenLab/awesome-gpt-image-2-6)，署名见 [ATTRIBUTION](docs/ATTRIBUTION.md)。
