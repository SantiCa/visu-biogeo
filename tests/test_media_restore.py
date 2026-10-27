import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import restore_media as media


class MediaRestoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = 'assets/reviewed/example.jpg'
        self.raw = b'approved specimen bytes'
        self.entry = {'bytes': len(self.raw), 'sha256': hashlib.sha256(self.raw).hexdigest()}
        (self.root / 'data').mkdir()
        (self.root / 'data/curated-images.json').write_text(json.dumps({
            'specimen': {'images': [{'status': 'approved', 'url': './' + self.path}]}
        }), encoding='utf8')

    def response(self, raw, url=None):
        response = io.BytesIO(raw)
        response.geturl = lambda: url or media.ORIGIN + '/' + self.path
        return response

    def test_download_requires_exact_hash_and_never_saves_corrupt_bytes(self):
        corrupt = b'x' * len(self.raw)
        with patch.object(media, 'urlopen', return_value=self.response(corrupt)):
            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                media.restore_one(self.root, self.path, self.entry, media.ORIGIN)
        self.assertFalse((self.root / self.path).exists())

    def test_verified_download_is_reused_without_another_request(self):
        with patch.object(media, 'urlopen', return_value=self.response(self.raw)) as request:
            self.assertEqual(media.restore_one(self.root, self.path, self.entry, media.ORIGIN), 'downloaded')
            self.assertEqual(media.restore_one(self.root, self.path, self.entry, media.ORIGIN), 'verified')
        self.assertEqual(request.call_count, 1)
        self.assertEqual((self.root / self.path).read_bytes(), self.raw)

    def test_local_modification_is_preserved_and_check_never_downloads(self):
        target = self.root / self.path
        target.parent.mkdir(parents=True)
        target.write_bytes(b'personal edit')
        with patch.object(media, 'urlopen') as request:
            with self.assertRaisesRegex(ValueError, 'preserved'):
                media.restore_one(self.root, self.path, self.entry, media.ORIGIN)
            with self.assertRaises(FileNotFoundError):
                media.restore_one(self.root, 'assets/reviewed/missing.jpg', self.entry, media.ORIGIN, True)
        request.assert_not_called()
        self.assertEqual(target.read_bytes(), b'personal edit')

    def test_rejects_paths_outside_media_and_insecure_origins(self):
        for path in ['../secret', 'assets/reviewed/../../secret', '/assets/reviewed/a.jpg',
                     'assets/reviewed/a/b.jpg', 'assets/reviewed/a\\b.jpg']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                media.safe_target(self.root, path)
        for origin in ['http://example.org', 'https://user:secret@example.org', 'https://example.org/path']:
            with self.subTest(origin=origin), self.assertRaises(ValueError):
                media.validate_origin(origin)

    def test_rejects_cross_origin_response(self):
        with patch.object(media, 'urlopen', return_value=self.response(self.raw, 'https://other.example/photo')):
            with self.assertRaisesRegex(ValueError, 'outside'):
                media.restore_one(self.root, self.path, self.entry, media.ORIGIN)
        self.assertFalse((self.root / self.path).exists())

    def test_refresh_requires_complete_bank_and_lock_tracks_approved_set(self):
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            media.refresh_lock(self.root)
        target = self.root / self.path
        target.parent.mkdir(parents=True)
        target.write_bytes(self.raw)
        self.assertEqual(media.refresh_lock(self.root)['locked'], 1)
        self.assertEqual(media.load_lock(self.root)['files'][self.path], self.entry)
        (self.root / 'data/curated-images.json').write_text('{}', encoding='utf8')
        with self.assertRaisesRegex(ValueError, 'Approved media changed'):
            media.load_lock(self.root)


if __name__ == '__main__':
    unittest.main()
