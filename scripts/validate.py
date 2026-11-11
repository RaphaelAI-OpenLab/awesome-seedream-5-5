#!/usr/bin/env python3
"""验证来源边界、双语生成一致性、仓库内部链接与基础安全。"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse
from build import ROOT, outputs


def require(condition, message):
    if not condition:
        raise ValueError(message)


def https(value):
    parsed = urlparse(value)
    return parsed.scheme == 'https' and bool(parsed.hostname) and not parsed.username and not parsed.password


def validate():
    read = lambda name: json.loads((ROOT / 'content' / (name + '.json')).read_text())
    cases, cats, recipes, social = (read(n) for n in ['cases', 'categories', 'recipes', 'social'])
    ids = [c['id'] for c in cases]
    require(len(ids) == len(set(ids)), '案例 ID 重复')
    require(len({c['id'] for c in cats}) == len(cats), '分类 ID 重复')
    categories = {c['id'] for c in cats}
    seen_media = set()
    for c in cases:
        require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', c['id']), '案例 ID 不安全')
        require(c['category'] in categories, f'{c["id"]}: 分类不存在')
        require(c['model'] == 'Seedream 5.5', f'{c["id"]}: 模型版本不匹配')
        require(c['source_type'] in {'official', 'creator-reported'}, '来源状态无效')
        require(c['reproduced'] is False, '独立复现状态需提供新证据后扩展校验器')
        require(c['model_evidence'] and c['author'], '缺少版本证据或作者')
        require(https(c['source_url']), '来源必须是无凭据的 HTTPS 地址')
        require(re.fullmatch(r'\d{4}-\d{2}-\d{2}', c['checked_at']), '核对日期无效')
        require(all(c['title'].get(lang) for lang in ['en', 'zh-CN']), '缺少双语标题')
        p = c['prompt']
        require(p['status'] in {'original', 'source-linked', 'not-published'}, '提示词状态无效')
        require(https(p['url']), '提示词缺少来源')
        require(bool(p['text']) == (p['status'] == 'original'), '原始提示词状态与正文矛盾')
        require(bool(c['media']), '案例无媒体')
        if c.get('animation_preview'):
            anim = c['animation_preview']
            require(re.fullmatch(r'assets/animations/[a-z0-9-]+\.gif', anim) is not None,
                    '动画预览路径无效')
            require((ROOT / anim).is_file() and 1000 < (ROOT / anim).stat().st_size < 3 * 1024 * 1024,
                    '动图预览缺失或超限')
            require((ROOT / anim).read_bytes()[:6] in (b'GIF87a', b'GIF89a'), '动图格式不正确')
        for m in c['media']:
            require(https(m['url']), '媒体地址无效')
            require(m['delivery'] == 'local-preview-with-source-link' and m['rights'] == 'rights-reserved', '媒体许可状态不正确')
            require(re.fullmatch(r'assets/previews/[a-z0-9-]+\.(?:jpg|webp)', m['preview']), '预览路径无效')
            require((ROOT / m['preview']).is_file(), '预览文件不存在')
            require(m['type'] in {'image', 'gif', 'video'}, '不支持的案例媒体类型')
            require(m['url'] not in seen_media, '同一媒体重复计数')
            seen_media.add(m['url'])
    require(len({r['id'] for r in recipes}) == len(recipes), '练习配方 ID 重复')
    for r in recipes:
        require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', r['id']), '配方 ID 不安全')
        require(all(r['prompt'].get(lang) and r['title'].get(lang) for lang in ['en', 'zh-CN']), '配方缺少双语内容')
        require(1 <= len(r['checks']) <= 5, '配方验收项数量无效')
    social_ids = {s['id'] for s in social}
    require(len(social_ids) == len(social), '社媒 ID 重复')
    for s in social:
        require(s['status'] == 'source-verified' and s['counted_as_case'] is False, '社媒状态不正确')
        require(s['duplicate_of'] is None or s['duplicate_of'] in social_ids, '重复关系不存在')
        require(all(https(s[k]) for k in ['url', 'media_url', 'poster_url']), '社媒地址无效')
        require(re.fullmatch(r'assets/previews/social-[0-9]+\.jpg', s['preview']), '社媒预览路径无效')
        require((ROOT / s['preview']).is_file(), '社媒预览不存在')
    import hashlib
    report = json.loads((ROOT / 'docs/media-check.json').read_text())
    preview_paths = {m['preview'] for c in cases for m in c['media']} | {s['preview'] for s in social}
    require({item['preview'] for item in report['items']} == preview_paths, '媒体检查未覆盖全部预览')
    for item in report['items']:
        require(item['status'] == 'decoded-preview', '预览解码未通过')
        require(item['preview'] in preview_paths, '媒体报告包含未知路径')
        raw = (ROOT / item['preview']).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == item['sha256'], '预览与核验哈希不一致')
        require(len(raw) == item['bytes'] and len(raw) < 512 * 1024, '预览文件大小不正确')
        if item['preview'].endswith('.webp'):
            require(raw[:4] == b'RIFF' and raw[8:12] == b'WEBP', 'WebP 文件签名不正确')
    external_cases = json.loads((ROOT / 'external-references/cases.json').read_text())['cases']
    for filename in ['README.md', 'README.zh-CN.md']:
        readme = (ROOT / filename).read_text()
        first = readme.index('<a id="with-prompts"></a>')
        second = readme.index('<a id="without-prompts"></a>')
        require(first < second, 'README 未按完整 Prompt 优先排序')
        for c, is_external in [(c, False) for c in cases] + [(c, True) for c in external_cases]:
            marker = f'<a id="{c["id"]}"></a>'
            require(readme.count(marker) == 1, f'{filename}: 案例缺失或重复：{c["id"]}')
            has_prompt = bool(c['prompt'].get('text')) and (is_external or c['prompt']['status'] == 'original')
            pos = readme.index(marker)
            require((first < pos < second) if has_prompt else (pos > second),
                    f'{filename}: Prompt 排序错误：{c["id"]}')
            if has_prompt:
                require(c['prompt']['text'] in readme, f'{filename}: 未展示 Prompt：{c["id"]}')
            for m in c['media']:
                if m.get('preview'):
                    src = ('external-references/' if is_external else '') + m['preview']
                    require(f'src="{src}"' in readme, f'{filename}: 未展示本地图片：{src}')
    for path, content in outputs().items():
        require(path.exists() and path.read_text() == content, f'生成结果过期: {path.relative_to(ROOT)}')
    expected_pages = {ROOT / 'cases' / c['id'] / filename for c in cases for filename in ['README.md', 'README.zh-CN.md']}
    require(set((ROOT / 'cases').rglob('*.md')) == expected_pages, '案例详情页缺失或含过期文件')
    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        text = path.read_text()
        targets = re.findall(r'\]\(([^\s)]+)\)', text) + re.findall(r'(?:href|src)="([^"<>]+)"', text)
        for target in targets:
            if urlparse(target).scheme or target.startswith('#'):
                continue
            dest = (path.parent / unquote(target.split('#')[0])).resolve()
            require(dest.is_relative_to(ROOT), f'链接超出仓库: {path.relative_to(ROOT)}: {target}')
            require(dest.exists(), f'内部链接失效: {path.relative_to(ROOT)}: {target}')
        require('sandbox:/' not in text and '/Users/' not in text, f'意外本地路径: {path}')
    secret_patterns = [r'gh[pousr]_[A-Za-z0-9]{20,}', r'github_pat_[A-Za-z0-9_]{20,}', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
    for folder in ['content', 'docs', 'templates', 'assets', '.github']:
        for path in (ROOT / folder).rglob('*'):
            if path.is_file() and path.suffix in {'.json', '.md', '.yml', '.svg'}:
                text = path.read_text()
                require(not any(re.search(pattern, text) for pattern in secret_patterns), f'疑似凭据: {path.relative_to(ROOT)}')
    print(f'校验通过：{len(cases)} 个案例、{len(expected_pages)} 个双语详情页、{len(recipes)} 份练习配方、{len(social)} 条社媒来源')


if __name__ == '__main__':
    try:
        validate()
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f'校验失败：{exc}', file=sys.stderr)
        raise SystemExit(1)
