"""Read-only count of the researched PRECEGE queue, not of all PDF omissions.

Run from a task worktree with --research-dir ../../tmp. No network, extraction,
imports or catalogue changes. The 43 nominal queries are research inputs, not
approved names. Higher-rank GBIF results never satisfy a species candidate.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
CURRENT_IDS = ['siren-lacertina', 'rana-pyrenaica', 'coronella-austriaca']
PREVIOUS = {
    '36': ('b4037717b35810e5bd16400b264366dd0b8fa47f', ['porcellana-platycheles']),
    '37': ('bc82e677d4f92531f6a1c7aada0fe9ea1c5f37ec', [
        'cordulegaster-boltonii', 'euphydryas-aurinia', 'bombus-terrestris']),
}
RELATED = {
    '27': ['burhinus-oedicnemus', 'phlomis-herba-venti',
           'berberomeloe-majalis', 'herpestes-ichneumon'],
    '30': ['canis-lupus', 'vulpes-vulpes'],
}


def git_json(ref, filename):
    return json.loads(subprocess.check_output(
        ['git', '-C', str(ROOT), 'show', ref + ':data/' + filename], encoding='utf8'))


def norm(name):
    return ''.join(c for c in unicodedata.normalize('NFKD', name.casefold())
                   if c.isalnum())


def find_species(name, catalog, taxonomy):
    return [x for x in catalog if x['kind'] in ['organismo', 'fosil']
            and taxonomy.get(x['id'], {}).get('rank') == 'species'
            and norm(name) in {norm(n) for n in [x['scientificName'], *x.get('aliases', [])]}]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--research-dir', type=Path, required=True)
    args = parser.parse_args()
    path = args.research_dir / 'cotejo-pdf-gbif.json'
    research = json.loads(path.read_text(encoding='utf8'))
    if len(research) != 43:
        raise ValueError('Research universe changed: review the queue definition first')
    current = json.loads((ROOT / 'data/species.json').read_text(encoding='utf8'))
    taxonomy = json.loads((ROOT / 'data/learning-taxonomy.json').read_text(encoding='utf8'))
    main_catalog = git_json('origin/main', 'species.json')
    main_taxonomy = git_json('origin/main', 'learning-taxonomy.json')
    main_sha = subprocess.check_output(
        ['git', '-C', str(ROOT), 'rev-parse', 'origin/main'], encoding='utf8').strip()
    previous = {}
    for pr, (sha, ids) in PREVIOUS.items():
        catalog = git_json(sha, 'species.json')
        taxa = git_json(sha, 'learning-taxonomy.json')
        for item_id in ids:
            item = next(x for x in catalog if x['id'] == item_id)
            assert taxa[item_id]['rank'] == 'species'
            previous[item_id] = (pr, item)
    excluded, rows = [], []
    seen = set()
    for query, match in research.items():
        if ' subsp. ' in query:
            excluded.append({'query': query, 'reason': 'subspecies, not a new species'})
            continue
        # This synonym was reviewed in PR 37. No other preliminary GBIF
        # substitution is treated as an approved synonym by this audit.
        name = 'Cordulegaster boltonii' if query == 'Cordulegaster annulatus' else query
        if name in seen:
            excluded.append({'query': query, 'reason': 'same reviewed species already counted'})
            continue
        seen.add(name)
        row = {'candidate': name, 'researchQuery': query}
        found = find_species(name, main_catalog, main_taxonomy)
        prior = [(pr, item) for pr, item in previous.values()
                 if norm(name) in {norm(n) for n in [item['scientificName'], *item.get('aliases', [])]}]
        added = [x for x in find_species(name, current, taxonomy) if x['id'] in CURRENT_IDS]
        if found:
            row.update(status='alreadyInMain', ids=[x['id'] for x in found])
        elif prior:
            row.update(status='verifiedPreviousPR', pr=prior[0][0], ids=[prior[0][1]['id']])
        elif added:
            row.update(status='verifiedThisBatch', ids=[x['id'] for x in added])
        else:
            exact = (match.get('canonicalName') == query and match.get('rank') == 'SPECIES'
                     and match.get('status') == 'ACCEPTED' and match.get('matchType') == 'EXACT')
            row['status'] = 'pendingReviewWithExactPreliminaryMatch' if exact else 'pendingTaxonomicResolution'
        rows.append(row)
    buckets = {status: [r for r in rows if r['status'] == status]
               for status in sorted({r['status'] for r in rows})}
    related = {pr: [{'id': x['id'], 'name': x['scientificName'], 'sources': x['sources']}
                    for x in main_catalog if x['id'] in ids] for pr, ids in RELATED.items()}
    assert all(len(related[pr]) == len(ids) for pr, ids in RELATED.items())
    chat_ids = sorted(set(CURRENT_IDS) | {item_id for item_id, (pr, _) in previous.items() if pr == '37'})
    related_queue_ids = sorted(item_id for item_id, (pr, _) in previous.items() if pr != '37')
    result = {'researchSHA256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'mainSHA': main_sha, 'nominalResearchQueries': len(research),
              'speciesCandidatesAfterExclusions': len(rows), 'excluded': excluded,
              'newThisBatch': CURRENT_IDS, 'chatSpeciesIds': chat_ids,
              'relatedQueueSpeciesIds': related_queue_ids,
              'chatSpeciesAlreadyInMain': sorted(set(chat_ids) & {x['id'] for x in main_catalog}),
              'previousPRSnapshots': {pr: sha for pr, (sha, _) in PREVIOUS.items()},
              'counts': {k: len(v) for k, v in buckets.items()}, 'buckets': buckets,
              'relatedAdditionsOutsideThe51PDFQueue': related,
              'limit': 'Known researched queue only. Exact preliminary matches still need review. '
                       'Not a definitive count of omissions in the 51 PDFs; no global re-audit.'}
    sys.stdout.reconfigure(encoding='utf8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
