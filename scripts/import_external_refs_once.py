#!/usr/bin/env python3
"""One-time fetch of small web-gallery reference previews; never save the source originals."""
import hashlib,io,json,time
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request,urlopen
from PIL import Image,ImageOps,UnidentifiedImageError
from build_external_refs import ROOT,DIR,outputs
MAX_BYTES=14_000_000
HOSTS={"vdobloom.com","www.made.app","r2.flux1.ai","aws.seedreamv5.com","cdn.froging.ai","cdn.orylia.ai"}
def get(url):
    u=urlsplit(url)
    if u.scheme!="https" or u.hostname not in HOSTS:
        raise ValueError("Unapproved web media origin: "+url)
    last=None
    for i in range(3):
        try:
            req=Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; ReferencePreviewAudit/1.0)","Accept":"image/avif,image/webp,image/png,image/jpeg,image/*"})
            with urlopen(req,timeout=28) as response:
                final=urlsplit(response.geturl())
                if final.scheme!="https" or final.hostname not in HOSTS:
                    raise ValueError("Unexpected media redirect: "+str(final.hostname))
                result=response.read(MAX_BYTES+1)
                ctype=response.headers.get("Content-Type") or ""
                if len(result)<1024 or len(result)>MAX_BYTES:raise ValueError("Unexpected media size")
                if "text/html" in ctype:raise ValueError("Received HTML instead of image")
                return result,response.geturl()
        except Exception as e:
            last=e;time.sleep(1+i)
    raise RuntimeError(str(last))
def make_jpg(raw):
    Image.MAX_IMAGE_PIXELS=60_000_000
    with Image.open(io.BytesIO(raw)) as source:
        if source.format not in ("PNG","JPEG","WEBP"):
            raise ValueError("Unsupported image codec "+str(source.format))
        img=ImageOps.exif_transpose(source)
        if "A" in img.getbands():
            base=Image.new("RGB",img.size,(247,247,247))
            base.paste(img,mask=img.getchannel("A"))
            img=base
        else:img=img.convert("RGB")
        img.thumbnail((440,440),Image.Resampling.LANCZOS)
        buf=io.BytesIO()
        img.save(buf,"JPEG",quality=68,optimize=True)
        jpeg=buf.getvalue()
        if not (1000<len(jpeg)<320000):raise ValueError("Low-res preview outside expected size limit")
        with Image.open(io.BytesIO(jpeg)) as inspect:inspect.verify()
        return jpeg,img.width,img.height
def main():
    path=DIR/"cases.json"
    root=json.loads(path.read_text(encoding="utf-8"))
    checks=[]
    report=[]
    ok=0;misses=0
    (DIR/"previews").mkdir(exist_ok=True,parents=True)
    for item in root["cases"]:
        for n,m in enumerate(item["media"],1):
            name="previews/"+item["id"]+"-"+f"{n:02d}"+".jpg"
            if m.get("preview") and (DIR/m["preview"]).exists():
                print("SKIP saved",name,flush=True)
                continue
            urls=[m["url"]]
            if m.get("alternative_url") and m["alternative_url"] not in urls:
                urls.append(m["alternative_url"])
            image=None;error=""
            for source_url in urls:
                try:
                    raw,actual=get(source_url)
                    jpeg,w,h=make_jpg(raw)
                    image=(raw,jpeg,w,h,actual)
                    break
                except Exception as exc:
                    error=str(exc)
            if image is None:
                misses+=1
                report.append({"id":item["id"],"source_media":m["url"],"status":"source-only","error":error[:250]})
                print("SOURCE ONLY",item["id"],n,error[:100],flush=True)
                continue
            raw,jpg,w,h,actual=image
            (DIR/name).write_bytes(jpg)
            m["preview"]=name
            m["preview_transform"]="source-web-image-resized-to-440px-low-quality-jpeg"
            m["source_sha256"]=hashlib.sha256(raw).hexdigest()
            m["downloaded_from"]=actual
            checks.append({"preview":name,"sha256":hashlib.sha256(jpg).hexdigest(),
                           "bytes":len(jpg),"width":w,"height":h,
                           "source_sha256":m["source_sha256"]})
            report.append({"id":item["id"],"source_media":m["url"],"status":"saved-low-res-preview",
                           "preview":name,"width":w,"height":h,
                           "source_sha256":m["source_sha256"]})
            ok+=1
            print("SAVED",item["id"],n,len(jpg),w,h,flush=True)
    if ok<16:raise RuntimeError("Too few web-media previews fetched: "+str(ok)+"; errors "+str(misses))
    path.write_text(json.dumps(root,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (DIR/"media-check.json").write_text(json.dumps({"checked_at":"2026-11-11","items":checks},indent=2,ensure_ascii=False)+"\n")
    (DIR/"source-audit.json").write_text(json.dumps({"checked_at":"2026-11-11",
      "cases":len(root["cases"]),"saved_previews":ok,"source_only":misses,
      "source_rights":"all unverified — not cleared for public image reuse",
      "download_mode":"compressed 440px reference thumbnail only","entries":report},ensure_ascii=False,indent=2)+"\n")
    from build_external_refs import main as build_external
    import subprocess
    subprocess.run(["python3","scripts/build_external_refs.py"],cwd=ROOT,check=True)
    subprocess.run(["python3","scripts/build.py"],cwd=ROOT,check=True)
    subprocess.run(["python3","scripts/validate_external_refs.py"],cwd=ROOT,check=True)
    subprocess.run(["python3","scripts/validate.py"],cwd=ROOT,check=True)
    print("COMPLETE",len(root["cases"]),"references",ok,"previews",misses,"source-only",flush=True)
if __name__=="__main__":main()
