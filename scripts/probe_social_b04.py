#!/usr/bin/env python3
import json
from urllib.request import Request,urlopen
posts=[('94vanAI','2119938579078238370'),('dongxi_nlp','2120031669893939524'),('ahmetmertugrul','2119920477535719739')]
for handle,post in posts:
  for name,url in [('syndication',f'https://cdn.syndication.twimg.com/tweet-result?id={post}&lang=en&token=0'),('fx',f'https://api.fxtwitter.com/{handle}/status/{post}')]:
    try:
      req=Request(url,headers={'User-Agent':'Mozilla/5.0','Accept':'application/json'})
      with urlopen(req,timeout=18) as r: data=json.loads(r.read(1000000).decode());status=r.status
      tweet=data.get('tweet',data)
      photos=tweet.get('photos') or tweet.get('media',{}).get('photos') or []
      media=tweet.get('media')
      print('PROBE',name,post,'http',status,'top_keys',list(data.keys())[:20],'media',str(media)[:400],'photos',str(photos)[:1200],'text',str(tweet.get('text') or tweet.get('full_text'))[:450],flush=True)
    except Exception as exc:
      print('PROBE ERROR',name,post,type(exc).__name__,str(exc)[:200],flush=True)
