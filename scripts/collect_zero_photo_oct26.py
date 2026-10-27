import json,urllib.error
from collect_commons_html import collect,PATH
def main():
 data=json.loads(PATH.read_text(encoding='utf8'))
 for id,category in [('diploctenium','Diploctenium fossils'),('turritella','Turritella fossils'),('productus','Productus fossils'),('gomphotherium','Gomphotherium fossils'),('aspidiscus-cristatus','Aspidiscus cristatus')]:
  try:result=collect(category,3)
  except urllib.error.HTTPError as e:
   if e.code==429:print('Commons rate limit; stopped',flush=True);break
   print(id,str(e),flush=True);continue
  except Exception as e:print(id,str(e),flush=True);continue
  old=data.get(id,{});existing=old.get('images',[]);seen={im['url'] for im in existing};result['images']=existing+[im for im in result['images'] if im['url'] not in seen];data[id]=result
  PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print(id,len(result['images']),flush=True)
if __name__=='__main__':main()
