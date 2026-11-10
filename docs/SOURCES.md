# 来源与核验记录

核对日期：2026-11-10。首版包含 28 个案例：20 个官方来源案例、8 个作者自报案例；社媒记录独立于案例计数。

## 官方来源

1. [Seedream 5.5 模型页](https://seed.bytedance.com/en/seedream5_5)：18 个不同演示，包括 13 个 GIF 和 5 张静态图。按页面图片 DOM 与同组说明关联，完整媒体地址见 `content/cases.json`。
2. [官方发布说明](https://seed.bytedance.com/en/blog/more-realistic-images-more-stable-editing-across-100-rounds-introducing-seedream-5-5)：补充莎士比亚报刊与蝴蝶信息图两个案例；同一画面不重复计数。

官方材料说明的模型发布日期为 2026-11-09。性能陈述属于官方自报，不构成本仓库实测。GIF 为官方展示序列，不代表原生视频或动画输出。透明素材演示的 GIF 不用于证明预览文件自身有真实 Alpha 通道。

## 创作者来源

[Piotr Olszewski / QUANTSLANT 的原始实测文章](https://quantslant.com/seedream-5-5-features-pricing-benchmarks/)明确将收录的八张图标为 Seedream 5.5；按该文章的图片、图注和版本标记逐一关联。只收录 `/2026/11/sd55/` 中的八个案例，没有混入同一文章中的旧模型对照图。

保留报纸文字错误与雨衣角色的半透明局限示例，避免只展示成功结果。作者的准确率、耗时、价格与像素变化数据没有作为本仓库的测量结果引用。完整原始指令仅收录纸条局部编辑一例；其余提示词或展示说明链接至来源。

## 社媒来源

| 原帖 | 核对方式 | 去重 |
| --- | --- | --- |
| [ByteDance Seed 发布帖](https://x.com/ByteDanceSeed_/status/2119717948470546446) | X 官方 oEmbed 与公开 syndication 响应 | 一份视频 |
| [Dreamina AI 发布帖](https://x.com/dreamina_ai/status/2119751497282125949) | 同上 | 一张图片 |
| [ByteDance Seed 另一发布帖](https://x.com/ByteDanceSeed_/status/2119720475068920181) | 同上 | 视频地址与第一帖相同，不重复计数 |

公开读取端点示例：

```text
https://publish.twitter.com/oembed?url=https://x.com/ByteDanceSeed_/status/2119717948470546446&omit_script=true
https://cdn.syndication.twimg.com/tweet-result?id=2119717948470546446&lang=en&token=0
```

本次直接读取 X 网页时返回 403，核对使用上述公开接口。数据保留作者、发布日期、原帖地址、原媒体地址与重复关系，不归档整段帖文，不记录用户凭据或登录态。社媒宣传中的准确率等陈述未作为独立验证事实。

## 发布边界

1. 原对话提供的 `awesome-seedream-5-5.zip` 下载入口未能触发下载，也没有返回可用文件地址；本仓库根据当前可访问的原始来源独立重建，不能声称与原 ZIP 内容逐字相同。
2. README 与案例页使用 640px 范围内的 JPEG 代表帧预览（GIF 选取时长 75% 处），并保留原始媒体链接。预览经过抽帧、缩放与 JPEG 压缩，不是原始输出文件，不保留动画或 Alpha。第三方原始文件没有打包发布。
3. `docs/media-check.json` 记录本地预览的哈希与解码结果；`docs/source-media-check.json` 保留首轮原始媒体检查结果。首轮下载的父婴样本未通过解码，已排除此例，补入作者明确标记版本的黄昏火车站案例。之后定位到单次读取可能截断响应，预览刷新已改为循环读取并校验长度；三个 RGBA GIF 超过首轮的 100 MiB 上限；最终预览使用完整下载的临时源文件（上限 256 MiB），在时长 75% 处抽帧。预览解码通过不等于完整动画视觉验收。
4. 本仓库没有运行付费生图、独立复现、模型 API 接入或人工视觉验收。

## 首版生成与维护

`content/` 是维护入口；构建与离线校验仅使用 Python 3.11+ 标准库。预览刷新使用网络与 ffmpeg，本地预览解码检查使用 ffmpeg。没有部署独立网站；案例通过 GitHub README 与仓库内详情页浏览，离线检索使用 `scripts/search.py`。

## 2026-11-10 社媒研究补充批次

新增 [8 条社媒研究场景索引](SOCIAL-CASES-2026-11-10.md) 与 [JSON 元数据](../content/social-research-2026-11-10.json)。证据等级、找不到单帖的情形、与官方演示可能重复的内容已经标注。**这些线索不计入主 README 的已验证案例或社媒数量**，不托管第三方原始素材。

## 第二批新增创作者社媒案例（2026-11-10）

[五个源帖关联的新案例和排重备注](SOCIAL-SHOWCASE-2026-11-10-BATCH2.md)与 [JSON 元数据](../content/social-discoveries-batch02.json)。本批仅有社媒镜像/聚合页面级别的作者自述证据，准确单帖 ID、原媒体直接地址和完整提示词仍有缺口；不将其加入 `content/cases.json` 或 `content/social.json` 的严格计数，不上传其他人的图片冒充作者输出。

## 第三批社媒 Prompt 与图片（2026-11-10）

来源为 BeatAPI 的公开整理项目，其中关联了原 X 作者、完整 prompt 及镜像图片。本仓库实际保存了裁缩至640px内的 JPEG 预览，保留原帖与媒体链接。无法证明是原始未压缩文件或原生透明图，也不声称原作者授权转让版权。详情见 content/social-image-batch03.json 和 docs/social-image-batch03-audit.json。
