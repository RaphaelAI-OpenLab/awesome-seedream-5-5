#!/usr/bin/env python3
"""One-time public-site page structure inspection; saves text/asset metadata only."""
import json,re,time
from urllib.parse import urljoin
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup
from pathlib import Path
SOURCES=[
("vdobloom","https://vdobloom.com/blog/seedream-5-5-prompt-guide/"),
("made","https://www.made.app/models/seedream-5-5"),
("flux1","https://flux1.ai/seedream-5-5"),
("froging","https://www.froging.ai/seedream-5-5-ai-image-generator"),
("seedream-studio","https://seedreamv5.com/seedream-5.5"),
("orylia","https://orylia.ai/ai-models/seedream-5-5"),
("xiaohu-guide","https://xiaohu.ai/en/article/seedream-5-5-user-guide/"),
("insmind","https://www.insmind.com/blog/seedream-5-5-prompts"),
("spicyapi","https://spicyapi.ai/reviews/seedream-5-5"),
]
out=[]
for name,url in SOURCES:
    try:
        req=Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; open-source-source-audit/1.0)","Accept":"text/html,application/xhtml+xml"})
        with urlopen(req,timeout=25) as r:
            raw=r.read(3_500_000)
            if len(raw)>3_000_000:raise ValueError("too big")
            page=r.geturl()
        soup=BeautifulSoup(raw,"html.parser")
        for el in soup(["script","style","noscript"]):el.decompose()
        sections=[]
        headings=soup.find_all(["h1","h2","h3","h4"])
        for h in headings[:110]:
            title=h.get_text(" ",strip=True)[:140]
            txt=[]
            cursor=h
            # Collect sections by next document elements, excluding nested headers
            for nxt in h.next_elements:
                if nxt is h:continue
                if getattr(nxt,"name",None) in ("h1","h2","h3","h4"):
                    break
                if getattr(nxt,"name",None) in ("p","blockquote","pre","figcaption"):
                    t=nxt.get_text(" ",strip=True)
                    if t and (not txt or txt[-1]!=t):
                        txt.append(t[:1100])
                if len(txt)>=7:break
            images=[]
            for img in list(h.parent.find_all("img"))[:3]:
                src=img.get("src") or img.get("data-src") or ""
                images.append({"src":urljoin(page,src) if src else "", "alt":str(img.get("alt") or "")[:170]})
            sections.append({"title":title,"text":txt[:6],"images":images})
        all_imgs=[]
        for img in soup.find_all("img")[:80]:
            src=img.get("src") or img.get("data-src") or img.get("data-lazy-src") or ""
            if src and not src.startswith("data:"):
                all_imgs.append({"src":urljoin(page,src),"alt":str(img.get("alt") or "")[:130]})
        result={"name":name,"url":url,"final_url":page,"status":"ok","title":soup.title.get_text(" ",strip=True) if soup.title else "",
                "text_length":len(soup.get_text(" ",strip=True)),
                "heading_sections":sections[:75],"images":all_imgs[:60]}
        print("SITE",name,"ok","headings",len(sections),"images",len(all_imgs),flush=True)
    except Exception as e:
        result={"name":name,"url":url,"status":"error","error":str(e)[:350]}
        print("SITE",name,"error",str(e)[:220],flush=True)
    out.append(result)
Path("external-references").mkdir(exist_ok=True)
Path("external-references/.web-probe.json").write_text(json.dumps({"sources":out},ensure_ascii=False,indent=2)+"\n")
print("COMPLETE",sum(x["status"]=="ok" for x in out),flush=True)
