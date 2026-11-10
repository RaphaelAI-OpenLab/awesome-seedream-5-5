#!/usr/bin/env python3
"""离线检索案例标题、分类、作者与提示词。"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('query')
parser.add_argument('--json', action='store_true')
args = parser.parse_args()
cases = json.loads((ROOT / 'content/cases.json').read_text())
found = [c for c in cases if args.query.casefold() in json.dumps(c, ensure_ascii=False).casefold()]
if args.json:
    print(json.dumps(found, ensure_ascii=False, indent=2))
else:
    for case in found:
        print(f'{case["title"]["zh-CN"]} / {case["title"]["en"]}\n  {ROOT / "cases" / case["id"] / "README.zh-CN.md"}\n  {case["source_url"]}')
    print(f'匹配 {len(found)} 个案例')
