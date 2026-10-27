import json
from pathlib import Path
D=Path(__file__).resolve().parents[1]/'data'
def main():
 p=D/'study-notes.json';n=json.loads(p.read_text(encoding='utf8'))
 rows={
  'trichinella-spiralis':('Trichinella combina una raíz griega relacionada con el pelo con un diminutivo; spiralis alude a la forma enrollada. El nombre genérico sustituyó a Trichina porque este ya se había usado para un insecto.','https://wwwnc.cdc.gov/eid/article/27/12/21-1230_article'),
  'toxoplasma-gondii':('Toxoplasma alude a una forma arqueada, combinando raíces griegas para arco y algo formado o modelado. gondii remite al roedor en el que se describió el organismo, citado históricamente como Ctenodactylus gondii.','https://wwwnc.cdc.gov/eid/article/16/10/et-1610_article'),
  'plasmodium-falciparum':('Plasmodium deriva de una voz griega para algo formado o modelado. La derivación histórica del epíteto falciparum queda pendiente de contrastar con una referencia lingüística específica.','https://wwwnc.cdc.gov/eid/article/17/10/et-1710_article')}
 for id,(text,url) in rows.items():n[id]['etymology']=text;n[id]['sources'].append({'url':url,'title':'Emerging Infectious Diseases · etimología del nombre'});n[id]['etymologyReviewedAt']='2026-10-26'
 p.write_text(json.dumps(n,ensure_ascii=False,indent=2),encoding='utf8')
 print('2 binomial etymologies completed and 1 generic root documented')
if __name__=='__main__':main()
