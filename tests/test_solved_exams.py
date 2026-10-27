import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from import_solved_exams import apply_evidence
from prepare_release import public_files

def load(name):return json.loads((ROOT/'data'/name).read_text(encoding='utf8'))

class SolvedExamImportTests(unittest.TestCase):
    def test_reapplication_preserves_ids_and_is_idempotent(self):
        catalog,history,exams,evidence=[load(n) for n in ['species.json','andalucia-priority.json','exams.json','solved-exam-evidence.json']]
        before=copy.deepcopy((catalog,history,exams));ids=[x['id'] for x in catalog]
        report=apply_evidence(catalog,history,exams,evidence)
        self.assertEqual(report['newEntryIds'],[])
        self.assertEqual(report['newItemYearOccurrences'],0)
        self.assertEqual([x['id'] for x in catalog],ids)
        self.assertEqual((catalog,history,exams),before)

    def test_new_entries_preserve_existing_user_fields_and_madrid(self):
        full=load('species.json');evidence=load('solved-exam-evidence.json')
        new_ids=set(json.loads((ROOT/'tests/fixtures/solved-exams-import.json').read_text(encoding='utf8'))['newEntryIds'])
        catalog=[x for x in full if x['id'] not in new_ids]
        catalog[0]['personalMarker']={'keep':True}
        history=load('andalucia-priority.json');history['events']=[e for e in history['events'] if not e.get('evidenceId')]
        exams=load('exams.json');madrid=copy.deepcopy([e for e in exams['events'] if e.get('region')=='Madrid'])
        apply_evidence(catalog,history,exams,evidence)
        self.assertEqual(catalog[0]['personalMarker'],{'keep':True})
        self.assertEqual(len({x['id'] for x in catalog}),len(catalog))
        self.assertEqual([e for e in exams['events'] if e.get('region')=='Madrid'],madrid)
        self.assertTrue(new_ids.issubset({x['id'] for x in catalog}))

    def test_distribution_contains_no_supplied_pdf_or_private_path(self):
        files=public_files()
        self.assertFalse(any(name.lower().endswith('.pdf') for name in files))
        for name in files:
            self.assertFalse(name.startswith(('tmp/','supabase/','output/')))
        for name in ['species.json','andalucia-priority.json','exams.json']:
            text=(ROOT/'data'/name).read_text(encoding='utf8')
            self.assertNotIn('G:/Mi unidad',text)
            self.assertNotIn('G:\\Mi unidad',text)

if __name__=='__main__':unittest.main()
