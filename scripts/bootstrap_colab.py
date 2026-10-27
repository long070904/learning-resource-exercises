"""Set up a downloaded GitHub source ZIP without running course/model code.

Private repository: use GitHub's Code > Download ZIP while signed in, then upload
that ZIP to Colab. No token, password, Drive mount, or stale package hash is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

GITHUB_REPOSITORY = 'https://github.com/long070904/learning-resource-exercises'
PUBLIC_CLONE_URL = GITHUB_REPOSITORY + '.git'
DEFAULT_DESTINATION = Path('/content/HaiLong_Colab_Exercises')
REQUIRED_HELPERS = ('colab_runtime.py', 'course_persistence.py', 'colab_full_runner.py')
REQUIRED_FILES = REQUIRED_HELPERS + ('exercise_manifest.json',)
MAX_FILES = 10000
MAX_TOTAL_BYTES = 512 * 1024 * 1024
MAX_MEMBER_BYTES = 64 * 1024 * 1024
RECEIPT_NAME = '.bootstrap_receipt.json'


def _archive_sha256(archive: Path) -> str:
    digest = hashlib.sha256()
    with archive.open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def _member_parts(name: str) -> tuple[str, ...]:
    """Reject traversal and Windows aliases before constructing any output path."""
    if not name or '\\' in name or name.startswith('/') or '\x00' in name:
        raise ValueError('Unsafe ZIP member name')
    raw = name[:-1] if name.endswith('/') else name
    parts = raw.split('/')
    invalid = '<>:"|?*'
    reserved = {'CON', 'PRN', 'AUX', 'NUL'} | {
        f'{prefix}{i}' for prefix in ('COM', 'LPT') for i in range(1, 10)
    }
    for part in parts:
        if not part or part in ('.', '..') or part.endswith((' ', '.')):
            raise ValueError('Unsafe ZIP path component')
        if any(c in invalid or ord(c) < 32 for c in part):
            raise ValueError('Unsafe ZIP path component')
        if part.split('.', 1)[0].upper() in reserved:
            raise ValueError('Reserved Windows ZIP path component')
    return tuple(parts)


def _validate_archive(archive: zipfile.ZipFile):
    members = archive.infolist()
    if not members or len(members) > MAX_FILES:
        raise ValueError('Empty archive or too many ZIP members')
    validated = []
    seen = set()
    total = 0
    file_paths = set()
    directory_paths = set()
    for info in members:
        parts = _member_parts(info.filename)
        key = '/'.join(parts).casefold()
        if key in seen:
            raise ValueError('Duplicate or case-colliding ZIP member')
        seen.add(key)
        mode = stat.S_IFMT(info.external_attr >> 16)
        if mode not in (0, stat.S_IFREG, stat.S_IFDIR):
            raise ValueError('Symlinks and special ZIP members are not allowed')
        if info.flag_bits & 1:
            raise ValueError('Encrypted ZIP members are not supported')
        if info.file_size > MAX_MEMBER_BYTES:
            raise ValueError('ZIP member exceeds the source-package limit')
        total += info.file_size
        if total > MAX_TOTAL_BYTES:
            raise ValueError('ZIP exceeds the source-package size limit')
        if info.is_dir():
            directory_paths.add(key)
        else:
            file_paths.add(key)
        directory_paths.update('/'.join(parts[:i]).casefold() for i in range(1, len(parts)))
        validated.append((info, parts))
    if file_paths & directory_paths:
        raise ValueError('ZIP contains a file/directory path collision')

    # Accept a normal GitHub branch ZIP (one wrapper directory), or an already
    # unwrapped source ZIP. All members must belong to the one selected payload.
    names = {tuple(parts) for info, parts in validated if not info.is_dir()}
    candidates = []
    for wrapper in ((), (validated[0][1][0],)):
        if all(wrapper + (required,) in names for required in REQUIRED_FILES):
            if all(parts[:len(wrapper)] == wrapper for _, parts in validated):
                candidates.append(wrapper)
    if len(candidates) != 1:
        raise ValueError('ZIP must contain one complete learning-resource repository payload')
    wrapper = candidates[0]
    return [(info, parts[len(wrapper):]) for info, parts in validated
            if len(parts) > len(wrapper)], '/'.join(wrapper), total


def assert_helper_modules(repository: Path) -> None:
    """Check filenames and manifest data; never import downloaded helper code."""
    repository = Path(repository)
    missing = [name for name in REQUIRED_FILES if not (repository / name).is_file()]
    if missing:
        raise ValueError('Repository payload is missing required files: ' + ', '.join(missing))
    rows = json.loads((repository / 'exercise_manifest.json').read_text(encoding='utf-8'))
    if not isinstance(rows, list) or not rows:
        raise ValueError('Expected a nonempty exercise manifest list')
    for row in rows:
        path = row.get('path') if isinstance(row, dict) else None
        if not isinstance(path, str) or not path.endswith('.ipynb'):
            raise ValueError('Unexpected exercise manifest path')
        parts = _member_parts(path)
        if not (repository.joinpath(*parts)).is_file():
            raise ValueError('An exercise listed in the manifest is missing')


def prepare_from_zip(archive: Path, destination: Path = DEFAULT_DESTINATION) -> Path:
    """Validate, stage and extract source files without overwriting existing work."""
    archive = Path(archive).expanduser().resolve()
    destination = Path(destination).expanduser().resolve()
    if not archive.is_file() or not zipfile.is_zipfile(archive):
        raise ValueError('Choose the repository ZIP downloaded from GitHub')
    archive_hash = _archive_sha256(archive)
    if destination.exists():
        receipt = destination / RECEIPT_NAME
        if receipt.is_file():
            saved = json.loads(receipt.read_text(encoding='utf-8'))
            if saved.get('archive_sha256') == archive_hash:
                assert_helper_modules(destination)
                return destination
        raise FileExistsError('Destination already exists. Use a fresh runtime or another destination; existing files were preserved.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as package:
        members, wrapper, declared_bytes = _validate_archive(package)
        with tempfile.TemporaryDirectory(prefix='.learning-resource-setup-', dir=destination.parent) as staging:
            payload = Path(staging) / 'payload'
            payload.mkdir()
            files_written = 0
            for info, parts in members:
                target = payload.joinpath(*parts)
                if not target.resolve().is_relative_to(payload.resolve()):
                    raise ValueError('ZIP target escapes the repository payload')
                if info.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                written = 0
                with package.open(info) as source, target.open('xb') as output:
                    for chunk in iter(lambda: source.read(1024 * 1024), b''):
                        written += len(chunk)
                        if written > info.file_size or written > MAX_MEMBER_BYTES:
                            raise ValueError('ZIP member exceeds its declared size')
                        output.write(chunk)
                if written != info.file_size:
                    raise ValueError('ZIP member size mismatch')
                files_written += 1
            assert_helper_modules(payload)
            receipt = {'setup_utc': datetime.now(timezone.utc).isoformat(),
                       'repository_url': GITHUB_REPOSITORY,
                       'archive_sha256': archive_hash, 'archive_wrapper': wrapper,
                       'files_written': files_written, 'declared_uncompressed_bytes': declared_bytes,
                       'course_code_executed': False, 'credentials_used': False}
            (payload / RECEIPT_NAME).write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
            if destination.exists():
                raise FileExistsError('Destination appeared during setup; existing files were preserved')
            payload.rename(destination)
    return destination


def prepare_public_clone(destination: Path = DEFAULT_DESTINATION) -> Path:
    """Optional unauthenticated route ONLY after the repository is made public."""
    destination = Path(destination).expanduser().resolve()
    if destination.exists():
        raise FileExistsError('Destination exists; existing files were preserved')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.learning-resource-public-clone-', dir=destination.parent) as staging:
        payload = Path(staging) / 'payload'
        environment = dict(os.environ, GIT_TERMINAL_PROMPT='0')
        result = subprocess.run(['git', 'clone', '--depth', '1', PUBLIC_CLONE_URL, str(payload)],
                                env=environment, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError('Public clone failed. For a private repository, download its ZIP while signed in and upload that ZIP instead.')
        assert_helper_modules(payload)
        if destination.exists():
            raise FileExistsError('Destination appeared during setup; existing files were preserved')
        payload.rename(destination)
    return destination


def list_exercises(repository: Path):
    """Print source paths and recorded GPU hints without starting an exercise."""
    repository = Path(repository).resolve()
    assert_helper_modules(repository)
    rows = json.loads((repository / 'exercise_manifest.json').read_text(encoding='utf-8'))
    for index, row in enumerate(rows, 1):
        hint = 'GPU suggested' if row.get('gpu') else 'see exercise setup'
        print(f'{index:02d}. {row["path"]}  [{hint}]')
    print(f'\n{len(rows)} exercise sources found. Setup does not establish completion or start training.')
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--zip', type=Path, dest='archive', help='Signed-in GitHub Download ZIP file')
    action.add_argument('--public-clone', action='store_true', help='Use ONLY when the repository is public')
    action.add_argument('--list', type=Path, dest='existing', help='List an existing repository without extraction')
    parser.add_argument('--destination', type=Path, default=DEFAULT_DESTINATION)
    options = parser.parse_args()
    repository = options.existing
    if options.archive:
        repository = prepare_from_zip(options.archive, options.destination)
    elif options.public_clone:
        repository = prepare_public_clone(options.destination)
    print('Repository:', Path(repository).resolve())
    list_exercises(repository)


if __name__ == '__main__':
    main()
