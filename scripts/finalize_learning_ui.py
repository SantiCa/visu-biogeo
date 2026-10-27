from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
p=R/'app.js';s=p.read_text(encoding='utf8');s=s.replace("esc(RANK_LABELS[n.rank]||", "esc(n.label||RANK_LABELS[n.rank]||")
s=s.replace("const t=learningTaxonomy[item.id],g=learningGeology[item.id];if(g)","const t=learningTaxonomy[item.id],g=learningGeology[item.id];if(t?.nonTaxonomic)return '<section class=\"taxonomy-summary\"><h3>Estructura biogénica</h3><p>'+esc(t.reviewNote)+'</p></section>';if(g)")
p.write_text(s,encoding='utf8')
p=R/'data/learning-taxonomy.json';t=json.loads(p.read_text(encoding='utf8'));catalog=json.loads((R/'data/species.json').read_text(encoding='utf8'))
for r in t.values():
 r['ranks']={k:v for k,v in r.get('ranks',{}).items() if not v.startswith('NO_')};r['hierarchy']=[x for x in r.get('hierarchy',[]) if not x['name'].startswith('NO_')]
p.write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf8')
bio=[i for i in catalog if i['kind'] in ['organismo','fosil']];audit={'date':'2026-10-26','biologicalEntries':len(bio),'rankedPhyla':sum(bool(t[i['id']]['ranks'].get('phylum')) for i in bio),'commonNames':sum(bool(t[i['id']].get('commonName')) for i in bio),'notApplicableIds':[i['id'] for i in bio if t[i['id']].get('nonTaxonomic')],'pendingIds':[i['id'] for i in bio if not t[i['id']]['ranks'].get('phylum') and not t[i['id']].get('nonTaxonomic')]};(R/'data/learning-taxonomy-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(audit))
p=R/'tooltips.mjs';s=p.read_text(encoding='utf8').replace("catalog:'el catálogo y la lectura libre',", "catalog:'el catálogo y la lectura libre',classification:'los árboles de taxonomía, minerales y rocas',");p.write_text(s,encoding='utf8')
p=R/'scripts/build_installer.py';s=p.read_text(encoding='utf8').replace("version='7.2-'","version='8.0-'");p.write_text(s,encoding='utf8')
print('UI refinements applied')
