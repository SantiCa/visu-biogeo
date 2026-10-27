"""Restore approved public media, verifying a versioned SHA-256 lock (stdlib only)."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://visu-biogeo-santica.nimblequail260.chatgpt.site'


def approved_paths(root):
    curated = json.loads((root / 'data/curated-images.json').read_text(encoding='utf8'))
    return list(dict.fromkeys(
        im['url'][2:]
        for row in curated.values() for im in row.get('images', [])
        if im.get('status') == 'approved'
        and im.get('url', '').startswith('./assets/reviewed/')
    ))


def safe_target(root, relative):
    path = PurePosixPath(relative)
    if (not relative.startswith('assets/reviewed/') or '\\' in relative
            or path.is_absolute() or any(p in ('..', '.') for p in relative.split('/'))
            or len(path.parts) != 3 or ':' in relative):
        raise ValueError('Invalid media path: ' + relative)
    root = root.resolve()
    target = (root / relative).resolve()
    if root not in target.parents:
        raise ValueError('Media path escapes the project: ' + relative)
    return target


def sha256_file(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def check_local(target, entry):
    if not target.is_file():
        raise ValueError('Local path is not a file: ' + str(target))
    if target.stat().st_size != entry['bytes'] or sha256_file(target) != entry['sha256']:
        raise ValueError('Local file differs; preserved without overwriting: ' + str(target))


def validate_origin(origin):
    parsed = urlsplit(origin)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username
            or parsed.password or parsed.path not in ('', '/') or parsed.query or parsed.fragment):
        raise ValueError('The media origin must be a plain HTTPS origin')
    return origin.rstrip('/')


def load_lock(root):
    lock = json.loads((root / 'data/media-lock.json').read_text(encoding='utf8'))
    if lock.get('format') != 1:
        raise ValueError('Unsupported media lock format')
    lock['origin'] = validate_origin(lock['origin'])
    if set(lock['files']) != set(approved_paths(root)):
        raise ValueError('Approved media changed: run --refresh-lock with the complete local bank')
    for relative, entry in lock['files'].items():
        safe_target(root, relative)
        if (not re.fullmatch('[0-9a-f]{64}', entry['sha256'])
                or type(entry['bytes']) is not int or entry['bytes'] <= 0):
            raise ValueError('Invalid size or SHA-256: ' + relative)
    return lock


def refresh_lock(root):
    entries = {}
    for relative in sorted(approved_paths(root)):
        target = safe_target(root, relative)
        if not target.is_file():
            raise ValueError('Cannot refresh an incomplete bank: ' + relative)
        entries[relative] = {'sha256': sha256_file(target), 'bytes': target.stat().st_size}
    lock = {'format': 1, 'origin': ORIGIN, 'files': entries}
    (root / 'data/media-lock.json').write_text(
        json.dumps(lock, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    return {'locked': len(entries), 'bytes': sum(e['bytes'] for e in entries.values())}


def restore_one(root, relative, entry, origin, check_only=False):
    target = safe_target(root, relative)
    if target.exists():
        check_local(target, entry)
        return 'verified'
    if check_only:
        raise FileNotFoundError('Missing media: ' + relative)
    url = origin + '/' + quote(relative, safe='/')
    request = Request(url, headers={'User-Agent': 'VisuBioGeo-media-restore/1.0'})
    with urlopen(request, timeout=45) as response:
        effective = urlsplit(response.geturl())
        expected = urlsplit(origin)
        if (effective.scheme, effective.netloc) != (expected.scheme, expected.netloc):
            raise ValueError('Media redirected outside the configured origin: ' + relative)
        raw = response.read(entry['bytes'] + 1)
    if len(raw) != entry['bytes'] or hashlib.sha256(raw).hexdigest() != entry['sha256']:
        raise ValueError('Downloaded size or SHA-256 mismatch; file not saved: ' + relative)
    target.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation also preserves a local file created during the download.
    with target.open('xb') as output:
        output.write(raw)
    return 'downloaded'


def run(root, check_only=False, sample=False, workers=4):
    lock = load_lock(root)
    paths = approved_paths(root)
    if sample:
        paths = list(dict.fromkeys(
            next((p for p in paths if p.endswith(ext)), '') for ext in ('.jpeg', '.png', '.jpg')
        ))
        paths = [p for p in paths if p]
    results = {'selected': len(paths), 'verified': 0, 'downloaded': 0, 'errors': []}

    def restore(relative):
        try:
            return restore_one(root, relative, lock['files'][relative], lock['origin'], check_only), None
        except Exception as error:
            return None, {'path': relative, 'error': str(error)}

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for index, (result, error) in enumerate(executor.map(restore, paths), 1):
            if error:
                results['errors'].append(error)
            else:
                results[result] += 1
            if index % 500 == 0:
                print(f'Checked {index}/{len(paths)}; errors: {len(results["errors"])}', flush=True)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    operation = parser.add_mutually_exclusive_group()
    operation.add_argument('--check', action='store_true', help='Verify local files without downloading')
    operation.add_argument('--refresh-lock', action='store_true', help='Hash the approved local bank; no upload')
    parser.add_argument('--sample', action='store_true', help='Only the three photos used by native tests')
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        parser.error('--workers must be between 1 and 8')
    if args.refresh_lock and args.sample:
        parser.error('--refresh-lock requires the full bank')
    try:
        report = refresh_lock(ROOT) if args.refresh_lock else run(ROOT, args.check, args.sample, args.workers)
    except Exception as error:
        parser.exit(1, str(error) + '\n')
    print(json.dumps(report, ensure_ascii=True, indent=2))
    if report.get('errors'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
