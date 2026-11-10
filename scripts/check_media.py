#!/usr/bin/env python3
"""检查仓库内预览的哈希与解码；不等于原始媒体完整解码或模型复现。"""
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    if not shutil.which('ffprobe') or not shutil.which('ffmpeg'):
        raise SystemExit('需先安装 ffmpeg；日常离线校验不依赖此命令。')
    cases = json.loads((ROOT / 'content/cases.json').read_text())
    social = json.loads((ROOT / 'content/social.json').read_text())
    paths = {m['preview'] for c in cases for m in c['media']} | {s['preview'] for s in social}
    results = []
    for relative in sorted(paths):
        path = ROOT / relative
        raw = path.read_bytes()
        probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name,width,height', '-of', 'json', str(path)], check=True, capture_output=True, text=True, timeout=20)
        stream = json.loads(probe.stdout)['streams'][0]
        subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-threads', '1', '-i', str(path), '-f', 'null', '-'], check=True, capture_output=True, text=True, timeout=20)
        results.append(dict(preview=relative, status='decoded-preview', bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), **stream))
    report = dict(checked_at=datetime.now(timezone.utc).isoformat(), method='本地缩放 JPEG 预览：SHA-256、ffprobe、ffmpeg 解码；不代表原始 GIF 完整解码、模型复现或人工视觉验收。', items=results)
    (ROOT / 'docs/media-check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'本地预览解码通过：{len(results)}/{len(paths)}')


if __name__ == '__main__':
    main()
