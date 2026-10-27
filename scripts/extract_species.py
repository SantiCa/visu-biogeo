"""Build the study catalogue from the supplied VISU PDFs.

This is deliberately conservative: it finds latin binomials and genus-level
entries ("Genus sp.") but leaves the original PDFs as the source of truth.
Run it whenever a source list is replaced or extended.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from pypdf import PdfReader


PDF_DIRECTORY = Path(
    r"G:\Mi unidad\1_Preparación Opos Educación\4_Secundaria BIO GEO"
    r"\1_Oposicion BioYGeo Preceje\4_Practico\2_VISU"
)
OUTPUT = Path(__file__).parents[1] / "data" / "species.json"

# Scientific notation occurring in the lists.  It supports taxa such as
# "Citrus x sinensis" and genus-level entries such as "Perla sp.".
TAXON = re.compile(
    r"\b([A-Z][a-z]{2,}(?:\s+(?:x|×)\s+|\s+)[a-z][a-z-]{1,}(?:\s+(?:subsp\.|var\.)\s+[a-z-]+)?|[A-Z][a-z]{2,}\s+sp\.)",
    re.UNICODE,
)
EXCLUDED = {
    "Oolitos de",
    "Familia theaceae",
    "Familia ebenaceae",
    "Reino Animalia",
    "Reino Plantae",
}


def normalise(name: str) -> str:
    name = re.sub(r"\s+", " ", name.strip())
    return name.replace(" × ", " x ")


def is_gbif_taxon(record: dict) -> bool:
    """Exclude Spanish labels accidentally matching the Latin-name pattern.

    GBIF's name matcher is queried only when the script is called with
    --verify-gbif. A high-confidence genus/species match is enough for the
    VISU entries, including lists written as "Genus sp.".
    """
    query = urllib.parse.urlencode({"name": record["scientificName"]})
    request = urllib.request.Request(
        f"https://api.gbif.org/v1/species/match?{query}",
        headers={"User-Agent": "visu-biogeo-catalog/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            match = json.load(response)
    except Exception:
        # Retain the item on transient network errors rather than silently
        # deleting potentially valid study material.
        return True
    rank_is_taxonomic = match.get("rank") in {"SPECIES", "GENUS", "SUBSPECIES", "VARIETY"}
    # A genus-level label is intended only for entries explicitly written as
    # "Genus sp.". For a two-word candidate, require an exact scientific-name
    # match so that Spanish phrases such as "Acacia del" do not survive via a
    # loose match to the genus Acacia.
    allowed_match = record["scientificName"].endswith("sp.") or match.get("matchType") == "EXACT"
    return rank_is_taxonomic and allowed_match and match.get("confidence", 0) >= 80


def main() -> None:
    positional_args = [argument for argument in sys.argv[1:] if not argument.startswith("--")]
    source_dir = Path(positional_args[0]) if positional_args else PDF_DIRECTORY
    found: dict[str, set[str]] = defaultdict(set)
    for pdf in sorted(source_dir.glob("*.pdf")):
        try:
            reader = PdfReader(str(pdf))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:  # keep one corrupt PDF from blocking the catalog
            print(f"Skipping {pdf.name}: {exc}", file=sys.stderr)
            continue
        for raw in TAXON.findall(text):
            name = normalise(raw)
            if name not in EXCLUDED:
                found[name].add(pdf.name)

    records = [
        {
            "id": re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"),
            "scientificName": name,
            "sources": sorted(sources),
            "andaluciaPriority": 0,
        }
        for name, sources in sorted(found.items(), key=lambda item: item[0].lower())
    ]
    if "--verify-gbif" in sys.argv:
        verified: list[dict] = []
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = {executor.submit(is_gbif_taxon, record): record for record in records}
            for future in as_completed(futures):
                if future.result():
                    verified.append(futures[future])
        records = sorted(verified, key=lambda item: item["scientificName"].lower())
        print(f"GBIF verification retained {len(records)} taxonomic entries")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(records)} study entries to {OUTPUT}")


if __name__ == "__main__":
    main()
