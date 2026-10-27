import json
from build_learning_geology import fetch_handbook,D
def main():
 p=D/'learning-geology.json';data=json.loads(p.read_text(encoding='utf8'));links={'apatito':['fluorapatite'],'baritina':['baryte'],'crisotilo':['clinochrysotile'],'carborundo':['Moissanite'],'espinela':['Spinel'],'azufre':['sulphur'],'wolframita':['ferberite','hubnerite']}
 for id,slugs in links.items():
  if id not in data:continue
  for slug in slugs:
   _,ok=fetch_handbook(slug)
   if not ok:print('Reference unavailable',id,slug,flush=True);continue
   url='https://handbookofmineralogy.org/pdfs/'+slug+'.pdf'
   if not any(s['url']==url for s in data[id]['sources']):data[id]['sources'].append({'url':url,'title':'Handbook of Mineralogy · '+slug+(' · miembro del grupo' if id in ['apatito','wolframita'] else '')})
  print(id,len(data[id]['sources']),'references',flush=True)
 opal={'url':'https://www.gia.edu/gia-website/opal','title':'Gemological Institute of America · sílice hidratada y fórmula general'}
 if not any(s['url']==opal['url'] for s in data['opalo']['sources']):data['opalo']['sources'].append(opal)
 data['carborundo']['description']='Carborundo es el nombre habitual del carburo de silicio sintético. Su análogo mineral natural es la moissanita. Se conserva entre los materiales del listado, explicitando su origen sintético habitual.'
 for id,r in data.items():
  if r.get('representation') and r.get('parentMaterialId') in data:r['sources']=data[r['parentMaterialId']]['sources']
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
