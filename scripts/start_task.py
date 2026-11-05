"""Start one task in a clean worktree from the latest origin/main."""
import argparse
import json
from pathlib import Path
import re
import subprocess


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], text=True,
                            encoding='utf8', capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name', nargs='?', help='Area and task, e.g. interfaz-buscador')
    parser.add_argument('--check', action='store_true', help='Check main without creating a task')
    args = parser.parse_args()
    if not args.check and (not args.name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.name)):
        parser.error('Provide a lowercase task name separated with hyphens')
    try:
        checkout = Path(__file__).resolve().parents[1]
        root = Path(git(checkout, 'rev-parse', '--path-format=absolute', '--git-common-dir')).parent
        if git(root, 'branch', '--show-current') != 'main':
            raise ValueError('The shared checkout must be on main')
        if git(root, 'status', '--porcelain'):
            raise ValueError('The shared checkout has changes. Preserve them before starting a task')
        git(root, 'fetch', 'origin')
        base = git(root, 'rev-parse', 'origin/main')
        # Reject local commits on main instead of mixing them into a fresh task.
        git(root, 'merge-base', '--is-ancestor', 'main', 'origin/main')
        result = {'root': str(root), 'base': base}
        if args.check:
            result['mainCurrent'] = git(root, 'rev-parse', 'main') == base
            print(json.dumps(result))
            return 0 if result['mainCurrent'] else 1
        branch = 'codex/' + args.name
        destination = root / 'worktrees' / args.name
        if destination.exists():
            raise ValueError('Task directory already exists. Continue its task or choose a new name')
        if subprocess.run(['git', '-C', str(root), 'show-ref', '--verify', '--quiet',
                           'refs/heads/' + branch]).returncode == 0:
            raise ValueError('Task branch already exists. Continue its task or choose a new name')
        git(root, 'merge', '--ff-only', 'origin/main')
        git(root, 'worktree', 'add', '-b', branch, str(destination), base)
        result.update(branch=branch, worktree=str(destination))
        print(json.dumps(result))
        return 0
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
