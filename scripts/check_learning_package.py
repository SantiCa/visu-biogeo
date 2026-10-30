from pathlib import Path
import json,zipfile,hashlib
from prepare_release import ROOT,public_files
def main():
 files=public_files();bad=[]
 with zipfile.ZipFile(ROOT/'output/windows-installer/payload.zip') as archive:
  names=set(archive.namelist())
  for relative in files:
   packaged='app/'+relative
   if packaged not in names or hashlib.sha256(archive.read(packaged)).digest()!=hashlib.sha256((ROOT/relative).read_bytes()).digest():bad.append(relative)
  if hashlib.sha256(archive.read('Visu BioGeo.exe')).digest()!=hashlib.sha256((ROOT/'Abrir Visu BioGeo.exe').read_bytes()).digest():bad.append('Visu BioGeo.exe')
  forbidden=[n for n in names if n.lower().endswith('.pdf') or '/tmp/' in n or '/supabase/' in n]
 report={'version':(ROOT/'output/windows-installer/version.txt').read_text(),'filesChecked':len(files),'mismatches':bad,'forbiddenFiles':forbidden,'learningModuleIncluded':'classification-learning.mjs' in files,'learningTaxonomyIncluded':'data/learning-taxonomy.json' in files,'learningGeologyIncluded':'data/learning-geology.json' in files,'serviceWorkerIncluded':'sw.js' in files,'treeGuideIncluded':'taxonomy-guide.mjs' in files,'taxonReferenceIncluded':'taxon-reference.mjs' in files,'examPhotoRulesIncluded':'exam-photos.mjs' in files}
 (ROOT/'output/package-check-v8.13.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report));assert not bad and not forbidden
if __name__=='__main__':main()
