#!/usr/bin/env python3
"""One-off source-first ingestion of creator media; only reduced preview copies."""
import hashlib,io,json,re,subprocess,tempfile,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlsplit,urlunsplit
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=json.loads((ROOT/"content/social-source-batch07.json").read_text())
MAX_IMAGE=14_000_000; MAX_VIDEO=36_000_000

def get(url,cap=2_000_000):
    req=Request(url,headers={"User-Agent":"Mozilla/5.0","Accept":"application/json,image/*,video/mp4"})
    with urlopen(req,timeout=35) as resp:
        dest=urlsplit(resp.geturl())
        if dest.scheme!="https" or dest.hostname not in ("api.fxtwitter.com","pbs.twimg.com","video.twimg.com"):
            raise ValueError("Unexpected final host: "+resp.geturl())
        blob=resp.read(cap+1)
        if not 100<len(blob)<=cap:raise ValueError("Invalid response byte count")
        return blob

def tweet(item):
    m=re.fullmatch(r"https://x\.com/([^/]+)/status/(\d+)",item["post"])
    if not m: raise ValueError("Invalid original post")
    user,num=m.groups()
    last=None
    for n in range(3):
        try:
            t=json.loads(get(f"https://api.fxtwitter.com/{user}/status/{num}"))["tweet"]
            actual=(t.get("author") or {}).get("screen_name") or ""
            if actual.lower()!=user.lower():raise ValueError("Author mismatch")
            text=t.get("text") or ""
            if not re.search(r"(seedream[\s_.-]*5[\s_.-]*5|即梦.{0,6}5\.5)",text,re.I):
                raise ValueError("No version 5.5 attribution in original post")
            return t
        except Exception as exc:
            last=exc;time.sleep(n+1)
    raise RuntimeError(str(last))

def download(url,video=False):
    p=urlsplit(url)
    if p.scheme!="https":raise ValueError("Not HTTPS")
    if video:
        if p.hostname!="video.twimg.com" or not p.path.startswith(("/tweet_video/","/amplify_video/")):
            raise ValueError("Not original X video")
    else:
        if p.hostname!="pbs.twimg.com" or not p.path.startswith("/media/"):
            raise ValueError("Not original X image")
    urls=[url]
    if not video:
        urls.extend([urlunsplit((p.scheme,p.netloc,p.path,"name=large","")),urlunsplit((p.scheme,p.netloc,p.path,"",""))])
    error=None
    for candidate in dict.fromkeys(urls):
        for n in range(2):
            try:return get(candidate,MAX_VIDEO if video else MAX_IMAGE)
            except Exception as exc:error=exc;time.sleep(n+.5)
    raise RuntimeError(str(error))

def jpg(blob):
    Image.MAX_IMAGE_PIXELS=50_000_000
    with Image.open(io.BytesIO(blob)) as src:
        if src.format not in ("JPEG","PNG","WEBP"):raise ValueError("Unsupported image type")
        pic=ImageOps.exif_transpose(src)
        if "A" in pic.getbands():
            background=Image.new("RGB",pic.size,(245,245,245))
            background.paste(pic,mask=pic.getchannel("A"));pic=background
        else:pic=pic.convert("RGB")
        pic.thumbnail((640,640),Image.Resampling.LANCZOS)
        out=io.BytesIO();pic.save(out,"JPEG",quality=82,optimize=True)
        b=out.getvalue()
        if not 1000<len(b)<512*1024:raise ValueError("Preview too big or too small")
        with Image.open(io.BytesIO(b)) as verify:verify.verify()
        return b,pic.width,pic.height

def video_variant(m):
    variants=[f for f in m.get("formats",[]) if f.get("container")=="mp4" and str(f.get("url","")).startswith("https://video.twimg.com/")]
    if not variants:return m["url"]
    def sortkey(x):
        q=re.search(r"/(\d+)x(\d+)/",x["url"])
        return abs((int(q.group(1)) if q else 1280)-640)
    return sorted(variants,key=sortkey)[0]["url"]

def clip(blob):
    with tempfile.TemporaryDirectory() as d:
        source=Path(d)/"x.mp4";source.write_bytes(blob)
        duration_cmd=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1",str(source)],text=True,capture_output=True,timeout=20)
        try:duration=float(duration_cmd.stdout.strip())
        except ValueError:duration=6.0
        if not duration>0:duration=6.0
        frame=Path(d)/"frame.jpg"
        seek=min(max(.1,duration*.42),max(.1,duration-.15))
        p=subprocess.run(["ffmpeg","-y","-v","error","-ss",str(seek),"-i",str(source),
            "-frames:v","1","-vf","scale=640:640:force_original_aspect_ratio=decrease",
            str(frame)],capture_output=True,text=True,timeout=45)
        if p.returncode!=0 or not frame.exists():raise RuntimeError("Video frame decode failed "+p.stderr[:200])
        still,w,h=jpg(frame.read_bytes())
        gif_path=Path(d)/"sample.gif";gif=None
        for fps,width in ((7,240),(5,180)):
            proc=subprocess.run(["ffmpeg","-y","-v","error","-ss",str(max(.0,duration*.1)),"-t",str(min(2.6,duration*.75)),
                "-i",str(source),"-vf",f"fps={fps},scale={width}:-1:flags=lanczos","-loop","0",str(gif_path)],
                text=True,capture_output=True,timeout=60)
            if proc.returncode==0 and gif_path.exists() and 1000<gif_path.stat().st_size<3_000_000:
                gif=gif_path.read_bytes();break
        return still,w,h,gif

def run():
    cases_p=ROOT/"content/cases.json";checks_p=ROOT/"docs/media-check.json"
    cases=json.loads(cases_p.read_text());checks=json.loads(checks_p.read_text())
    known={c["source_url"].lower() for c in cases};ids={c["id"] for c in cases}
    prev={m["url"].split("?")[0] for c in cases for m in c["media"]}
    checked={c["preview"]:c for c in checks["items"]}
    (ROOT/"assets/animations").mkdir(parents=True,exist_ok=True)
    successes=[];failures=[]
    for item in MANIFEST["cases"]:
        if item["id"] in ids or item["post"].lower() in known:continue
        try:
            t=tweet(item)
            body=t.get("text") or ""
            media=(t.get("media") or {}).get("all") or (t.get("media") or {}).get("photos") or []
            if not media:raise ValueError("No attached original media")
            photos=[];animated=None
            for n,m in enumerate(media,1):
                kind=m.get("type")
                if kind not in ("photo","video","gif"):continue
                try:
                    origin=video_variant(m) if kind!="photo" else m.get("url")
                    if not origin or origin.split("?")[0] in prev:continue
                    raw=download(origin,kind!="photo")
                    if kind=="photo":
                        still,w,h=jpg(raw);gif=None
                    else:
                        still,w,h,gif=clip(raw)
                    target=f'assets/previews/{item["id"]}-{n:02d}.jpg'
                    (ROOT/target).write_bytes(still)
                    checked[target]={"preview":target,"status":"decoded-preview","bytes":len(still),
                                     "sha256":hashlib.sha256(still).hexdigest(),
                                     "codec_name":"mjpeg","width":w,"height":h}
                    photos.append({"url":origin,"type":"image" if kind=="photo" else "video",
                                   "rights":"rights-reserved","delivery":"local-preview-with-source-link",
                                   "preview":target,"preview_transform":"original-X-media-thumbnail-to-JPEG",
                                   "origin_media_id":str(m.get("id") or "")})
                    if gif and not animated:
                        animated=f'assets/animations/{item["id"]}.gif'
                        (ROOT/animated).write_bytes(gif)
                    prev.add(origin.split("?")[0])
                except Exception as exc:
                    failures.append({"id":item["id"],"media_index":n,"reason":str(exc)})
            if not photos:raise ValueError("No usable original-media attachment")
            phrase=("图片为从 X 原帖保存的压缩预览；视频为短动图摘要，不是原生 Seedream GIF。"
                    "模型结果及数据由作者自报，本站未独立复现。")
            english=("Source X images saved as compressed previews; video is represented by a brief derived GIF, "
                     "not model-native animation. Creator assertions are not independently reproduced.")
            if item["comparison"]:
                phrase+=" 包含跨模型对照/其他生成工具，不能将所有媒体归类为 Seedream 单独生成。"
                english+=" Multi-model or external workflow: not every frame is Seedream-only."
            prompt={"status":"not-published","url":item["post"],"text":None}
            case={"id":item["id"],"title":item["title"],"category":item["category"],
                  "author":item["author"],"source_url":item["post"],
                  "source_type":"creator-reported","model":"Seedream 5.5",
                  "model_evidence":"public-author-X-post-and-media",
                  "checked_at":"2026-11-11","reproduced":False,"prompt":prompt,
                  "caveat":{"zh-CN":phrase,"en":english},"media":photos}
            if animated:case["animation_preview"]=animated
            cases.append(case);known.add(item["post"].lower());ids.add(item["id"])
            successes.append({"id":item["id"],"post":item["post"],"creator":item["author"],
                              "media_count":len(photos),"animated":bool(animated),
                              "text_excerpt":body[:350],"prompt_status":prompt["status"],
                              "media":photos})
            print("CASE SAVED",item["id"],len(photos),"GIF",bool(animated),flush=True)
        except Exception as exc:
            failures.append({"id":item["id"],"reason":str(exc)})
            print("CASE FAILED",item["id"],str(exc)[:200],flush=True)
    if len(successes)<4:
        raise RuntimeError("Fewer than 4 new cases; abort: "+json.dumps(failures))
    cases_p.write_text(json.dumps(cases,indent=2,ensure_ascii=False)+"\n")
    checks["items"]=sorted(checked.values(),key=lambda x:x["preview"])
    checks_p.write_text(json.dumps(checks,indent=2,ensure_ascii=False)+"\n")
    audit={"checked_at":"2026-11-11","added":successes,"failed":failures,
           "copyright":"Only reduced media previews; rights reserved by respective creators.",
           "model_limit":"Mixed-model outputs labeled; model version self-attributed."}
    (ROOT/"docs/social-source-batch07-audit.json").write_text(json.dumps(audit,indent=2,ensure_ascii=False)+"\n")
    src=ROOT/"docs/SOURCES.md"
    src.write_text(src.read_text().rstrip()+"\n\n## 第七批 X 社媒原帖图片和视频（2026-11-11）\n\n"
                   "从原始作者 X 帖子公开媒体直接提取图片/视频 CDN 地址，下载压缩 JPEG 预览和视频短动图；"
                   "作者、来源、媒体 ID、缺失 Prompt 状态、失败条目见 docs/social-source-batch07-audit.json。"
                   "多模型案例不表示全部画面由 Seedream 5.5 生成。未独立复现，第三方媒体权利保留。\n")
    subprocess.run(["python3","scripts/build.py"],cwd=ROOT,check=True)
    subprocess.run(["python3","scripts/validate.py"],cwd=ROOT,check=True)
    print("DONE",len(successes),"new cases",flush=True)
if __name__=="__main__":run()
