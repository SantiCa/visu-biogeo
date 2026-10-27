from pathlib import Path
from bs4 import BeautifulSoup
import urllib.request,json
R=Path(__file__).resolve().parents[1];OUT=R/'tmp/nps-zero-oct26';OUT.mkdir(exist_ok=True)
URLS={
'glacial-gallery':'https://npgallery.nps.gov/SearchResults/albumid/915ccd1d-b609-4c34-9364-0b3f83301c66',
'cave-speleothems':'https://www.nps.gov/subjects/caves/speleothems.htm',
'cave-jewel':'https://home.nps.gov/jeca/formations-of-jewel-cave.htm',
'cave-mammoth':'https://home.nps.gov/maca/learn/nature/stalactites-stalagmites-and-cave-formations.htm',
'glacial-peaks':'https://www.nps.gov/articles/nunataksareteshorns.htm',
'rivers':'https://www.nps.gov/subjects/geology/fluvial-landforms.htm'}
def main():
 result={}
 for name,url in URLS.items():
  p=OUT/(name+'.html')
  try:
   if not p.exists():p.write_bytes(urllib.request.urlopen(url,timeout=40).read())
   soup=BeautifulSoup(p.read_bytes(),'html.parser');images=[]
   for im in soup.find_all('img'):
    parent=im.find_parent('figure') or im.parent.parent
    if im.get('alt') or 'AssetDetail' in str(parent):images.append({'src':im.get('src'),'alt':im.get('alt'),'context':parent.get_text(' ',strip=True)[:750],'link':im.find_parent('a').get('href') if im.find_parent('a') else None})
   result[name]={'url':url,'images':images,'links':[{'href':a['href'],'text':a.get_text(' ',strip=True)[:200]} for a in soup.select('a[href]') if 'AssetDetail' in a['href']]};print(name,json.dumps(result[name],ensure_ascii=False)[:14000],flush=True)
  except Exception as e:print(name,str(e),flush=True)
 (OUT/'index.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
