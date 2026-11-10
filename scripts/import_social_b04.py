#!/usr/bin/env python3
"""Collect public X image posts into small, attributed Seedream 5.5 previews."""
import hashlib,io,json,re,subprocess,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from urllib.parse import urlsplit,urlunsplit
from urllib.request import Request,urlopen
from PIL import Image,ImageOps

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=json.loads((ROOT/"content/social-source-batch04.json").read_text())
MODEL=re.compile(r"seedream[\s_.-]*5[\s_.-]*5|sd[\s_.-]*5[\s_.-]*5",re.I)

def get_json(url):
    last=None
    for i in range(3):
        try:
            req=Request(url,headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
            with urlopen(req,timeout=24) as r:
                b=r.read(2000001)
            if len(b)>2000000: raise ValueError("JSON too big")
            return json.loads(b)
        except Exception as e:
            last=e
            time.sleep(1+i)
    raise RuntimeError(str(last))

def source_post(item):
    url=item["source_url"]
    match=re.fullmatch(r"https://x\.com/([^/]+)/status/(\d+)",url)
    if not match: raise ValueError("Not a post "+url)
    handle,number=match.groups()
    try:
        result=get_json("https://api.fxtwitter.com/"+handle+"/status/"+number)
        tweet=result.get("tweet") or {}
        media=tweet.get("media") or {}
        photos=media.get("photos") or [m for m in media.get("all",[]) if m.get("type")=="photo"]
        if photos:
            text=str(tweet.get("text") or "")
            return [{"id":str(p.get("id") or ""),"url":p["url"],"alt":p.get("altText") or ""} for p in photos],text,"fx-public"
    except Exception as e:
        print("Fx fallback",item["id"],str(e)[:120],flush=True)
    tweet=get_json("https://cdn.syndication.twimg.com/tweet-result?id="+number+"&lang=en&token=0")
    photos=tweet.get("photos") or []
    media=[m for m in tweet.get("mediaDetails",[]) if m.get("type")=="photo"]
    parsed=[]
    for j,p in enumerate(photos):
        code=str(media[j].get("id_str") or media[j].get("id") or "") if j<len(media) else ""
        parsed.append({"id":code,"url":p["url"],"alt":p.get("accessibilityLabel") or ""})
    if not parsed: raise ValueError("No X photos")
    return parsed,str(tweet.get("text") or ""),"x-syndication"

def fetch_image(url):
    p=urlsplit(url)
    if p.scheme!="https" or p.hostname not in ("pbs.twimg.com","cdn.beatapi.io"):
        raise ValueError("Unsupported image host")
    if p.hostname=="pbs.twimg.com" and not p.path.startswith("/media/"):
        raise ValueError("Not an X media file")
    if p.hostname=="cdn.beatapi.io" and not p.path.startswith("/prompt-gallery/seedream-5-5/"):
        raise ValueError("Not a gallery media file")
    opts=[url]
    if p.hostname=="pbs.twimg.com":
        opts.append(urlunsplit((p.scheme,p.netloc,p.path,"name=large","")))
        opts.append(urlunsplit((p.scheme,p.netloc,p.path,"","")))
    error=None
    for attempt_url in dict.fromkeys(opts):
        for retry in range(2):
            try:
                req=Request(attempt_url,headers={"User-Agent":"Mozilla/5.0","Accept":"image/*"})
                with urlopen(req,timeout=25) as r:
                    if urlsplit(r.geturl()).hostname not in ("pbs.twimg.com","cdn.beatapi.io"):
                        raise ValueError("Unexpected redirect")
                    blob=r.read(18000001)
                if len(blob)<1024 or len(blob)>18000000: raise ValueError("Invalid size")
                return blob
            except Exception as e:
                error=e
                time.sleep(retry+0.4)
    raise RuntimeError(str(error))

def preview_photo(task):
    item,number,photo=task
    raw=fetch_image(photo["url"])
    Image.MAX_IMAGE_PIXELS=48000000
    with Image.open(io.BytesIO(raw)) as source:
        if source.format not in ("PNG","JPEG","WEBP"): raise ValueError("Unexpected format")
        img=ImageOps.exif_transpose(source)
        if "A" in img.getbands():
            base=Image.new("RGB",img.size,(245,245,245))
            base.paste(img,mask=img.getchannel("A"))
            img=base
        else:
            img=img.convert("RGB")
        img.thumbnail((640,640),Image.Resampling.LANCZOS)
        buf=io.BytesIO()
        img.save(buf,format="JPEG",quality=82,optimize=True)
        jpeg=buf.getvalue()
        if len(jpeg)>=512*1024: raise ValueError("Preview too large")
        with Image.open(io.BytesIO(jpeg)) as test: test.verify()
    return (item["id"],number,photo,jpeg,img.width,img.height,hashlib.sha256(raw).hexdigest())

def main():
    source={}
    errors=[]
    for item in MANIFEST["x_cases"]:
        try:
            photos,text,method=source_post(item)
            wanted=item["media_ids"]
            picked=[next((p for p in photos if p["id"]==id),None) for id in wanted]
            picked=[p for p in picked if p]
            if not picked and method=="x-syndication" and len(photos)==len(wanted):
                picked=photos
            if not picked: raise ValueError("Media IDs do not match source post")
            explicit=bool(MODEL.search(text+" "+" ".join(p["alt"] for p in picked)))
            source[item["id"]]={"item":item,"photos":picked,"text":text,"method":method,"explicit":explicit}
            print("POST",item["id"],len(picked),"model-explicit",explicit,flush=True)
            if len(picked)!=len(wanted):
                errors.append({"id":item["id"],"reason":"partial photo IDs","wanted":len(wanted),"matched":len(picked)})
        except Exception as exc:
            errors.append({"id":item["id"],"reason":"X lookup failed","error":str(exc)})
            print("POST ERROR",item["id"],str(exc),flush=True)
    for item in MANIFEST["prompt_cases"]:
        source[item["id"]]={"item":item,"photos":[{"id":"curator","url":item["media_url"],"alt":""}],
                           "text":item["prompt_text"],"method":"public-source-prompt-and-media","explicit":True}
    casefile=ROOT/"content/cases.json"
    reportfile=ROOT/"docs/media-check.json"
    cases=json.loads(casefile.read_text())
    report=json.loads(reportfile.read_text())
    caseids={x["id"] for x in cases}
    occupied={m["url"].split("?")[0] for c in cases for m in c["media"]}
    checked={x["preview"]:x for x in report["items"]}
    tasks=[(d["item"],index,photo) for key,d in source.items() if key not in caseids
           for index,photo in enumerate(d["photos"],1) if photo["url"].split("?")[0] not in occupied]
    gotten={}
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures={executor.submit(preview_photo,task):task for task in tasks}
        for fut in as_completed(futures):
            task=futures[fut]
            try:
                id,num,photo,jpeg,w,h,original_hash=fut.result()
                gotten[(id,num)]=(photo,jpeg,w,h,original_hash)
                print("MEDIA",id,num,w,h,len(jpeg),flush=True)
            except Exception as exc:
                errors.append({"id":task[0]["id"],"index":task[1],"error":str(exc),"reason":"media download failed"})
                print("MEDIA ERROR",task[0]["id"],task[1],str(exc),flush=True)
    additions=[]
    audits=[]
    for id,d in source.items():
        item=d["item"]
        if id in caseids: continue
        media=[]
        for number,photo in enumerate(d["photos"],1):
            k=gotten.get((id,number))
            if not k: continue
            _,jpeg,w,h,original_hash=k
            filename=f"assets/previews/{id}-{number:02d}.jpg"
            (ROOT/filename).write_bytes(jpeg)
            checked[filename]={"preview":filename,"status":"decoded-preview","bytes":len(jpeg),
                               "sha256":hashlib.sha256(jpeg).hexdigest(),"codec_name":"mjpeg",
                               "width":w,"height":h}
            media.append({"url":photo["url"],"type":"image","rights":"rights-reserved",
                          "delivery":"local-preview-with-source-link","preview":filename,
                          "preview_transform":"original-X-post-attachment-resized-to-640px-jpeg",
                          "origin_media_id":photo.get("id"),"origin_alt":photo.get("alt","")[:200]})
            occupied.add(photo["url"].split("?")[0])
        if not media:
            errors.append({"id":id,"reason":"no media downloaded"})
            continue
        if "prompt_text" in item:
            prompt={"status":"original","url":item["source_mirror_url"],"text":item["prompt_text"]}
            evidence="creator-prompt-from-attributed-public-social-mirror"
        else:
            prompt={"status":"source-linked" if re.search(r"\bprompt\s*[:：]",d["text"],re.I) else "not-published",
                    "url":item["source_url"],"text":None}
            evidence=("author-post-and-original-X-media-verified" if d["explicit"]
                      else "original-X-media-verified-model-attributed-by-curator")
        zh="已从作者 X 原帖下载配图，并保存为640px以内的JPEG预览。模型来源归因未经独立生成验证。"
        en="Photos fetched from the author's original X post; local JPEG previews are at most 640px. Model attribution is not an independent reproduction."
        if item.get("comparison"):
            zh+=" 原帖为多模型对比，部分图片来自其他模型，需按原帖标签区分。"
            en+=" This multi-model comparison includes outputs from other models; follow labels at the source."
        if item["category"]=="rgba-assets":
            zh+=" 缩略图无法证明原始Alpha透明度。"
            en+=" JPEG preview does not verify original alpha."
        if item.get("source_description_zh"):
            zh+=" "+item["source_description_zh"]
            en+=" "+item.get("source_description_en","")
        cases.append({"id":id,"title":item["title"],"category":item["category"],
                      "author":item["author"],"source_url":item["source_url"],
                      "source_type":"creator-reported","model":"Seedream 5.5",
                      "model_evidence":evidence,"checked_at":"2026-11-10",
                      "reproduced":False,"prompt":prompt,"caveat":{"zh-CN":zh,"en":en},"media":media})
        additions.append({"id":id,"images":len(media),"source_url":item["source_url"],
                          "prompt":prompt["status"],"previews":[m["preview"] for m in media]})
        audits.append({"id":id,"method":d["method"],"explicit_seedream_5_5_text":d["explicit"],
                       "author_text_excerpt":d["text"][:240],
                       "media_id_count":len(d["photos"]),
                       "downloaded":len(media)})
    image_count=sum(x["images"] for x in additions)
    if len(additions)<8 or image_count<12:
        raise RuntimeError("Too few images for publication: "+str(additions)+"; errors="+str(errors))
    casefile.write_text(json.dumps(cases,ensure_ascii=False,indent=2)+"\n")
    report["items"]=sorted(checked.values(),key=lambda x:x["preview"])
    reportfile.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    (ROOT/"docs/social-x-batch04-audit.json").write_text(json.dumps(
        {"checked_at":"2026-11-10","original_medium":"public X CDN media URLs",
         "independently_reproduced":False,"copyright":"Third-party rights reserved",
         "added":additions,"source_audit":audits,"failures":errors},ensure_ascii=False,indent=2)+"\n")
    builder=ROOT/"scripts/build.py"
    s=builder.read_text()
    anchor="            if prompt['status'] == 'original':"
    gallery="""            if len(c['media']) > 1:
                gallery = ['', '## ' + choose('同一原帖的更多图片', 'More photos from the original post'), '']
                for number, frame in enumerate(c['media'][1:], 2):
                    gallery += [f'**{choose("配图", "Image")} {number}**', '',
                                f'![{name} - {number}](../../{frame["preview"]})', '',
                                f'[{choose("原媒体", "Source media")}]({frame["url"]})', '']
                detail[-2:-2] = gallery
"""
    if "More photos from the original post" not in s:
        if anchor not in s: raise ValueError("Builder anchor missing")
        s=s.replace(anchor,gallery+anchor)
    s=s.replace("以上为作者公开的原始指令，包含波兰语文案。没有执行复现。",
                "这是原作者或来源整理者公开的提示词，本站未独立复现，第三方转载请对照原帖。")
    s=s.replace("The source author published this exact instruction, including the Polish copy. It has not been reproduced here.",
                "This public source prompt is attributed to the creator. This case was not independently reproduced.")
    builder.write_text(s)
    sourcefile=ROOT/"docs/SOURCES.md"
    sourcefile.write_text(sourcefile.read_text().rstrip()+"\n\n## 第四批：X 社媒图片原帖归档（2026-11-10）\n\n"
      +"通过公开 X 帖子数据接口，按作者单帖 ID 核对媒体 ID，并从 pbs.twimg.com 下载实际图片。多图帖子作为一个案例，保存多张压缩 JPEG 预览与原图链接；对比案例不把其他模型图片说成 Seedream 单模型输出。另有两条公开完整 Prompt 的透明素材案例来自 BeatAPI 的署名整理。各项成功/失败及来源证据见 docs/social-x-batch04-audit.json。原作者保留媒体和提示词的相应权利，本站不宣称独立复现。\n")
    subprocess.run(["python3","scripts/build.py"],cwd=ROOT,check=True)
    subprocess.run(["python3","scripts/validate.py"],cwd=ROOT,check=True)
    print("SUCCESS cases",len(additions),"downloaded images",image_count,"errors",len(errors),flush=True)

if __name__=="__main__":
    main()
