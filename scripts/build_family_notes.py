"""Document the nomenclatural construction, without inventing a deeper Greek/Latin story."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data'
TYPES={'Pinaceae':'Pinus','Saturniidae':'Saturnia','Pteridaceae':'Pteris','Boraginaceae':'Borago','Cannabaceae':'Cannabis','Fabaceae':'Faba','Arecaceae':'Areca','Cistaceae':'Cistus','Paridae':'Parus','Ephedraceae':'Ephedra','Forficulidae':'Forficula','Liliaceae':'Lilium','Asteraceae':'Aster','Cupressaceae':'Cupressus','Lycopodiaceae':'Lycopodium','Agaricaceae':'Agaricus','Mantidae':'Mantis','Marchantiaceae':'Marchantia','Osmundaceae':'Osmunda','Anatidae':'Anas','Amaryllidaceae':'Amaryllis','Polypodiaceae':'Polypodium','Salicaceae':'Salix','Rosaceae':'Rosa','Lythraceae':'Lythrum','Fagaceae':'Fagus','Lamiaceae':'Lamium','Poaceae':'Poa','Taxaceae':'Taxus','Upupidae':'Upupa','Xiphiidae':'Xiphias','Papilionidae':'Papilio','Caryophyllaceae':'Caryophyllus','Berberidaceae':'Berberis','Triviidae':'Trivia','Pectinidae':'Pecten','Pentatomidae':'Pentatoma','Naticidae':'Natica','Tamaricaceae':'Tamarix','Isoetaceae':'Isoetes','Viverridae':'Viverra','Empusidae':'Empusa','Asparagaceae':'Asparagus','Primulaceae':'Primula','Brassicaceae':'Brassica','Apiaceae':'Apium','Dryopteridaceae':'Dryopteris','Scrophulariaceae':'Scrophularia','Solanaceae':'Solanum','Ranunculaceae':'Ranunculus','Rubiaceae':'Rubia','Nectriaceae':'Nectria','Tettigoniidae':'Tettigonia','Tenebrionidae':'Tenebrio','Geastraceae':'Geastrum','Sycettidae':'Sycetta','Gelidiaceae':'Gelidium','Cutleriaceae':'Cutleria'}
def main():
    out={}
    for family,genus in TYPES.items():
        botanical=family.endswith('aceae');suffix='-aceae' if botanical else '-idae'
        out[family]={'etymology':f'Deriva del nombre genérico {genus}, con la terminación {suffix} de familia. El origen lingüístico más remoto del género queda pendiente cuando no hay una referencia contrastada.','typeGenus':genus,'sources':[{'url':'https://iapt-taxon.org/melbourne/main.php?page=art18' if botanical else 'https://code.iczn.org/formation-and-treatment-of-names/article-29-family-group-names','title':'Formación de nombres de familia: código botánico' if botanical else 'Formación de nombres de familia: ICZN, art. 29'}],'reviewedAt':'2026-10-25'}
    roots={
        'Asteraceae':('Aster procede del griego que significa «estrella».','https://www.asturnatura.com/genero/aster'),
        'Cistaceae':('Cistus procede del antiguo nombre griego de las jaras; su relación con «cesta» es una interpretación histórica.','https://www.asturnatura.com/especie/cistus-albidus'),
        'Lycopodiaceae':('Lycopodium combina raíces griegas para «lobo» y «piececito», por una comparación de sus ramillas.','https://www.asturnatura.com/especie/lycopodium-clavatum'),
        'Taxaceae':('Taxus es el nombre latino del tejo.','https://www.asturnatura.com/especie/taxus-baccata')}
    for family,(explanation,url) in roots.items():
        out[family]['etymology']=f"Se forma a partir de {TYPES[family]} y la terminación -aceae de familia. {explanation}"
        out[family]['sources'].append({'url':url,'title':'Asturnatura: raíz del nombre genérico'})
    (D/'family-notes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(len(out),'familias con formación nomenclatural documentada')
if __name__=='__main__':main()
