import unittest,json,copy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from import_madrid_compilation import apply_compilation
from prepare_release import public_files
def load(name):return json.loads((ROOT/'data'/name).read_text(encoding='utf8'))

class MadridCompilationTests(unittest.TestCase):
    def test_reimport_preserves_existing_state_and_is_idempotent(self):
        catalog,exams,evidence=[load(n) for n in ['species.json','exams.json','madrid-compilation-evidence.json']]
        catalog[0]['personalMarker']='preserve'
        before=copy.deepcopy((catalog,exams));report=apply_compilation(catalog,exams,evidence)
        self.assertEqual(report['newEntryIds'],[])
        self.assertEqual((catalog,exams),before)

    def test_all_source_rows_have_explicit_decisions_without_pdf_distribution(self):
        evidence=load('madrid-compilation-evidence.json')
        self.assertEqual(len(evidence['rows']),406)
        self.assertEqual(len({r['id'] for r in evidence['rows']}),406)
        self.assertTrue(all(r['status'] in ['accepted','pending'] for r in evidence['rows']))
        self.assertFalse(any(p.lower().endswith('.pdf') for p in public_files()))
        self.assertNotIn('AppData',json.dumps(load('exams.json')))

    def test_offline_registration_script_is_in_the_distributed_package(self):
        self.assertIn('sw.js',public_files())
        self.assertTrue((ROOT/'sw.js').is_file())

if __name__=='__main__':unittest.main()
