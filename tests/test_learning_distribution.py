import unittest,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from prepare_release import public_files
class LearningDistribution(unittest.TestCase):
 def test_essential_learning_resources_ship_and_native_server_allows_them(self):
  files=public_files();native=(ROOT/'desktop/VisuBioGeo.cs').read_text(encoding='utf8')
  for name in ['classification-learning.mjs','taxonomy-guide.mjs','taxon-reference.mjs','exam-photos.mjs','data/learning-taxonomy.json','data/learning-geology.json','sw.js']:
   self.assertIn(name,files);self.assertIn('"'+Path(name).name+'"',native);self.assertTrue((ROOT/name).is_file())
  self.assertFalse(any(name.endswith('.pdf') for name in files))
 def test_biological_coverage_distinguishes_unresolved_and_inapplicable(self):
  taxonomy=json.loads((ROOT/'data/learning-taxonomy.json').read_text(encoding='utf8'));audit=json.loads((ROOT/'data/learning-taxonomy-audit.json').read_text(encoding='utf8'))
  self.assertTrue(set(audit['notApplicableIds']).isdisjoint(audit['pendingIds']))
  for t in taxonomy.values():self.assertFalse(any(n.startswith('NO_') for n in t.get('ranks',{}).values()))
if __name__=='__main__':unittest.main()
