#!/usr/bin/env python3
import json
from urllib.request import urlopen,Request
posts=[
("nima2qisi2","2119983938383106432"),
("ahmetmertugrul","2119920477535719739"),
("ahmetmertugrul","2119915956365369596"),
("ahmetmertugrul","2119922071916757233"),
("KakiponzuX","2119979776651710778")
]
for user,pid in posts:
 try:
  url=f"https://api.fxtwitter.com/{user}/status/{pid}"
  req=Request(url,headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
  with urlopen(req,timeout=25) as r: data=json.loads(r.read(500000))
  tweet=data.get("tweet") or {}
  print("SOURCE_TEXT",pid,json.dumps({"text":tweet.get("text"),"raw_text":tweet.get("raw_text"),"note_tweet":tweet.get("note_tweet"),"author":tweet.get("author",{}).get("screen_name")},ensure_ascii=False),flush=True)
 except Exception as e:
  print("PROBE ERROR",pid,str(e),flush=True)
