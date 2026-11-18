"""Read and update ranked notes without changing catalogue IDs or classification."""
import json
from pathlib import Path
import re

DATA = Path(__file__).resolve().parents[1] / 'data'
RANK_FILES = {
    'class': 'class-notes.json',
    'order': 'order-notes.json',
    'family': 'family-notes.json',
    'genus': 'genus-notes.json',
    'species': 'species-notes.json',
}
OTHER_FILE = 'other-notes.json'
NOTE_FILES = (*RANK_FILES.values(), OTHER_FILE)


def file_for_rank(rank):
    return RANK_FILES.get(re.sub(r'^(sub|super|infra)', '', rank or ''), OTHER_FILE)


def read_json(path):
    return json.loads(path.read_text(encoding='utf8'))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def load_note_banks(data_dir=DATA):
    return {name: read_json(data_dir / name) for name in NOTE_FILES}


def load_study_notes(data_dir=DATA):
    notes = {}
    seen = set()
    for bank in load_note_banks(data_dir).values():
        for item_id, entry in bank['entries'].items():
            if item_id in seen:
                raise ValueError('Duplicate catalogue entry: ' + item_id)
            seen.add(item_id)
            if 'profile' in entry:
                notes[item_id] = entry['profile']
    return notes


def load_family_notes(data_dir=DATA):
    taxa = read_json(data_dir / RANK_FILES['family'])['taxa']
    return {taxon['name']: taxon['note'] for taxon in taxa.values()
            if taxon['rank'] == 'family' and 'note' in taxon}


def entry_rank(item, taxonomy):
    if item['kind'] not in ('organismo', 'fosil') or taxonomy.get('nonTaxonomic'):
        return None
    # Use the documented identification rank, never infer one from word count.
    return taxonomy.get('rank')


def synchronize_names(banks, catalog, taxonomy):
    entries = {}
    for bank in banks.values():
        for item_id, entry in bank['entries'].items():
            if item_id in entries:
                raise ValueError('Duplicate catalogue entry: ' + item_id)
            entries[item_id] = entry
        bank['entries'] = {}
    unknown = entries.keys() - {item['id'] for item in catalog}
    if unknown:
        raise ValueError('Unknown catalogue IDs: ' + ', '.join(sorted(unknown)))
    for item in catalog:
        taxon = taxonomy.get(item['id'], {})
        rank = entry_rank(item, taxon)
        bank = banks[file_for_rank(rank)]
        entry = entries.get(item['id'], {})
        bank['entries'][item['id']] = {**entry, 'name': item['scientificName']}
        if rank:
            key = rank + ':' + item['scientificName']
            bank['taxa'].setdefault(key, {'name': item['scientificName'], 'rank': rank})
        if item['kind'] in ('organismo', 'fosil') and not taxon.get('nonTaxonomic'):
            for taxon_rank, name in taxon.get('ranks', {}).items():
                if name:
                    banks[file_for_rank(taxon_rank)]['taxa'].setdefault(
                        taxon_rank + ':' + name, {'name': name, 'rank': taxon_rank})


def save_note_banks(banks, data_dir=DATA):
    for filename, bank in banks.items():
        bank['taxa'] = dict(sorted(bank['taxa'].items()))
        if bank != read_json(data_dir / filename):
            write_json(data_dir / filename, bank)


def save_study_notes(notes, data_dir=DATA):
    banks = load_note_banks(data_dir)
    catalog = {item['id']: item for item in read_json(data_dir / 'species.json')}
    taxonomy = read_json(data_dir / 'learning-taxonomy.json')
    unknown = notes.keys() - catalog.keys()
    if unknown:
        raise ValueError('Unknown catalogue IDs: ' + ', '.join(sorted(unknown)))
    for item_id, profile in notes.items():
        item = catalog[item_id]
        filename = file_for_rank(entry_rank(item, taxonomy.get(item_id, {})))
        for bank in banks.values():
            bank['entries'].pop(item_id, None)
        banks[filename]['entries'][item_id] = {'name': item['scientificName'], 'profile': profile}
    synchronize_names(banks, list(catalog.values()), taxonomy)
    save_note_banks(banks, data_dir)


def save_family_notes(notes, data_dir=DATA):
    path = data_dir / RANK_FILES['family']
    bank = read_json(path)
    for name, note in notes.items():
        taxon = bank['taxa'].setdefault('family:' + name, {'name': name, 'rank': 'family'})
        taxon['note'] = note
    write_json(path, bank)


def validate_note_banks(data_dir=DATA):
    banks = load_note_banks(data_dir)
    catalog = {item['id']: item for item in read_json(data_dir / 'species.json')}
    taxonomy = read_json(data_dir / 'learning-taxonomy.json')
    seen_entries, seen_taxa, errors = set(), set(), []
    for filename, bank in banks.items():
        for key, taxon in bank['taxa'].items():
            if key in seen_taxa:
                errors.append('Duplicate taxon: ' + key)
            seen_taxa.add(key)
            if key != taxon['rank'] + ':' + taxon['name']:
                errors.append('Invalid taxon key: ' + key)
            if file_for_rank(taxon['rank']) != filename:
                errors.append('Taxon in wrong rank file: ' + key)
            guide = taxon.get('guide')
            if guide and not all(guide.get(field) for field in ('text', 'contrast', 'source')):
                errors.append('Incomplete group guide: ' + key)
        for item_id, entry in bank['entries'].items():
            if item_id in seen_entries:
                errors.append('Duplicate catalogue entry: ' + item_id)
            seen_entries.add(item_id)
            item = catalog.get(item_id)
            if item is None:
                errors.append('Unknown catalogue ID: ' + item_id)
                continue
            rank = entry_rank(item, taxonomy.get(item_id, {}))
            if entry['name'] != item['scientificName'] or file_for_rank(rank) != filename:
                errors.append('Stale catalogue placeholder: ' + item_id)
    for item_id, item in catalog.items():
        if item_id not in seen_entries:
            errors.append('Missing catalogue placeholder: ' + item_id)
        taxon = taxonomy.get(item_id, {})
        rank = entry_rank(item, taxon)
        required = dict(taxon.get('ranks', {})) if item['kind'] in ('organismo', 'fosil') and not taxon.get('nonTaxonomic') else {}
        for required_rank, name in [*required.items(), (rank, item['scientificName'])]:
            if required_rank and name and required_rank + ':' + name not in seen_taxa:
                errors.append('Missing taxon placeholder: ' + required_rank + ':' + name)
    return errors
