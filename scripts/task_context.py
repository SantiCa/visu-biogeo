"""Read-only, bounded context queries for a focused task; no external dependencies."""
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf8'))


def select_rows(rows, args):
    if args.kind:
        rows = [row for row in rows if row.get('kind') == args.kind]
    rows.sort(key=lambda row: (not row.get('priority', False), row.get('name', '').casefold(), row['id']))
    return {'matching': len(rows), 'shown': min(len(rows), args.limit), 'items': rows[:args.limit]}


def image_context(args):
    audit = load('image-audit.json')
    rows = [dict(row) for row in audit['allMissingPairs']
            if args.missing_pairs or row['approvedImages'] == 0]
    return {'area': 'imagenes', 'auditDate': audit['date'],
            'selection': 'missing-pairs' if args.missing_pairs else 'zero-approved-images',
            **select_rows(rows, args)}


def note_context(args):
    catalog = load('species.json')
    notes = load('study-notes.json')
    priority = {row['itemId'] for row in load('andalucia-priority.json')['events']}
    rows = []
    for row in catalog:
        note = notes.get(row['id'])
        if args.pending_etymology:
            matches = note is not None and (not note.get('etymology') or re.search(
                'pendiente|contrastar|requiere contraste', note['etymology'], re.I))
        else:
            matches = note is None
        if matches:
            rows.append({'id': row['id'], 'name': row['scientificName'], 'kind': row['kind'],
                         'priority': row['id'] in priority})
    return {'area': 'fichas',
            'selection': 'pending-etymology' if args.pending_etymology else 'missing-profile',
            **select_rows(rows, args)}


def entry_context(item_id):
    row = next((row for row in load('species.json') if row['id'] == item_id), None)
    if row is None:
        raise ValueError('Unknown catalogue ID: ' + item_id)
    return {
        'entry': row,
        'approvedImages': [im for im in load('curated-images.json').get(item_id, {}).get('images', [])
                           if im.get('status') == 'approved'],
        'studyNote': load('study-notes.json').get(item_id),
        'learningTaxonomy': load('learning-taxonomy.json').get(item_id),
        'learningGeology': load('learning-geology.json').get(item_id),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for command in ('images', 'notes'):
        sub = commands.add_parser(command)
        sub.add_argument('--limit', type=int, default=5)
        sub.add_argument('--kind', help='Catalogue kind, e.g. fosil, organismo, estructura')
        if command == 'images':
            sub.add_argument('--missing-pairs', action='store_true')
        else:
            sub.add_argument('--pending-etymology', action='store_true')
    entry = commands.add_parser('entry')
    entry.add_argument('id')
    args = parser.parse_args()
    if hasattr(args, 'limit') and not 1 <= args.limit <= 20:
        parser.error('--limit must be between 1 and 20')
    try:
        result = (entry_context(args.id) if args.command == 'entry' else
                  image_context(args) if args.command == 'images' else note_context(args))
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, str(error) + '\n')
    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
