#!/usr/bin/env python3
"""Hash and provenance checks for the separate web-reference queue."""
import hashlib,json,re
from urllib.parse import urlsplit
from build_external_refs import ROOT,DIR,ZH,outputs
def must(x,msg):
    if not x:raise ValueError(msg)
def https(x):
    u=urlsplit(x);return u.scheme=="https" and bool(u.netloc) and not u.username and not u.password
def main():
    cases=json.loads((DIR/"cases.json").read_text())["cases"]
    checks=json.loads((DIR/"media-check.json").read_text())["items"]
    byfile={x["preview"]:x for x in checks}
    main_cases=json.loads((ROOT/"content/cases.json").read_text())
    existing={x["source_url"] for x in main_cases}
    ids=set();sourcefiles=set();previews=set()
    for c in cases:
        id=c["id"]
        must(re.fullmatch(r"web-[a-z0-9-]+",id),"unsafe ID "+id)
        must(id not in ids,"duplicate ID "+id);ids.add(id)
        must(c["category"] in ZH,"bad category "+id)
        must(c["model"]=="Seedream 5.5" and c["model_evidence"]=="site-self-reported","bad model evidence "+id)
        must(https(c["source_url"]) and c["source_url"] not in existing,"source invalid or main duplicate "+id)
        must(c["counted_in_main"] is False,"external counted as main "+id)
        must(c["prompt"]["status"]=="source-exact" and len(c["prompt"]["text"])>=45 and https(c["prompt"]["url"]),"missing source prompt "+id)
        must(c["rights"]["republication_license"] in ("not verified","verified","restricted"),"invalid rights status "+id)
        must(c["remake"]["status"] in ("pending","recreated","published"),"bad remake state "+id)
        for step in c.get("steps",[]):must(len(step["prompt"])>=25,"invalid edit instruction "+id)
        must(c["media"],"missing media "+id)
        for m in c["media"]:
            must(https(m["url"]),"invalid media URL "+id)
            must(m["url"] not in sourcefiles,"duplicate source image "+id);sourcefiles.add(m["url"])
            if m.get("preview"):
                p=m["preview"]
                must(re.fullmatch(r"previews/web-[a-z0-9-]+-\d{2}\.jpg",p),"invalid preview path "+p)
                must(p not in previews and p in byfile,"duplicate or missing preview check "+p);previews.add(p)
                raw=(DIR/p).read_bytes()
                must(raw[:3]==b"\xff\xd8\xff" and raw[-2:]==b"\xff\xd9","bad JPEG "+p)
                must(1000<=len(raw)<320000,"preview size "+p)
                record=byfile[p]
                must(len(raw)==record["bytes"] and hashlib.sha256(raw).hexdigest()==record["sha256"],"hash mismatch "+p)
                must(record["width"]>0 and record["height"]>0,"bad dimensions "+p)
    must(set(byfile)==previews,"stale preview audit entries")
    for path,content in outputs().items():
        must(path.is_file() and path.read_text()==content,"outdated generated page "+str(path))
    print("External reference validation OK:",len(cases),"cases,",len(previews),"low-resolution previews")
if __name__=="__main__":main()
