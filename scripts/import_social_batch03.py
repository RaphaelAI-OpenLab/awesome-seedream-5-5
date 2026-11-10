#!/usr/bin/env python3
import json,hashlib,io,time,subprocess
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlsplit
from PIL import Image,ImageOps
root=Path(__file__).resolve().parents[1]

def download(url):
 p=urlsplit(url)
 assert p.scheme=="https" and p.netloc=="cdn.beatapi.io" and p.path.startswith("/prompt-gallery/seedream-5-5/")
 for retry in range(3):
  try:
   with urlopen(Request(url,headers={"User-Agent":"Mozilla/5.0","Accept":"image/*"}),timeout=30) as r:
    b=r.read(12000001)
   if not (1024<len(b)<=12000000): raise ValueError("size")
   return b
  except Exception as e:
   print("download error",type(e).__name__,e,flush=True)
   time.sleep(2+retry*2)
 raise RuntimeError("unable to download "+url)

def thumbnail(blob):
 Image.MAX_IMAGE_PIXELS=30000000
 with Image.open(io.BytesIO(blob)) as source:
  if source.format not in ("JPEG","PNG","WEBP"): raise ValueError("format")
  img=ImageOps.exif_transpose(source)
  if "A" in img.getbands():
   bg=Image.new("RGB",img.size,"#f4f4f4")
   bg.paste(img,mask=img.getchannel("A"))
   img=bg
  else: img=img.convert("RGB")
  img.thumbnail((640,640),Image.Resampling.LANCZOS)
  output=io.BytesIO()
  img.save(output,"JPEG",quality=81,optimize=True)
  b=output.getvalue()
  if len(b)>=512000: raise ValueError("preview too big")
  return b,img.width,img.height

def main():
 items=json.loads((root/"content/social-image-batch03.json").read_text())["cases"]
 casefile=root/"content/cases.json"
 checkfile=root/"docs/media-check.json"
 cases=json.loads(casefile.read_text())
 report=json.loads(checkfile.read_text())
 ids={x["id"] for x in cases}
 existing={x["url"] for c in cases for x in c["media"]}
 bypath={r["preview"]:r for r in report["items"]}
 added=[]
 failed=[]
 for i in items:
  if i["id"] in ids or i["media_url"] in existing: continue
  print("fetching",i["id"],flush=True)
  try:
   original=download(i["media_url"])
   jpg,w,h=thumbnail(original)
  except Exception as e:
   failed.append({"id":i["id"],"error":str(e)})
   continue
  preview="assets/previews/"+i["id"]+".jpg"
  (root/preview).write_bytes(jpg)
  z="来自公开整理站的作者归因图片与提示词，未在本仓库独立复现。图像为缩小版，非原始导出。"
  e="Source-attributed social image and prompt from a public curator; not reproduced here. Reduced preview, not original export."
  if i["category"]=="rgba-assets":
   z+=" 这张 JPEG 不能证明原始 Alpha 透明度。"
   e+=" JPEG does not verify the source alpha channel."
  if i["id"]=="social-genel-japanese-deli":
   z+=" 此图是三模型比较拼图，Seedream 5.5 为左侧列。"
   e+=" This is a 3-model collage, with Seedream 5.5 at left."
  cases.append({"id":i["id"],"title":i["title"],"category":i["category"],"author":i["author"],
    "source_url":i["source_post_url"],"source_type":"creator-reported","model":"Seedream 5.5",
    "model_evidence":"creator-reported-via-prompt-and-media-mirror","checked_at":"2026-11-10",
    "reproduced":False,"prompt":{"status":"original","url":i["source_mirror_url"],"text":i["prompt"]},
    "caveat":{"zh-CN":z,"en":e},
    "media":[{"url":i["media_url"],"type":"image","rights":"rights-reserved",
              "delivery":"local-preview-with-source-link","preview":preview,
              "preview_transform":"curator-mirror-resized-jpeg-640"}]})
  bypath[preview]={"preview":preview,"status":"decoded-preview","bytes":len(jpg),
                   "sha256":hashlib.sha256(jpg).hexdigest(),"codec_name":"mjpeg","width":w,"height":h}
  added.append({"id":i["id"],"post":i["source_post_url"],"preview":preview,
                "mirror_sha256":hashlib.sha256(original).hexdigest()})
  print("saved",preview,w,h,flush=True)
 if len(added)<3: raise RuntimeError("Not enough downloaded images; "+str(failed))
 casefile.write_text(json.dumps(cases,indent=2,ensure_ascii=False)+"\n")
 report["items"]=sorted(bypath.values(),key=lambda x:x["preview"])
 checkfile.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
 (root/"docs/social-image-batch03-audit.json").write_text(json.dumps(
   {"date":"2026-11-10","source":"BeatAPI prompt gallery mirror",
    "note":"Preview was locally fetched and resized, but source exported original and rights clearance not independently established.",
    "added":added,"failed":failed},indent=2,ensure_ascii=False)+"\n")
 src=root/"docs/SOURCES.md"
 src.write_text(src.read_text().rstrip()+"\n\n## 第三批社媒 Prompt 与图片（2026-11-10）\n\n来源为 BeatAPI 的公开整理项目，其中关联了原 X 作者、完整 prompt 及镜像图片。本仓库实际保存了裁缩至640px内的 JPEG 预览，保留原帖与媒体链接。无法证明是原始未压缩文件或原生透明图，也不声称原作者授权转让版权。详情见 content/social-image-batch03.json 和 docs/social-image-batch03-audit.json。\n")
 build=root/"scripts/build.py"
 text=build.read_text().replace("以上为作者公开的原始指令，包含波兰语文案。没有执行复现。","以上为来源公开、归因于作者的提示词；本站未独立复现，请对照原作者帖文确认二次转录。").replace("The source author published this exact instruction, including the Polish copy. It has not been reproduced here.","The prompt is attributed to the creator by the source curator; no independent reproduction was performed.")
 build.write_text(text)
 subprocess.run(["python3","scripts/build.py"],cwd=root,check=True)
 subprocess.run(["python3","scripts/validate.py"],cwd=root,check=True)
 print("SUCCESS",len(added),"actual image previews",flush=True)
if __name__=="__main__": main()
