#!/usr/bin/env python3
"""从结构化数据生成双语 README 与案例详情页；不联网。"""
import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'site.config.json').read_text())
REPO = 'https://github.com/' + CONFIG['repository']


def data(name):
    return json.loads((ROOT / 'content' / (name + '.json')).read_text())


def file_for(lang):
    return 'README.zh-CN.md' if lang == 'zh-CN' else 'README.md'


def render(lang):
    zh = lang == 'zh-CN'
    cases, categories, social, recipes = (data(n) for n in ['cases', 'categories', 'social', 'recipes'])
    unique_social = sum(s['duplicate_of'] is None for s in social)
    choose = lambda cn, en: cn if zh else en
    title = choose('Seedream 5.5 提示词与案例合集', 'Awesome Seedream 5.5')
    lines = [
        '<!-- 由 scripts/build.py 生成，请编辑 content/ 内的数据。 -->', '',
        f'[![{title}](assets/header.svg)]({CONFIG["brand_url"]})', '', f'# {title}', '',
        f'[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) '
        f'[![Stars](https://img.shields.io/github/stars/{CONFIG["repository"]}?style=social)]({REPO}) '
        f'[![Validate]({REPO}/actions/workflows/validate.yml/badge.svg)]({REPO}/actions/workflows/validate.yml) '
        f'[![MIT](https://img.shields.io/badge/code-MIT-lightgrey)](LICENSE)', '',
        '[English](README.md) · [简体中文](README.zh-CN.md)', '',
        choose('由 Raphael 整理的图片与编辑案例库。官方展示、作者自报结果与本仓库编写的练习提示词分别标记。',
               'A visual reference collection by Raphael. Official demos, creator-reported outputs and original practice recipes are labeled separately.'), '',
        choose(f'**{len(cases)} 个来源案例 · {len(categories)} 个分类 · {len(recipes)} 份原创练习配方 · {len(social)} 条独立追踪的发布帖（{unique_social} 份不同媒体）**',
               f'**{len(cases)} sourced cases · {len(categories)} categories · {len(recipes)} original practice recipes · {len(social)} separately tracked launch posts ({unique_social} distinct media items)**'), '',
        choose('案例未由本仓库独立复现。仓库只保存缩放后的单帧预览，完整图片、GIF 与视频链接至原始地址；第三方媒体及其预览的版权归原权利人。',
               'Cases have not been independently reproduced here. Only reduced single-frame previews are bundled; full images, GIFs and videos are linked at their origins. Third-party media and previews retain their owners’ rights.'), '',
        choose('[浏览案例](#cases) · [练习提示词](#recipes) · [社媒原帖](#social) · [投稿](CONTRIBUTING.md) · [来源与核验](docs/SOURCES.md)',
               '[Browse cases](#cases) · [Practice recipes](#recipes) · [Social sources](#social) · [Contribute](CONTRIBUTING.md) · [Source audit](docs/SOURCES.md)'), '',
        '## ' + choose('模型与入口', 'Model & access'), '',
        choose('Seedream 5.5 的官方发布日期为 **2026-11-09**。能力和入口以[官方模型页](https://seed.bytedance.com/en/seedream5_5)与[中文发布说明](https://seed.bytedance.com/zh/blog/more-realistic-images-more-stable-editing-across-100-rounds-introducing-seedream-5-5)为准。',
               'Seedream 5.5 was announced on **2026-11-09**. See the [official model page](https://seed.bytedance.com/en/seedream5_5) and [release announcement](https://seed.bytedance.com/en/blog/more-realistic-images-more-stable-editing-across-100-rounds-introducing-seedream-5-5) for capabilities and rollout.'), '',
        choose(f'[访问 Raphael]({CONFIG["brand_url"]})。这是品牌主页链接；本仓库尚未核实 Raphael 是否提供 Seedream 5.5，也不提供模型 API 或权重。',
               f'[Visit Raphael]({CONFIG["brand_url"]}). This is a brand homepage link. Seedream 5.5 availability on Raphael has not been verified; this collection supplies neither a model API nor weights.'), '',
        '## ' + choose('收录口径', 'Collection status'), '',
        '| ' + choose('项目 | 数量 |', 'Item | Count |'), '| --- | ---: |',
        f'| {choose("官方来源案例", "Official-source cases")} | {sum(c["source_type"] == "official" for c in cases)} |',
        f'| {choose("作者自报案例", "Creator-reported cases")} | {sum(c["source_type"] == "creator-reported" for c in cases)} |',
        f'| {choose("仓库内完整原始提示词", "Complete original source prompts included")} | {sum(c["prompt"]["status"] == "original" for c in cases)} |',
        f'| {choose("独立复现案例", "Independently reproduced cases")} | 0 |',
        f'| {choose("来源核对日期", "Sources checked")} | {max(c["checked_at"] for c in cases)} |', '',
        choose('同一案例的多轮图片不重复计数；重复社媒视频不增加案例总数。来源页中的展示说明不等于实际完整生成提示词。',
               'Edit rounds are grouped as one case. Duplicate social videos do not increase the case count. Source-page demo descriptions are not treated as complete generation prompts.'), '',
        '<a id="categories"></a>', '## ' + choose('按分类浏览', 'Browse by category'), '',
        '| ' + choose('分类 | 案例数 |', 'Category | Cases |'), '| --- | ---: |'
    ]
    for cat in categories:
        lines.append(f'| [{cat["label"][lang]}](#{cat["id"]}) | {sum(c["category"] == cat["id"] for c in cases)} |')
    lines += ['', '<a id="cases"></a>', '## ' + choose('全部案例', 'All cases'), '']
    pages = {}
    for cat in categories:
        lines += [f'<a id="{cat["id"]}"></a>', f'### {cat["label"][lang]}', '']
        group = [c for c in cases if c['category'] == cat['id']]
        for c in group:
            name, media = c['title'][lang], c['media'][0]
            page = f'cases/{c["id"]}/{file_for(lang)}'
            status = choose('官方展示', 'Official demo') if c['source_type'] == 'official' else choose('作者自报', 'Creator-reported')
            image = f'<a href="{page}"><img src="{c.get("animation_preview", media["preview"])}" alt="{html.escape(name, quote=True)}" width="420" loading="lazy" /></a>'
            lines += [f'#### [{name}]({page})', '', image, '',
                      f'{status} · {c["author"]} · [{choose("原始来源", "Source")}]({c["source_url"]}) · [{choose("详情与提示词状态", "Details & prompt status")}]({page})', '']
            if c.get('caveat'):
                lines += ['> ' + c['caveat'][lang], '']
            prompt = c['prompt']
            detail = [f'# {name}', '', '[English](README.md) · [简体中文](README.zh-CN.md)', '',
                      f'[{choose("返回案例目录", "Back to cases")}](../../{file_for(lang)}#cases)', '',
                      f'**{status} · {choose("未独立复现", "Not independently reproduced")}**', '',
                      f'![{name}](../../{media["preview"]})', '',
                      (choose('以上为缩放后的代表帧预览，不是完整动画或可用的透明素材导出文件。', 'This is a reduced representative-frame preview, not a complete animation or an exported transparent asset.') if not media['preview'].endswith('.webp') else choose('这是来源注明出处的公开案例汇编的 WebP 预览，并非原始媒体或透明素材导出。', 'This is a WebP preview from an attributed public gallery, not original media or an exported transparent asset.')), '',
                      f'[{choose("打开原始媒体", "Open original media") if not media["preview"].endswith(".webp") else choose("打开汇编预览", "Open gallery preview")}]({media["url"]})', '',
                      '## ' + choose('提示词', 'Prompt'), '']
            if c.get('animation_preview'):
                detail[-2:-2] = [
                    '', '## ' + choose('原帖视频的短动图预览', 'Animated excerpt from X video'), '',
                    f'![{name} — animated preview](../../{c["animation_preview"]})', '',
                    choose('这是原帖视频生成的低分辨率短动图预览，并非模型原生输出 GIF；完整视频请打开原始媒体。',
                           'Low-resolution excerpt of the source post video, not a native Seedream GIF. Open original media for the full video.'), ''
                ]
            if len(c['media']) > 1:
                gallery = ['', '## ' + choose('同一原帖的更多图片', 'More photos from the original post'), '']
                for number, frame in enumerate(c['media'][1:], 2):
                    gallery += [f'**{choose("配图", "Image")} {number}**', '',
                                f'![{name} - {number}](../../{frame["preview"]})', '',
                                f'[{choose("原媒体", "Source media") if not frame["preview"].endswith(".webp") else choose("汇编预览", "Gallery preview")}]({frame["url"]})', '']
                detail[-2:-2] = gallery
            if prompt['status'] == 'original':
                detail += ['```text', prompt['text'], '```', '',
                           choose('以上为来源公开、归因于作者的提示词；本站未独立复现，请对照原作者帖文确认二次转录。', 'The prompt is attributed to the creator by the source curator; no independent reproduction was performed.'), '']
            elif prompt['status'] == 'source-linked':
                detail += [choose('提示词或展示说明位于原始来源；本页不复制全文，不把展示说明标为实际完整输入。', 'Prompt text or demo descriptions are available at the source. The full text is not copied here; demo descriptions are not presented as complete model inputs.'), '']
            else:
                detail += [choose('该来源没有公开本案例的完整输入提示词；本仓库不补写为原始提示词。', 'The source does not publish a complete input prompt for this example. No reconstructed text is labeled as the original prompt.'), '']
            detail += [f'[{choose("查看提示词来源", "View prompt source")}]({prompt["url"]})', '',
                       '## ' + choose('出处与边界', 'Attribution & limits'), '',
                       f'- {choose("作者", "Author")}: {c["author"]}',
                       f'- {choose("模型来源归因", "Source model attribution")}: Seedream 5.5',
                       f'- {choose("核对日期", "Checked")}: {c["checked_at"]}',
                       f'- [{choose("来源页面", "Source page")}]({c["source_url"]})', '',
                       (choose('原始媒体通过来源地址提供；仓库只保存经缩放的 JPEG 代表帧预览。原权利人保留权利；MIT 许可不覆盖这些媒体、预览与原始提示词。GIF 是展示序列，不代表模型原生生成动画；JPEG 预览不含 Alpha 通道。',
                              'Original media is linked at its source. Only reduced representative-frame JPEG previews are bundled. Owners retain their rights; MIT does not cover this media, previews or source prompts. Demo GIFs do not establish native animation generation; JPEG previews have no alpha channel.') if not media['preview'].endswith('.webp') else choose('原帖在上方链接。WebP 来自注明出处的公开第三方汇编，不代表有转载许可、拿到原始附件或独立复现。媒体、预览、提示词版权仍属原作者，MIT 许可不覆盖。', 'Original post is linked above. This WebP comes from an attributed public third-party gallery: no redistribution license, raw-media status, or model reproduction is implied. Owners retain rights to images, previews and prompts; MIT does not cover them.')), '']
            if c.get('caveat'):
                detail += ['> ' + c['caveat'][lang], '']
            pages[ROOT / page] = '\n'.join(detail)
    lines += ['<a id="recipes"></a>', '## ' + choose('原创练习提示词', 'Original practice recipes'), '',
              choose('以下配方由本仓库编写，尚未用 Seedream 5.5 执行。它们不对应上方样张的原始输入。每份包含中英文指令和验收项。',
                     'These recipes were written for this collection and have not been executed with Seedream 5.5. They are not the original inputs for the sourced images. Each includes Chinese/English instructions and acceptance checks.'), '']
    lines += ['| ' + choose('配方 | 状态 |', 'Recipe | Status |'), '| --- | --- |']
    for recipe in recipes:
        lines.append(f'| [{recipe["title"][lang]}](templates/{recipe["id"]}.md) | {choose("原创，未执行", "Original, not executed")} |')
    lines += ['', '<a id="social"></a>', '## ' + choose('社媒原始素材', 'Original social sources'), '',
              choose('通过 X 官方公开嵌入接口与公开 syndication 响应核对账号、版本和媒体地址。保留原帖及原图/视频链接，不复制帖文全文。',
                     'Account, model version and media URLs were checked through X public oEmbed and syndication responses. Original posts and media are linked without copying full post text.'), '']
    for s in social:
        if s['duplicate_of']:
            continue
        lines += [f'### {s["author"]} · @{s["handle"]}', '',
                  f'[![{s["author"]}]({s["preview"]})]({s["url"]})', '',
                  f'[{choose("原始帖子", "Original post")}]({s["url"]}) · [{choose("原始媒体", "Original media")}]({s["media_url"]})', '']
    lines += [choose('[补充社媒研究（含待核实线索）](docs/SOCIAL-CASES-2026-11-10.md)', '[Additional social research (including pending leads)](docs/SOCIAL-CASES-2026-11-10.md)'), '']
    lines += [choose('[新增 5 个创作者社媒案例（原始媒体待补）](docs/SOCIAL-SHOWCASE-2026-11-10-BATCH2.md)', '[New creator showcase: five social examples (source media pending)](docs/SOCIAL-SHOWCASE-2026-11-10-BATCH2.md)'), '']
    lines += ['## ' + choose('本地维护', 'Local maintenance'), '',
              '```bash', 'python3 scripts/build.py', 'python3 scripts/validate.py', 'python3 scripts/search.py RGBA', '```', '',
              choose('可选：`python3 scripts/check_media.py` 检查本地预览，需安装 ffmpeg；`python3 scripts/refresh_previews.py` 联网刷新缩放代表帧预览，不打包原始媒体。',
                     'Optional: `python3 scripts/check_media.py` checks local previews and requires ffmpeg. `python3 scripts/refresh_previews.py` refreshes reduced representative-frame previews over the network without bundling original media.'), '',
              '## ' + choose('贡献与许可', 'Contributing & licensing'), '',
              choose('按[投稿说明](CONTRIBUTING.md)提供原帖、明确版本证据和提示词状态。版权问题请[提交问题](https://github.com/RaphaelAI-OpenLab/awesome-seedream-5-5/issues/new?template=report-problem.yml)。',
                     'Follow the [contribution guide](CONTRIBUTING.md) with the original post, explicit version evidence and prompt status. Report rights issues through the [issue form](https://github.com/RaphaelAI-OpenLab/awesome-seedream-5-5/issues/new?template=report-problem.yml).'), '',
              choose('代码与原创文档适用 [MIT](LICENSE)；第三方提示词与媒体保留各自权利。README 组织方式参考 [GPT Image 2.6 仓库](https://github.com/RaphaelAI-OpenLab/awesome-gpt-image-2-6)，署名见 [ATTRIBUTION](docs/ATTRIBUTION.md)。',
                     'Code and original documentation use [MIT](LICENSE). Third-party prompts and media retain their own rights. Layout follows the [GPT Image 2.6 collection](https://github.com/RaphaelAI-OpenLab/awesome-gpt-image-2-6); see [attribution](docs/ATTRIBUTION.md).'), '']
    pages[ROOT / file_for(lang)] = '\n'.join(lines)
    return pages


def outputs():
    result = {}
    for lang in CONFIG['languages']:
        result.update(render(lang))
    for recipe in data('recipes'):
        lines = [f'# {recipe["title"]["zh-CN"]} / {recipe["title"]["en"]}', '',
                 '**本仓库原创练习配方 · 未执行 · 不对应来源样张的原始输入**', '',
                 '## 中文指令', '', '```text', recipe['prompt']['zh-CN'], '```', '',
                 '## English prompt', '', '```text', recipe['prompt']['en'], '```', '',
                 '## 验收项', '']
        lines += [f'{i}. {v}' for i, v in enumerate(recipe['checks'], 1)]
        lines += ['', '如服务没有对应模型或输出开关，不以提示词文字代替服务能力。生成结果需要人工检查。', '']
        result[ROOT / 'templates' / (recipe['id'] + '.md')] = '\n'.join(lines)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = outputs()
    changed = [p for p, text in expected.items() if not p.exists() or p.read_text() != text]
    if args.check:
        if changed:
            raise SystemExit('生成内容过期: ' + ', '.join(str(p.relative_to(ROOT)) for p in changed))
        print(f'生成一致性通过：{len(expected)} 个文件')
        return
    for path, text in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    print(f'已生成 {len(expected)} 个文件')


if __name__ == '__main__':
    main()
