#!/usr/bin/env python3
"""Restore creator-authored full prompts from the actual public X post body."""
import hashlib,json,re,subprocess,time
from pathlib import Path
from urllib.request import Request,urlopen
root=Path(__file__).resolve().parents[1]
cases_path=root/"content/cases.json"
audit_path=root/"docs/social-x-batch04-audit.json"
specs={
 "socialx-window-light-portrait":("nima2qisi2","2119983938383106432","Seedream 5.5👇\n",None),
 "socialx-glass-jellyfish-lamp":("ahmetmertugrul","2119920477535719739","RGBA + partial transparency\n\n","\n\n@dreamina_ai"),
 "socialx-deep-sea-field-guide":("ahmetmertugrul","2119915956365369596","#dreaminacpp \n\n",None),
 "socialx-blue-hour-fisherman":("ahmetmertugrul","2119922071916757233","#dreaminacpp\n\n",None),
}

def get_post(user,pid):
 last=None
 for retry in range(3):
  try:
   req=Request(f"https://api.fxtwitter.com/{user}/status/{pid}",headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
   with urlopen(req,timeout=25) as r: data=json.loads(r.read(1000000))
   tweet=data.get("tweet") or {}
   if not tweet.get("text"): raise ValueError("no text")
   return tweet
  except Exception as e:
   last=e
   time.sleep(1+retry)
 raise RuntimeError(str(last))

def main():
 cases=json.loads(cases_path.read_text())
 byid={c["id"]:c for c in cases}
 records=[]
 for caseid,(user,pid,start,end) in specs.items():
  tweet=get_post(user,pid)
  author=(tweet.get("author") or {}).get("screen_name") or ""
  if author.lower()!=user.lower(): raise ValueError("Author mismatch "+caseid)
  body=tweet["text"]
  if start not in body: raise ValueError("start marker missing "+caseid)
  prompt=body.split(start,1)[1]
  if end is not None:
   if end not in prompt: raise ValueError("end marker missing "+caseid)
   prompt=prompt.split(end,1)[0]
  prompt=prompt.strip()
  if not (90<=len(prompt)<4000): raise ValueError("implausible prompt size "+caseid)
  if re.search(r"https?://",prompt): raise ValueError("unexpected URL inside prompt")
  case=byid[caseid]
  if case["source_url"]!=f"https://x.com/{user}/status/{pid}":
   raise ValueError("case/post mismatch")
  case["prompt"]={"status":"original","url":case["source_url"],"text":prompt}
  records.append({"id":caseid,"characters":len(prompt),
                  "source_url":case["source_url"],
                  "prompt_sha256":hashlib.sha256(prompt.encode()).hexdigest(),
                  "extraction":"exact author-post text segment"})
  print("PROMPT VERIFIED",caseid,len(prompt),flush=True)
 partial=byid["socialx-transparent-character"]
 if partial["prompt"]["status"]=="not-published":
  partial["prompt"]["status"]="source-linked"
  partial["caveat"]["zh-CN"]+=" 原帖公开了透明背景提示词后缀，但未提供完整身份设定指令。"
  partial["caveat"]["en"]+=" The author shared the transparency prompt suffix, not the entire base identity prompt."
 cases_path.write_text(json.dumps(cases,ensure_ascii=False,indent=2)+"\n")
 audit=json.loads(audit_path.read_text())
 audit["source_post_exact_prompts"]=records
 audit_path.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n")
 subprocess.run(["python3","scripts/build.py"],cwd=root,check=True)
 subprocess.run(["python3","scripts/validate.py"],cwd=root,check=True)
 print("SOURCE PROMPTS SUCCESS",len(records),flush=True)

if __name__=="__main__":main()
