"""Local audit helpers: read-only PDF extraction, downloaded exam evidence."""
from pathlib import Path
import json, re, urllib.request
from pypdf import PdfReader
from extract_species import PDF_DIRECTORY

root = Path(__file__).resolve().parents[1]
out = root / 'tmp' / 'audit'
out.mkdir(parents=True, exist_ok=True)
for pdf in PDF_DIRECTORY.glob('*.pdf'):
    pages = [p.extract_text() or '' for p in PdfReader(pdf).pages]
    (out / (pdf.stem + '.txt')).write_text('\n'.join(f'\nPAGE {i+1}\n{x}' for i,x in enumerate(pages)), encoding='utf-8')

page = urllib.request.urlopen('https://www.precege.com/examenes/', timeout=30).read().decode()
links = re.findall(r'data-downloadurl=[\"\']([^\"\']+)', page)
for year in (2018, 2021):
    url = next(x for x in links if 'andalucia' in x.lower() and str(year) in x)
    data = urllib.request.urlopen(url.replace('&amp;', '&'), timeout=30).read()
    if not data.startswith(b'%PDF'): raise ValueError(f'Not a PDF: {year}')
    dest = out / f'andalucia-{year}.pdf'
    dest.write_bytes(data)
    text = '\n'.join(f'\nPAGE {i+1}\n{p.extract_text() or ""}' for i,p in enumerate(PdfReader(dest).pages))
    (out / f'andalucia-{year}.txt').write_text(text, encoding='utf-8')
    print(year, url, len(data), flush=True)
