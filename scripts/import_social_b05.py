#!/usr/bin/env python3
"""Fetch public Seedream 5.5 creator posts and store small, attributed stills and animated excerpts.
Public social media is not a redistribution license. This collection stores reduced illustrative
previews with original X post/media links, retaining all third-party rights.
"""
import hashlib
import io
import json
import re
import subprocess
import tempfile
import time
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen
from PIL import Image,ImageOps

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=json.loads((ROOT/"content/social-source-batch05.json").read_text())
MODEL=re.compile(r"(seedream[\s_.-]*5[\s_.-]*5|即梦5\.5|豆包\s*5\.5)",re.I)
MAX_IMG=16_000_000
MAX_MOV=35_000_000

def fetch(url,limit=MAX_IMG,kind="image"):
    parts=urlsplit(url)
    if parts.scheme!="https" or parts.hostname not in ("pbs.twimg.com","video.twimg.com"):
        raise ValueError("Disallowed media host: "+url)
    if parts.hostname=="pbs.twimg.com" and not (parts.path.startswith("/media/") or
       parts.path.startswith("/tweet_video_thumb/") or parts.path.startswith("/amplify_video_thumb/")):
        raise ValueError("Disallowed X image path")
    if parts.hostname=="video.twimg.com" and not (parts.path.startswith("/amplify_video/") or parts.path.startswith("/tweet_video/")):
        raise ValueError("Disallowed X video path")
    alternatives=[url]
    if parts.hostname=="pbs.twimg.com":
        alternatives += [urlunsplit((parts.scheme,parts.netloc,parts.path,"name=large","")),
                         urlunsplit((parts.scheme,parts.netloc,parts.path,"",""))]
    error=None
    for candidate in dict.fromkeys(alternatives):
        for attempt in range(2):
            try:
                req=Request(candidate,headers={"User-Agent":"Mozilla/5.0","Accept":"image/*,video/mp4,*/*"})
                with urlopen(req,timeout=40) as resp:
                    dest=urlsplit(resp.geturl())
                    if dest.scheme!="https" or dest.hostname not in ("pbs.twimg.com","video.twimg.com"):
                        raise ValueError("unexpected redirect")
                    b=resp.read(limit+1)
                    if len(b)<1024 or len(b)>limit: raise ValueError("bad byte length: "+str(len(b)))
                    return b
            except Exception as exc:
                error=exc
                time.sleep(0.8+attempt)
    raise RuntimeError(kind+" download failed: "+str(error))

def tweet_json(url):
    match=re.fullmatch(r"https://x\.com/([^/]+)/status/(\d+)",url)
    if not match: raise ValueError("Not an original X status URL: "+url)
    username,tid=match.groups()
    error=None
    for attempt in range(3):
        try:
            request=Request("https://api.fxtwitter.com/"+username+"/status/"+tid,
                 headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
            with urlopen(request,timeout=25) as res:
                body=res.read(2_000_001)
                if len(body)>2_000_000: raise ValueError("oversized tweet")
                tweet=(json.loads(body).get("tweet") or {})
                if not isinstance(tweet,dict) or not tweet.get("text"): raise ValueError("no tweet body")
                author=(tweet.get("author") or {}).get("screen_name","")
                if author.lower()!=username.lower(): raise ValueError("author mismatch")
                return tweet
        except Exception as exc:
            error=exc
            time.sleep(1+attempt)
    raise RuntimeError("X post could not be read: "+str(error))

def jpg_from_image(raw):
    Image.MAX_IMAGE_PIXELS=48_000_000
    with Image.open(io.BytesIO(raw)) as src:
        if src.format not in ("PNG","JPEG","WEBP"): raise ValueError("not image")
        pic=ImageOps.exif_transpose(src)
        if "A" in pic.getbands():
            backdrop=Image.new("RGB",pic.size,(247,247,247))
            backdrop.paste(pic,mask=pic.getchannel("A"))
            pic=backdrop
        else: pic=pic.convert("RGB")
        pic.thumbnail((640,640),Image.Resampling.LANCZOS)
        output=io.BytesIO()
        pic.save(output,"JPEG",quality=82,optimize=True)
        result=output.getvalue()
        if len(result)>=512*1024: raise ValueError("JPG > 512 KiB")
        with Image.open(io.BytesIO(result)) as verify:verify.verify()
        return result,pic.width,pic.height

def get_mp4_url(media):
    options=[f for f in (media.get("formats") or []) if
             f.get("container")=="mp4" and f.get("url","").startswith("https://video.twimg.com/")]
    if options:
        def rank(f):
            url=f.get("url") or ""
            w=re.search(r"/(\d+)x(\d+)/",url)
            width=int(w.group(1)) if w else 1000
            return abs(width-640)
        return sorted(options,key=rank)[0]["url"]
    return media.get("url")

def sample_video(raw):
    with tempfile.TemporaryDirectory() as d:
        inp=Path(d)/"input.mp4"; inp.write_bytes(raw)
        probe=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                               "-of","default=noprint_wrappers=1:nokey=1",str(inp)],
                              capture_output=True,text=True,timeout=20)
        try:duration=float(probe.stdout.strip())
        except (ValueError,TypeError):duration=6.0
        if not (duration>0):duration=6.0
        at=max(0.1,min(duration-0.2,duration*0.45))
        frame=Path(d)/"frame.jpg"
        for seek in (at,0.3):
            cmd=["ffmpeg","-y","-v","error","-ss",str(seek),"-i",str(inp),
                 "-frames:v","1","-vf","scale=640:640:force_original_aspect_ratio=decrease",str(frame)]
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
            if p.returncode==0 and frame.is_file() and frame.stat().st_size>200:
                break
        if not frame.is_file():raise RuntimeError("ffmpeg frame extraction failed")
        jpeg,w,h=jpg_from_image(frame.read_bytes())
        giffile=Path(d)/"excerpt.gif";gif=None
        start=max(0,min(duration-0.5,duration*0.15))
        for fps,width in [(7,240),(5,180)]:
            cmd=["ffmpeg","-y","-v","error","-ss",str(start),"-t",str(min(2.8,duration-start)),
                 "-i",str(inp),"-vf",f"fps={fps},scale={width}:-1:flags=lanczos",
                 "-loop","0",str(giffile)]
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=45)
            if p.returncode==0 and giffile.is_file() and 1000<giffile.stat().st_size<3_000_000:
                gif=giffile.read_bytes();break
        return jpeg,w,h,gif,duration

def main():
    cases_path=ROOT/"content/cases.json"
    check_path=ROOT/"docs/media-check.json"
    cases=json.loads(cases_path.read_text())
    report=json.loads(check_path.read_text())
    ids={c["id"] for c in cases}
    source_posts={c["source_url"].lower() for c in cases if c["source_url"].startswith("https://x.com/")}
    url_keys={m["url"].split("?")[0] for c in cases for m in c["media"]}
    checks={x["preview"]:x for x in report["items"]}
    added=[];failures=[];audit=[]
    anim_dir=ROOT/"assets/animations";anim_dir.mkdir(parents=True,exist_ok=True)
    for item in MANIFEST["cases"]:
        cid=item["id"];post=item["source_url"]
        if cid in ids or post.lower() in source_posts:
            print("SKIP existing",cid,flush=True);continue
        try:
            tweet=tweet_json(post)
            txt=str(tweet.get("text") or "")
            media=(tweet.get("media") or {})
            allmedia=media.get("all") or media.get("photos") or []
            byid={str(m.get("id") or ""):m for m in allmedia}
            ordered=[m for m in allmedia if m.get("type") in ("photo","video","gif")]
            if not ordered:raise ValueError("No media attached")
            is_model=bool(MODEL.search(txt))
            if not is_model and not item.get("curator_attribution_url"):
                raise ValueError("Post does not explicitly identify Seedream 5.5")
            print("POST",cid,"items",len(ordered),"explicit-model",is_model,flush=True)
            saved=[]
            anim=None
            for index,m in enumerate(ordered,1):
                try:
                    kind=m.get("type")
                    origin=(get_mp4_url(m) if kind in ("video","gif") else m.get("url"))
                    if not origin or origin.split("?")[0] in url_keys:
                        continue
                    if kind in ("video","gif"):
                        movie=fetch(origin,MAX_MOV,"movie")
                        jpg,w,h,gif,seconds=sample_video(movie)
                        if gif is not None and anim is None:
                            a_path=f"assets/animations/{cid}.gif"
                            (ROOT/a_path).write_bytes(gif);anim=a_path
                        item_type="video"
                    else:
                        image=fetch(origin,MAX_IMG,"photo")
                        jpg,w,h=jpg_from_image(image);seconds=None;item_type="image"
                    preview=f"assets/previews/{cid}-{index:02d}.jpg"
                    (ROOT/preview).write_bytes(jpg)
                    checks[preview]={"preview":preview,"status":"decoded-preview","bytes":len(jpg),
                                     "sha256":hashlib.sha256(jpg).hexdigest(),
                                     "codec_name":"mjpeg","width":w,"height":h}
                    saved.append({"url":origin,"type":item_type,"rights":"rights-reserved",
                                 "delivery":"local-preview-with-source-link","preview":preview,
                                 "preview_transform":"original-X-attachment-reduced-JPEG",
                                 "origin_media_id":str(m.get("id") or ""),"origin_alt":(m.get("altText") or "")[:180]})
                    url_keys.add(origin.split("?")[0])
                    print("SAVED",cid,index,item_type,len(jpg),flush=True)
                except Exception as exc:
                    failures.append({"id":cid,"media_index":index,"reason":str(exc)})
                    print("MEDIA ERROR",cid,index,str(exc)[:200],flush=True)
            if not saved:
                failures.append({"id":cid,"reason":"No supported X image/video asset saved"});continue
            note_zh="图片直接从作者 X 原帖媒体下载并缩放；视频只保存抽帧和短动图预览，完整视频请打开原始媒体。模型归因来自作者或署名整理，非本仓库复现。"
            note_en="Images are reduced previews fetched from the creator's X post; videos are represented by a still and short animated excerpt, with full video at source. Model attribution is source-reported, not independently reproduced."
            if item.get("comparison"):
                note_zh+=" 此帖含其他模型对照或跨模型制作，不能把整组当作 Seedream 独立输出。"
                note_en+=" This comparison or mixed workflow includes outputs from other models and is not a Seedream-only result."
            if item.get("kind")=="mixed-seedream-seedance-video" or item.get("kind")=="mixed-model-video":
                note_zh+=" 成片包含其他视频生成模型的制作环节。"
                note_en+=" The final animation involves other video-generation components."
            if item.get("curator_attribution_url"):
                note_zh+=" 社媒整理站提供了图片对应关系；请以原帖为准。"
                note_en+=" A curator catalog provides image provenance; refer to the author's original post."
            if item["category"]=="rgba-assets":
                note_zh+=" JPEG/GIF预览不能证明原文件的Alpha通道。"
                note_en+=" JPEG/GIF preview does not establish native source alpha transparency."
            has_prompt=("prompt:" in txt.lower() or "prompt：" in txt.lower())
            prompt={"status":"source-linked" if has_prompt else "not-published","url":post,"text":None}
            case={
                "id":cid,"title":item["title"],"category":item["category"],
                "author":item["source_author"],"source_url":post,
                "source_type":"creator-reported","model":"Seedream 5.5",
                "model_evidence":"creator-X-post-explicit" if is_model else "social-curator-with-matching-original-X-media",
                "checked_at":"2026-11-10","reproduced":False,
                "prompt":prompt,
                "caveat":{"zh-CN":note_zh,"en":note_en},
                "media":saved,
            }
            if anim:case["animation_preview"]=anim
            cases.append(case);ids.add(cid);source_posts.add(post.lower())
            audit.append({"id":cid,"source_url":post,"author":item["source_author"],"media_count":len(saved),
                          "media_types":[i["type"] for i in saved],"model_explicit":is_model,
                          "source_text_excerpt":txt[:250],
                          "prompt_status":prompt["status"],"animation_preview":anim})
            added.append({"id":cid,"images":sum(m["type"]=="image" for m in saved),
                          "video_sources":sum(m["type"]=="video" for m in saved),
                          "animation_preview":bool(anim),"source_url":post})
        except Exception as exc:
            failures.append({"id":cid,"reason":"post lookup or processing failed: "+str(exc)})
            print("POST ERROR",cid,str(exc)[:250],flush=True)
    if len(added)<7 or sum(a["images"]+a["video_sources"] for a in added)<16:
        raise RuntimeError("Not enough independently sourced media, abort without writing case files: "+json.dumps({"added":added,"failed":failures}))
    cases_path.write_text(json.dumps(cases,ensure_ascii=False,indent=2)+"\n")
    report["items"]=sorted(checks.values(),key=lambda x:x["preview"])
    check_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    audit_path=ROOT/"docs/social-source-batch05-audit.json"
    audit_path.write_text(json.dumps({
      "date":"2026-11-10","post_count":len(added),
      "image_source_count":sum(a["images"] for a in added),
      "video_source_count":sum(a["video_sources"] for a in added),
      "animated_previews":sum(bool(a["animation_preview"]) for a in added),
      "copyright":"Third-party rights reserved. Preview files are derived small excerpts; original media linked.",
      "source_audit":audit,"added":added,"failures":failures
    },ensure_ascii=False,indent=2)+"\n")
    src=ROOT/"docs/SOURCES.md"
    src.write_text(src.read_text().rstrip()+"\n\n## 第五批：X 创作者新案例（2026-11-10）\n\n"
        +"直接从 X 原帖公开的媒体接口提取对应图片和视频 URL，并保存压缩 JPEG 预览。动态帖另生成低分辨率的短 GIF 摘要，不打包原始完整 MP4。来源与媒体、失败记录及提示词公开状态均见 docs/social-source-batch05-audit.json 和 content/social-source-batch05.json。跨模型案例注明其他模型参与，作者保留全部媒体权利，本仓库没有独立复现。\n")
    builder=ROOT/"scripts/build.py"
    s=builder.read_text()
    if "Animated excerpt from X video" not in s:
        anchor="            if len(c['media']) > 1:"
        code="""            if c.get('animation_preview'):
                detail[-2:-2] = [
                    '', '## ' + choose('原帖视频的短动图预览', 'Animated excerpt from X video'), '',
                    f'![{name} — animated preview](../../{c["animation_preview"]})', '',
                    choose('这是原帖视频生成的低分辨率短动图预览，并非模型原生输出 GIF；完整视频请打开原始媒体。',
                           'Low-resolution excerpt of the source post video, not a native Seedream GIF. Open original media for the full video.'), ''
                ]
"""
        if anchor not in s: raise ValueError("builder anchor missing")
        s=s.replace(anchor,code+anchor)
    builder.write_text(s)
    validator=ROOT/"scripts/validate.py"
    v=validator.read_text().replace("m['type'] in {'image', 'gif'}","m['type'] in {'image', 'gif', 'video'}")
    anchor="        for m in c['media']:"
    if "animation_preview" not in v:
        code="""        if c.get('animation_preview'):
            anim = c['animation_preview']
            require(re.fullmatch(r'assets/animations/[a-z0-9-]+\\\\.gif', anim) is not None,
                    '动画预览路径无效')
            require((ROOT / anim).is_file() and 1000 < (ROOT / anim).stat().st_size < 3 * 1024 * 1024,
                    '动图预览缺失或超限')
"""
        # Avoid double-escaping regex in the resulting file
        code=code.replace("[a-z0-9-]+\\\\.gif","[a-z0-9-]+\\.gif")
        if anchor not in v: raise ValueError("validator anchor missing")
        v=v.replace(anchor,code+anchor)
    validator.write_text(v)
    subprocess.run(["python3","scripts/build.py"],cwd=ROOT,check=True)
    subprocess.run(["python3","scripts/validate.py"],cwd=ROOT,check=True)
    print("ARCHIVE COMPLETE",json.dumps({"cases":len(added),"images":sum(a["images"] for a in added),
           "video_sources":sum(a["video_sources"] for a in added),
           "animations":sum(bool(a["animation_preview"]) for a in added),"errors":len(failures)}),flush=True)

if __name__=="__main__":
    main()
