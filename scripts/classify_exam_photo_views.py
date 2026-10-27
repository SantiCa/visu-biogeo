"""Explicit visual assessment of the frozen priority set; no automatic inference."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];batch=R/'tmp/reviews/exam-photo-use'
diagnostic={6,7,8,9,12,13,22,23,24,25,28,29,32,33,36,37,44,45,48,49,50,51,52,53,58,59,70,71,78,79,80,81,82,83,84,85,86,87,88,89,90,91,98,99,100,101,102,103,112,113,118,119,126,127,134,135,138,139,140,141,144,145,146,147,148,149,152,153,154,155,158,159,168,169,180,181,182,183,186,187,188,189,190,191,194,195,204,205,206,207,220,221,222,223,234,235,236,237,238,239,256,257,260,261,264,265,276,277,280,281,284,285,292,293,296,297,306,307,310,311,312,313,314,315,316,317,322,323,
 3,10,26,40,42,46,61,68,73,74,76,77,115,124,125,164,167,199,218,228,231,232,243,244,258,272,274,290,318}
detail={2,4,5,11,43,54,55,63,66,67,69,72,75,179,211,229,230,242,246,247,248,249,251,259,262,263,270,271,273,275,278,279,291,298,299}
context={18,41,97,178,252,253,267,300}
assert not (diagnostic&detail or diagnostic&context or detail&context)
p=R/'data/curated-images.json';cur=json.loads(p.read_text(encoding='utf8'));picks=json.loads((batch/'picks.json').read_text(encoding='utf8'));log=[]
for i,pick in enumerate(picks):
 use='diagnostic' if i in diagnostic else 'detail' if i in detail else 'context' if i in context else 'insufficient'
 im=next(im for im in cur[pick['id']]['images'] if im['url']==pick['url'] and im['status']=='approved')
 im.update(examUse=use,examUseCheckedAt='2026-10-26',examUseNote='Revisión visual del encuadre y de los rasgos visibles para la resolución nominal de esta entrada. No basta la identificación de la fuente; se separan partes aisladas y vistas insuficientes. Lote exam-photo-use, índice '+str(i)+'.')
 log.append({'index':i,**pick,'use':use})
p.write_text(json.dumps(cur,ensure_ascii=False,indent=2),encoding='utf8')
report={'date':'2026-10-26','assessed':len(picks),'diagnosticViews':len(diagnostic),'isolatedDetails':len(detail),'context':len(context),'insufficientViews':len(picks)-len(diagnostic|detail|context),'andaluciaPairs':sum(sum(im.get('examUse')=='diagnostic' for im in row['images'] if im['status']=='approved')>=2 for row in cur.values()),'decisions':log,'scope':'Elegibilidad fotográfica para estudiar, independiente del estado de aprobación. Andalucía exige dos vistas diagnósticas; no se rellenan huecos con fotos sin evaluar. Madrid puede presentar detalles sin añadir una vista completa como pista.'}
(R/'data/exam-photo-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in report.items() if k not in ['decisions','scope']}))
