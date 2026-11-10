#!/usr/bin/env python3
"""循环读取有大小上限的源文件，生成 640px 代表帧预览。"""
import argparse
import concurrent.futures
import json
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gif-only', action='store_true', help='只刷新 GIF 代表帧，保留已检查的静态预览')
    args = parser.parse_args()
    cases = json.loads((ROOT / 'content/cases.json').read_text())
    social = json.loads((ROOT / 'content/social.json').read_text())
    jobs = [(c['id'], c['media'][0]['url']) for c in cases]
    jobs += [('social-' + s['id'], s['poster_url']) for s in social if s['duplicate_of'] is None]
    preview_dir = ROOT / 'assets/previews'
    preview_dir.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='seedream-preview-') as temp:
        def make(job):
            ident, url = job
            animated = urlparse(url).path.endswith('.gif')
            if args.gif_only and not animated:
                return
            limit = 256 * 1024 * 1024
            source = Path(temp) / (ident + Path(urlparse(url).path).suffix)
            request = urllib.request.Request(url, headers={'User-Agent': 'Awesome-Seedream-Preview/1.0'})
            for attempt in range(3):
                with urllib.request.urlopen(request, timeout=45) as response, source.open('wb') as output:
                    declared = int(response.headers.get('Content-Length', 0))
                    if declared > limit:
                        raise ValueError(ident + ': 源文件超过 256 MiB 上限')
                    length = 0
                    while length <= limit:
                        chunk = response.read(min(64 * 1024, limit + 1 - length))
                        if not chunk:
                            break
                        output.write(chunk)
                        length += len(chunk)
                if length <= limit and (not declared or length == declared):
                    break
                if attempt == 2:
                    raise ValueError(f'{ident}: 下载长度 {length} 与预期 {declared} 不一致')
            timestamp = 0.0
            if animated:
                probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(source)], check=True, capture_output=True, text=True, timeout=60)
                timestamp = float(json.loads(probe.stdout)['format']['duration']) * 0.75
            target = preview_dir / (ident + '.jpg')
            candidate = Path(temp) / (ident + '.preview.jpg')
            command = ['ffmpeg', '-v', 'error', '-threads', '1', '-i', str(source)]
            if animated:
                command += ['-ss', str(timestamp)]
            command += ['-frames:v', '1', '-vf', 'scale=640:640:force_original_aspect_ratio=decrease:force_divisible_by=2,format=yuvj420p', '-q:v', '3', '-threads', '1', '-y', str(candidate)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
            if result.returncode or not candidate.exists() or not candidate.stat().st_size:
                raise RuntimeError(ident + ': ' + result.stderr[-800:])
            candidate.replace(target)
            print(f'{ident}: {target.stat().st_size} bytes; sample={timestamp:.2f}s', flush=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            list(executor.map(make, jobs))
    for case in cases:
        media = case['media'][0]
        media['preview'] = f'assets/previews/{case["id"]}.jpg'
        media['preview_transform'] = 'gif-at-75pct-duration-or-static-image-resized-to-fit-640px-jpeg'
        media['delivery'] = 'local-preview-with-source-link'
    for post in social:
        ident = post['duplicate_of'] or post['id']
        post['preview'] = f'assets/previews/social-{ident}.jpg'
    (ROOT / 'content/cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'content/social.json').write_text(json.dumps(social, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
