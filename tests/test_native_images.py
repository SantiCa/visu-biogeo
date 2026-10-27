import unittest,json,subprocess,time,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class NativeImages(unittest.TestCase):
 def test_reviewed_jpeg_and_named_png_load_without_exposing_private_files(self):
  executable=ROOT/'Abrir Visu BioGeo.exe'
  if not executable.exists():self.skipTest('Native launcher is not built')
  process=subprocess.Popen([str(executable),'--serve-only','--serve-for','30','--port','8088','--root',str(ROOT)],creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
  try:
   origin='http://127.0.0.1:8088/'
   for _ in range(60):
    try:urllib.request.urlopen(origin,timeout=1).close();break
    except (OSError,urllib.error.URLError):time.sleep(.1)
   photos=[im['url'][2:] for row in json.loads((ROOT/'data/curated-images.json').read_text(encoding='utf8')).values() for im in row['images'] if im['status']=='approved' and im['url'].startswith('./assets/reviewed/')]
   selected=[]
   for ext,mime in [('.jpeg','image/jpeg'),('.png','image/png'),('.jpg','image/jpeg')]:
    path=next((p for p in photos if p.endswith(ext)),None)
    if not path:continue
    with urllib.request.urlopen(origin+path,timeout=4) as response:self.assertEqual(response.headers.get_content_type(),mime);self.assertEqual(response.read(),(ROOT/path).read_bytes())
    selected.append(path)
   self.assertTrue(any(p.endswith('.jpeg') for p in selected))
   with urllib.request.urlopen(origin+'taxonomy-guide.mjs',timeout=4) as response:
    self.assertEqual(response.headers.get_content_type(),'text/javascript')
    self.assertEqual(response.read(),(ROOT/'taxonomy-guide.mjs').read_bytes())
   for path in ['data/learning-taxonomy-audit.json','supabase/schema.sql','assets/reviewed/%2e%2e/%2e%2e/config.js']:
    with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(origin+path,timeout=3)
    self.assertIn(e.exception.code,[403,404])
  finally:process.terminate();process.wait(timeout=5)
if __name__=='__main__':unittest.main()
