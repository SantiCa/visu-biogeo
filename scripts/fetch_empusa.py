from pathlib import Path
from review_images import download
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tmp/image-review'
for name,url in [
 ('empusa-spain.jpg','https://upload.wikimedia.org/wikipedia/commons/b/b7/Empusa_pennata_stehend.jpg'),
 ('empusa-portugal.jpg','https://upload.wikimedia.org/wikipedia/commons/e/ea/Empusa_pennata-.jpg')]:
    download(url,OUT/name)
    print(name,flush=True)
