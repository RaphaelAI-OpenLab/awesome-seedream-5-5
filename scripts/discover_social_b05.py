#!/usr/bin/env python3
import json,urllib.parse,urllib.request
def get(url):
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; SocialSeedreamResearch/1.0)","Accept":"application/json"})
 with urllib.request.urlopen(req,timeout=22) as r:return json.loads(r.read(3000000))
posts=[("xiaohu","2119774478788141417"),("larklee5","2119985661939974450"),("Sjonkerr","2119904922703438173"),("opener_ai","2119942433412931907"),("VORTEX_Promos","2119928374235701452")]
for handle,num in posts:
 try:
  j=get("https://api.fxtwitter.com/"+handle+"/status/"+num).get("tweet") or {}
  media=j.get("media") or {}
  print("XPOST",json.dumps({"url":j.get("url"),"text":(j.get("text") or "")[:1250],"media":media.get("all") or media.get("videos") or [],"photos":media.get("photos") or [],"author":(j.get("author") or {}).get("screen_name")},ensure_ascii=False),flush=True)
 except Exception as e:print("XERROR",handle,num,str(e)[:260],flush=True)
for q in ["Seedream 5.5","Seedream5.5","seedream5_5"]:
 try:
  url="https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?"+urllib.parse.urlencode({"q":q,"limit":100,"sort":"latest"})
  d=get(url)
  entries=[]
  for o in d.get("posts",[]):
   images=(o.get("embed") or {}).get("images") or []
   rec=o.get("record") or {}
   images2=(rec.get("embed") or {}).get("images") or []
   author=o.get("author") or {}
   entries.append({"uri":o.get("uri"),"handle":author.get("handle"),"did":author.get("did"),"text":(rec.get("text") or "")[:450],"createdAt":rec.get("createdAt"),"image_count":len(images),"images":[{"fullsize":x.get("fullsize"),"alt":(x.get("alt") or "")[:120]} for x in images[:6]],"record_image_count":len(images2)})
  print("BLUESKY",q,json.dumps(entries,ensure_ascii=False),flush=True)
 except Exception as e:print("BERROR",q,str(e)[:250],flush=True)
for url in ["https://www.reddit.com/search.json?q=%22Seedream%205.5%22&sort=new&limit=25","https://www.reddit.com/r/StableDiffusion/search.json?q=Seedream%205.5&restrict_sr=1&sort=new&limit=25"]:
 try:
  d=get(url)
  entries=[{"title":x["data"].get("title"),"permalink":x["data"].get("permalink"),"created":x["data"].get("created_utc"),"preview":bool(x["data"].get("preview")),"selftext":(x["data"].get("selftext") or "")[:180]} for x in (d.get("data") or {}).get("children",[])]
  print("REDDIT",json.dumps(entries,ensure_ascii=False),flush=True)
 except Exception as e:print("REDDITERROR",str(e)[:250],flush=True)
