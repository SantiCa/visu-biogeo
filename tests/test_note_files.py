import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from note_files import (NOTE_FILES, load_note_banks, load_study_notes, load_family_notes,
                        save_study_notes, save_family_notes, validate_note_banks)
from prepare_release import public_files


class RankedNotesTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.data = Path(self.temporary.name)
        for filename in (*NOTE_FILES, 'species.json', 'learning-taxonomy.json'):
            shutil.copyfile(ROOT / 'data' / filename, self.data / filename)

    def test_all_documented_names_and_catalogue_ids_have_correct_rank_placeholders(self):
        self.assertEqual(validate_note_banks(self.data), [])

    def test_saving_one_profile_preserves_other_profiles_family_notes_and_guides(self):
        before = load_note_banks(self.data)
        profile = copy.deepcopy(load_study_notes(self.data)['briza-minor'])
        profile['description'] = 'Updated description for this test.'
        save_study_notes({'briza-minor': profile}, self.data)
        after = load_note_banks(self.data)
        before['species-notes.json']['entries']['briza-minor']['profile'] = profile
        self.assertEqual(after, before)
        self.assertEqual(validate_note_banks(self.data), [])

    def test_family_updates_preserve_group_descriptions_and_empty_names(self):
        before = load_note_banks(self.data)
        family = copy.deepcopy(load_family_notes(self.data)['Poaceae'])
        family['etymology'] = 'Updated name construction for this test.'
        save_family_notes({'Poaceae': family}, self.data)
        before['family-notes.json']['taxa']['family:Poaceae']['note'] = family
        self.assertEqual(load_note_banks(self.data), before)

    def test_writes_reject_unknown_ids_without_changing_any_files(self):
        before = load_note_banks(self.data)
        with self.assertRaisesRegex(ValueError, 'Unknown catalogue IDs'):
            save_study_notes({'unknown-test-id': {}}, self.data)
        self.assertEqual(load_note_banks(self.data), before)

    def test_audit_detects_missing_names_and_incorrect_rank_files(self):
        path = self.data / 'species-notes.json'
        bank = json.loads(path.read_text(encoding='utf8'))
        bank['entries'].pop('briza-minor')
        bank['taxa']['class:Test'] = {'name': 'Test', 'rank': 'class'}
        path.write_text(json.dumps(bank), encoding='utf8')
        errors = validate_note_banks(self.data)
        self.assertIn('Missing catalogue placeholder: briza-minor', errors)
        self.assertIn('Taxon in wrong rank file: class:Test', errors)

    def test_offline_package_and_native_server_include_every_rank_file(self):
        files = public_files()
        native = (ROOT / 'desktop' / 'VisuBioGeo.cs').read_text(encoding='utf8')
        for filename in NOTE_FILES:
            self.assertIn('data/' + filename, files)
            self.assertIn('"' + filename + '"', native)
        self.assertIn('taxon-notes.mjs', files)
        self.assertIn('"taxon-notes.mjs"', native)
        self.assertNotIn('data/study-notes.json', files)


if __name__ == '__main__':
    unittest.main()
