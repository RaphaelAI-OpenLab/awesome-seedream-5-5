#!/usr/bin/env python3
"""Generate external reference queue and bilingual individual case pages."""
import argparse,json,html
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/"external-references"
ZH={"typography":"文字与海报","portraits":"人物与肖像","photography":"摄影与商品","interiors":"室内设计","characters":"角色与插画","infographics":"信息图","rgba-assets":"透明素材","multi-turn-editing":"多轮编辑"}
EN={"typography":"Typography and posters","portraits":"Portraits","photography":"Photography and products","interiors":"Interior design","characters":"Characters and illustrations","infographics":"Infographics","rgba-assets":"Transparent assets","multi-turn-editing":"Multi-turn editing"}
FENCE=chr(96)*3
def data():return json.loads((DIR/"cases.json").read_text(encoding="utf-8"))["cases"]
def filename(lang):return "README.zh-CN.md" if lang=="zh-CN" else "README.md"
def choose(lang,zh,en):return zh if lang=="zh-CN" else en
def outputs():
    cases=data()
    out={}
    for lang in ("en","zh-CN"):
        zh=lang=="zh-CN"
        labels=ZH if zh else EN
        npreviews=sum(bool(m.get("preview")) for c in cases for m in c["media"])
        nremade=sum(c["remake"]["status"]!="pending" for c in cases)
        title=choose(lang,"Seedream 5.5 全网外部参考 · 待重做","Seedream 5.5 web-wide reference and remake queue")
        lines=["<!-- Generated: edit cases.json, then run scripts/build_external_refs.py -->","",
               "# "+title,"","[English](README.md) · [简体中文](README.zh-CN.md)","",
               choose(lang,"这是独立的第三方图片和公开提示词整理区，不属于主 README 的正式案例，也不是 Raphael 自行生成的结果。",
                      "This separate collection contains third-party images and public prompts. These are not main collection cases or Raphael-generated outputs."),"",
               "**"+choose(lang,"待重做参考","References")+f": {len(cases)} · "+choose(lang,"本地低清预览","Local low-res previews")+f": {npreviews} · "+choose(lang,"已重做","Recreated")+f": {nremade}**","",
               choose(lang,"**版权：** 公开网页不代表可授权转载。图片可能受版权保护，本文仅供素材核对；正式宣传前须取得许可或移除参考预览。重新生成也不自动消除对他人作品、商标、肖像等权利的影响。",
                      "**Rights:** Public URLs do not grant rehosting rights. Source previews are research references only. Remove or license them before public promotion. A new generation is not automatically free of likeness, trademark or other rights issues."),"",
               choose(lang,"[查看重做流程](WORKFLOW.md) · [查看原始数据](cases.json) · [返回主仓库](../README.zh-CN.md)",
                      "[Remake workflow](WORKFLOW.md) · [Raw data](cases.json) · [Back to main](../README.md)"),"",
               "## "+choose(lang,"按分类浏览","Categories"),""]
        counts=Counter(c["category"] for c in cases)
        for cat,label in labels.items():
            if counts[cat]:lines.append(f"- [{label} ({counts[cat]})](#{cat})")
        lines.append("")
        for cat,label in labels.items():
            group=[c for c in cases if c["category"]==cat]
            if not group:continue
            lines.extend([f'<a id="{cat}"></a>',"## "+label,""])
            for c in group:
                name=c["title"][lang]
                link=f"cases/{c['id']}/{filename(lang)}"
                lines.extend(["### "+f"[{name}]({link})",""])
                first=c["media"][0]
                if first.get("preview"):
                    lines.extend([f'<a href="{link}"><img src="{html.escape(first["preview"],quote=True)}" alt="{html.escape(name,quote=True)}" width="300" loading="lazy" /></a>',""])
                else:
                    lines.extend([choose(lang,"预览未下载，原图仍可从来源打开。","Preview unavailable; original source link retained."),""])
                state=c["remake"]["status"]
                lines.extend([f"**{c['source_name']}** · "+choose(lang,"待重做" if state=="pending" else "已重做",
                    "Pending" if state=="pending" else "Recreated")+f" · [{choose(lang,'来源','Source')}]({c['source_url']})",""])
                detail=["<!-- Generated from external-references/cases.json; not original model output by Raphael. -->",
                        "# "+name,"","[English](README.md) · [简体中文](README.zh-CN.md)","",
                        f"[{choose(lang,'返回外部素材库','Back to external queue')}](../../{filename(lang)})","",
                        choose(lang,"**状态：待重做。第三方网站自报模型和结果，本站尚未独立复现。**",
                               "**Status: pending remake. Model and outputs are source-reported, not independently reproduced.**"),""]
                for idx,m in enumerate(c["media"],1):
                    detail.extend(["## "+choose(lang,"原始参考图","Original reference")+" "+str(idx),""])
                    if m.get("preview"):
                        detail.extend([f"![{name} {idx}](../../{m['preview']})",""])
                    else:detail.extend([choose(lang,"原图未保存到仓库，本项只有外部媒体入口。","Not stored locally; only the source-media URL is available."),""])
                    detail.extend([f"[{choose(lang,'打开来源图片','Open source image')}]({m['url']})",""])
                detail.extend(["## "+choose(lang,"来源公开 Prompt","Source-published prompt"),"",
                    choose(lang,"网站将以下文案标注为该结果的提示词；转载许可、生成模型和参数尚未独立审计。",
                           "The website associates this prompt with its output; license, model execution and settings were not independently audited."),"",
                    FENCE+"text",c["prompt"]["text"],FENCE,"",
                    f"[{choose(lang,'核对来源原文','Check original source')}]({c['prompt']['url']})",""])
                if c.get("steps"):
                    detail.extend(["## "+choose(lang,"连续编辑步骤","Edit sequence"),""])
                    for step in c["steps"]:
                        detail.extend(["### "+str(step["round"])+". "+step["title"],"",FENCE+"text",step["prompt"],FENCE,""])
                detail.extend(["## "+choose(lang,"重做与授权","Remake and rights"),"",
                   "- "+choose(lang,"来源","Source")+f": {c['source_name']} · [{c['source_url']}]({c['source_url']})",
                   "- "+choose(lang,"来源模型归因","Model evidence")+": "+c["model_evidence"],
                   "- "+choose(lang,"工作流","Workflow")+": "+c["workflow"],
                   "- "+choose(lang,"图像许可","Media license")+": "+c["rights"]["republication_license"],
                   "- "+choose(lang,"重做状态","Remake status")+": "+c["remake"]["status"],
                   "- "+choose(lang,"本次重做文件数","Owned replacement files")+": "+str(len(c["remake"]["own_media"])),"",
                   choose(lang,"后续生成的新图请放到独立 remade 目录并更新结构化状态；对来源图片的转载应在发布前处理授权或删除。",
                          "Put new outputs in the remade directory and update structured status. Clear licensing or remove source-media previews before promotion."),"",
                   choose(lang,"备注："+c["caveat"],"Notes: "+c["caveat"]),""])
                out[DIR/link]="\n".join(detail)
        out[DIR/filename(lang)]="\n".join(lines)
    return out
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--check",action="store_true");args=parser.parse_args()
    results=outputs();stale=[p for p,s in results.items() if not p.is_file() or p.read_text(encoding="utf-8")!=s]
    if args.check:
        if stale:raise SystemExit("External pages stale: "+", ".join(str(x.relative_to(ROOT)) for x in stale[:12]))
        print("External pages match:",len(results))
    else:
        for path,content in results.items():
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding="utf-8")
        print("External pages written:",len(results))
if __name__=="__main__":main()
