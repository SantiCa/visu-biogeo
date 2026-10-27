from pathlib import Path
import json,re
from collections import Counter
from build_learning_taxonomy import CACHE,D,save
def main():
 t=json.loads((D/'learning-taxonomy.json').read_text(encoding='utf8'));g=json.loads((D/'learning-geology.json').read_text(encoding='utf8'));catalog=json.loads((D/'species.json').read_text(encoding='utf8'));photos=json.loads((D/'inaturalist-images.json').read_text(encoding='utf8'))
 added=0;locales=Counter()
 for item in catalog:
  id=item['id'];path=CACHE/(str(photos.get(id,{}).get('taxonId'))+'.json')
  if id not in t or not path.exists():continue
  raw=json.loads(path.read_text(encoding='utf8'));names=[n for n in raw.get('names',[]) if ((n.get('locale') or '').startswith('es') or (n.get('lexicon') or '').lower()=='spanish') and n.get('is_valid',True)]
  locales.update((n.get('locale'),n.get('lexicon')) for n in names)
  if not t[id].get('commonName') and names:t[id]['commonName']=names[0]['name'];t[id]['commonNames']=[n['name'] for n in names];t[id]['commonNameStatus']='documented';added+=1
 for id,r in g.items():
  if r['domain']!='mineral' or not r.get('scheme'):continue
  group=r['path'][1];base=r['classification'];aliases=[]
  if base=='Óxidos e hidróxidos':aliases=['Hidróxidos','Oxihidróxidos'] if 'hidróxido' in group.lower() else ['Óxidos']
  elif base=='Fosfatos, arseniatos y vanadatos':aliases=['Vanadatos'] if 'Vanadato' in group else ['Arseniatos','Arsenatos'] if 'Arseniato' in group or 'Arsenato' in group else ['Fosfatos']
  elif base=='Sulfatos y afines':aliases=['Wolframatos'] if 'Wolframato' in group else ['Sulfatos']
  elif base=='Elementos nativos y afines':aliases=['Elementos nativos']
  elif base=='Carbonatos y nitratos':aliases=['Carbonatos']
  elif base=='Sulfuros y sulfosales':aliases=['Sulfuros','Sulfuros y sulfosales']
  r['classificationAliases']=aliases
  # Variable compositions are studied as such; no numerical single-member answer is invented.
  formula=r.get('formula','');r['formulaQuiz']=bool(re.fullmatch(r'[A-Za-z0-9(),·.]+',formula) and not any(c in formula for c in ['x','n']))
  prefix='La fórmula general incluye las sustituciones indicadas entre paréntesis; la composición concreta depende de la muestra. '
  if r['formulaQuiz'] and r.get('formulaKind')=='general-or-variable' and not r['description'].startswith(prefix):r['description']=prefix+r['description']
  if id in ['sulfato-de-cobre','lazurita','lepidolita']:r['formulaQuiz']=False
 save(D/'learning-taxonomy.json',t);save(D/'learning-geology.json',g)
 print(json.dumps({'additionalSpanishNames':added,'spanishLocales':{str(k):v for k,v in locales.items()},'quizMinerals':sum(r.get('formulaQuiz',False) for id,r in g.items() if any(x['id']==id and x['kind']=='mineral' for x in catalog))},ensure_ascii=False))
if __name__=='__main__':main()
