#!/usr/bin/env python3
"""Recover X video attachments after the first image pass; make JPG and tiny GIF excerpts."""
import hashlib,io,json,re,subprocess,tempfile,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlsplit
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/"content/social-source-batch05.json").read_text())
targets={"social05-kevin-watchmaker-forest","social05-xiaohu-thirty-round-gif",
 "social05-larklee-turkey-mixed-workflow","social05-sjonkerr-street-weather-edit",
 "social05-opener-morphic-character","social05-vortex-fifteen-round-compare"}

def get_tweet(post):
 m=re.fullmatch(r"https://x\.com/([^/]+)/status/(\d+)",post)
 if not m:raise ValueError("not an X status")
 handle,tid=m.groups()
 e=None
 for retry in range(3):
  try:
   req=Request("https://api.fxtwitter.com/"+handle+"/status/"+tid,
               headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
   with urlopen(req,timeout=25) as r:
    payload=json.loads(r.read(2_000_000))
   tweet=payload.get("tweet") or {}
   if (tweet.get("author") or {}).get("screen_name","").lower()!=handle.lower():
    raise ValueError("author mismatch")
   return tweet
  except Exception as ex:
   e=ex;time.sleep(retry+1)
 raise RuntimeError(str(e))

def select_video(m):
 versions=[v for v in m.get("formats",[]) if v.get("container")=="mp4" and "video.twimg.com" in v.get("url","")]
 if versions:
  def rank(x):
   width=re.search(r"/(\d+)x\d+/",x["url"])
   w=int(width.group(1)) if width else 1200
   return abs(w-640)
  return min(versions,key=rank)["url"]
 return m.get("url")

def download(url):
 p=urlsplit(url)
 if p.scheme!="https" or p.hostname!="video.twimg.com" or not p.path.startswith(("/tweet_video/","/amplify_video/")):
  raise ValueError("Untrusted video CDN")
 e=None
 for retry in range(3):
  try:
   req=Request(url,headers={"User-Agent":"Mozilla/5.0","Accept":"video/mp4"})
   with urlopen(req,timeout=45) as r:
    if urlsplit(r.geturl()).hostname!="video.twimg.com":raise ValueError("redirect")
    data=r.read(35_000_001)
   if len(data)<1024 or len(data)>35_000_000:raise ValueError("invalid MP4 size")
   return data
  except Exception as ex:
   e=ex;time.sleep(retry+1)
 raise RuntimeError(str(e))

def decode(blob,reported_duration):
 with tempfile.TemporaryDirectory() as tmp:
  inp=Path(tmp)/"source.mp4";inp.write_bytes(blob)
  duration=float(reported_duration or 0)
  if duration<1.0:
   p=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
    "-of","default=noprint_wrappers=1:nokey=1",str(inp)],text=True,capture_output=True,timeout=20)
   try: duration=float(p.stdout.strip())
   except ValueError:duration=5.0
  at=max(0.1,min(duration*0.42,max(0.1,duration-0.2)))
  path=Path(tmp)/"one.png"
  cmd=["ffmpeg","-y","-v","error","-ss",str(at),"-i",str(inp),
       "-vf","scale=640:640:force_original_aspect_ratio=decrease",
       "-frames:v","1",str(path)]
  p=subprocess.run(cmd,capture_output=True,text=True,timeout=50)
  if p.returncode!=0 or not path.is_file():raise RuntimeError("ffmpeg still: "+p.stderr[:300])
  with Image.open(path) as pic:
   pic=pic.convert("RGB")
   out=io.BytesIO();pic.save(out,"JPEG",quality=82,optimize=True);jpg=out.getvalue()
   w,h=pic.size
  if not(1000<len(jpg)<512*1024):raise ValueError("invalid JPG size")
  gifpath=Path(tmp)/"excerpt.gif";gif=None
  for fps,width in [(7,240),(5,180)]:
   p=subprocess.run(["ffmpeg","-y","-v","error","-ss",str(min(duration*0.18,max(0,duration-0.5))),
       "-t",str(min(2.8,max(0.5,duration*0.55))),"-i",str(inp),
       "-vf",f"fps={fps},scale={width}:-1:flags=lanczos","-loop","0",str(gifpath)],
       capture_output=True,text=True,timeout=50)
   if p.returncode==0 and gifpath.is_file() and 1000<gifpath.stat().st_size<3_000_000:
    gif=gifpath.read_bytes();break
  return jpg,w,h,gif

def main():
 casefile=ROOT/"content/cases.json"
 reportfile=ROOT/"docs/media-check.json"
 auditfile=ROOT/"docs/social-source-batch05-audit.json"
 cases=json.loads(casefile.read_text())
 report=json.loads(reportfile.read_text())
 audit=json.loads(auditfile.read_text())
 byid={c["id"]:c for c in cases}
 checks={x["preview"]:x for x in report["items"]}
 seen={m["url"].split("?")[0] for c in cases for m in c["media"]}
 media_dir=ROOT/"assets/animations";media_dir.mkdir(exist_ok=True,parents=True)
 recovered=[];failures=[]
 for item in manifest["cases"]:
  if item["id"] not in targets:continue
  id=item["id"]
  try:
   tweet=get_tweet(item["source_url"])
   videos=[m for m in ((tweet.get("media") or {}).get("all") or []) if m.get("type") in ("video","gif")]
   if not videos:
    failures.append({"id":id,"reason":"No original X video attachment"});continue
   medias=[]
   for idx,m in enumerate(videos,1):
    origin=select_video(m)
    if not origin or origin.split("?")[0] in seen:continue
    raw=download(origin)
    jpg,w,h,gif=decode(raw,m.get("duration"))
    preview=f"assets/previews/{id}-video-{idx:02d}.jpg"
    (ROOT/preview).write_bytes(jpg)
    checks[preview]={"preview":preview,"status":"decoded-preview","bytes":len(jpg),
                     "sha256":hashlib.sha256(jpg).hexdigest(),"codec_name":"mjpeg",
                     "width":w,"height":h}
    medias.append({"url":origin,"type":"video","rights":"rights-reserved",
                   "delivery":"local-preview-with-source-link","preview":preview,
                   "preview_transform":"X-video-excerpt-JPEG-still",
                   "origin_media_id":str(m.get("id"))})
    anim=None
    if gif:
     anim=f"assets/animations/{id}.gif"
     (ROOT/anim).write_bytes(gif)
    if id in byid:
     case=byid[id]
    else:
     zh="直接从 X 作者原帖视频抽帧，短GIF为预览而非模型原生 GIF。完整视频见原媒体链接。"
     en="Still and short GIF extracted from the original X post video, not a native model GIF. The source link has the full video."
     if item.get("comparison"):
      zh+=" 这是跨模型比较/混合工作流，不应全部视为 Seedream 5.5 单模型输出。"
      en+=" This comparison or mixed workflow contains outputs by other models."
     case={"id":id,"title":item["title"],"category":item["category"],"author":item["source_author"],
           "source_url":item["source_url"],"source_type":"creator-reported",
           "model":"Seedream 5.5","model_evidence":"creator-X-post-explicit",
           "checked_at":"2026-11-10","reproduced":False,
           "prompt":{"status":"not-published","url":item["source_url"],"text":None},
           "caveat":{"zh-CN":zh,"en":en},"media":[]}
     cases.append(case);byid[id]=case
    case["media"].extend(medias)
    if anim:case["animation_preview"]=anim
    seen.add(origin.split("?")[0])
    recovered.append({"id":id,"video_url":origin,"frame":preview,"gif":anim,"bytes":len(raw)})
    print("RECOVERED",id,preview,"gif",bool(anim),flush=True)
   if not medias:
    failures.append({"id":id,"reason":"no new video media"})
  except Exception as e:
   failures.append({"id":id,"reason":str(e)})
   print("ERROR",id,str(e)[:280],flush=True)
 if len(recovered)<4:raise RuntimeError("Video repair shortfall: "+json.dumps({"recovered":recovered,"failures":failures}))
 casefile.write_text(json.dumps(cases,ensure_ascii=False,indent=2)+"\n")
 report["items"]=sorted(checks.values(),key=lambda x:x["preview"])
 reportfile.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
 audit["recovered_video_sources"]=recovered
 audit["initial_run_failures"]=audit.get("failures",[])
 audit["failures"]=failures+[i for i in audit.get("failures",[]) if i.get("id") not in targets]
 audit["video_source_count"]=sum(a["video_sources"] for a in audit.get("added",[]))+len(recovered)
 audit["animated_previews"]=sum(bool(a["animation_preview"]) for a in audit.get("added",[]))+sum(bool(x["gif"]) for x in recovered)
 for add in audit["added"]:
  matching=[x for x in recovered if x["id"]==add["id"]]
  if matching:
   add["video_sources"]+=len(matching)
   add["animation_preview"]=bool(matching[0]["gif"])
 for rec in recovered:
  if not any(x["id"]==rec["id"] for x in audit["added"]):
   audit["added"].append({"id":rec["id"],"images":0,"video_sources":1,
                          "animation_preview":bool(rec["gif"]),
                          "source_url":byid[rec["id"]]["source_url"]})
 audit["post_count"]=len(audit["added"])
 auditfile.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n")
 subprocess.run(["python3","scripts/build.py"],cwd=ROOT,check=True)
 subprocess.run(["python3","scripts/validate.py"],cwd=ROOT,check=True)
 print("VIDEO RECOVERY SUCCESS",len(recovered),"video assets",sum(bool(x["gif"]) for x in recovered),"GIF excerpts",flush=True)

if __name__=="__main__":main()
