"""Evidence for original paraphrases, not text to paste into study cards."""
from pathlib import Path
from urllib.parse import quote
import json
from collect_teaching import soup
ROOT=Path(__file__).resolve().parents[1]
TERMS='adenina citosina guanina timina uracilo adenosina caroteno clorofila colesterol esfingosina fructosa gliceraldehido glucosa testosterona isopreno lactosa nicotinamida prostaglandina sacarosa retinol tiamina cobalamina riboflavina niacina pantotenico-ca piridoxina biotina folico-ca ascorbico-ca calciferol tocoferol fitomenadiona pegmatita obsidiana riolita eclogita'.split()
def main():
    out={}
    for term in TERMS:
        url='https://dicciomed.usal.es/palabra/'+quote(term)
        try:
            s=soup(url);text=s.get_text(' ',strip=True);start=text.find('Palabra ')
            excerpt=text[start:start+1000] if start>=0 else text[:300]
            out[term]={'source':url,'excerpt':excerpt};print(term,excerpt[:600],flush=True)
        except Exception as e:print(term,type(e).__name__,str(e),flush=True)
    (ROOT/'tmp/etymology-evidence-chemistry.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
