"""Colab paths, dependency profiles, data and evidence helpers for this package."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import importlib.metadata as metadata
from collections import Counter
import hashlib, json, os, re, shutil, subprocess, sys, urllib.request, zipfile, uuid, zlib

BASE = ['numpy>=1.26,<3', 'pandas>=2.2,<3', 'scipy>=1.14,<2',
        'scikit-learn>=1.5,<2', 'matplotlib>=3.9,<4', 'pillow>=10', 'packaging']
PROFILES = {
    'basic': [],
    'torch': ['torch>=2.5,<3'],
    'google': ['torch>=2.5,<3', 'keras>=3.8,<4', 'google-ml-edu==0.1.3', 'plotly>=5,<7'],
    'tensorflow': ['tensorflow>=2.18,<2.22'],
    'fairness': ['tensorflow==2.21.0', 'tf-keras==2.21.0', 'tensorflow-model-remediation==0.1.7.1', 'tensorboard>=2.20,<3'],
    'fastai': ['fastai==2.8.12', 'ddgs>=9', 'timm>=1,<2', 'ipywidgets>=8,<9'],
    'mit': ['mitdeeplearning==0.7.5', 'torchsummary', 'h5py', 'torchvision', 'opencv-python-headless>=4.11,<4.12'],
    'llm': ['mitdeeplearning==0.7.5', 'transformers>=4.55,<5', 'peft>=0.17,<1',
            'accelerate>=1,<2', 'datasets>=3,<5', 'lion-pytorch', 'opencv-python-headless>=4.11,<4.12'],
    'nlp': ['transformers>=4.55,<5', 'datasets>=3,<5', 'accelerate>=1,<2', 'sentencepiece'],
    'book': ['fastbook==0.0.29', 'fastai==2.8.12', 'ipywidgets>=7.8,<8', 'sentencepiece'],
    'diffusion': ['diffusers>=0.35,<0.37', 'transformers>=4.55,<5', 'accelerate>=1,<2',
                  'fastcore', 'fastdownload', 'ftfy', 'ipywidgets>=8,<9', 'imageio-ffmpeg'],
    'part2': ['fastcore>=1.7', 'fastprogress', 'datasets>=3,<5', 'torcheval==0.0.7',
              'diffusers>=0.35,<0.37', 'transformers>=4.55,<5', 'accelerate>=1,<2',
              'einops', 'timm>=1,<2', 'numba', 'numba-cuda', 'wandb', 'k-diffusion',
              'ipywidgets>=8,<9', 'imageio', 'imageio-ffmpeg', 'torchvision'],
}


def install_profile(profile):
    from packaging.requirements import Requirement
    missing = []
    for spec in BASE + PROFILES[profile]:
        req = Requirement(spec)
        try:
            installed = metadata.version(req.name)
        except metadata.PackageNotFoundError:
            installed = None
        if installed is None or installed not in req.specifier:
            missing.append(spec)
    if missing:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', *missing])
    # Fail clearly when a previously imported package was replaced by pip.
    for name in ['numpy', 'pandas', 'torch', 'tensorflow', 'keras', 'fastai', 'transformers']:
        module = sys.modules.get(name)
        if module is not None and getattr(module, '__version__', None):
            if str(module.__version__) != metadata.version(name):
                raise RuntimeError(f'{name} changed during setup. Restart the Colab session and run all cells again.')


def download(url, target):
    target = Path(target)
    if target.is_file() and target.stat().st_size:
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + '.download')
    print('Downloading', target.name)
    with urllib.request.urlopen(url, timeout=120) as response, temporary.open('wb') as out:
        shutil.copyfileobj(response, out)
    temporary.replace(target)
    return target


def safe_extract(archive, destination):
    destination = Path(destination).resolve()
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            if not (destination / member.filename).resolve().is_relative_to(destination):
                raise ValueError('Unsafe ZIP entry: ' + member.filename)
            if (member.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError('ZIP symlinks are not supported: ' + member.filename)
        z.extractall(destination)


TINY_IMAGENET_URL = 'https://cs231n.stanford.edu/tiny-imagenet-200.zip'
# Published dataset archive checksum: https://zenodo.org/records/10720917
# The official Stanford ZIP metadata independently confirms these exact counts.
TINY_IMAGENET_MD5 = '90528d7ca1a48142e341f4ef8d21d0de'
TINY_IMAGENET_CLASSES = 200
TINY_IMAGENET_TRAIN_PER_CLASS = 500
TINY_IMAGENET_VAL_PER_CLASS = 50
TINY_IMAGENET_TEST_IMAGES = 10000
TINY_IMAGENET_NOTEBOOKS = {
    '24_imgnet_tiny-wide.ipynb', '24_imgnet_tiny-widish.ipynb',
    '24_imgnet_tiny.ipynb', '24a_imgnet_tiny-200.ipynb', '25_superres.ipynb',
}


def _tiny_digests(path):
    md5, sha256 = hashlib.md5(), hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            md5.update(chunk); sha256.update(chunk)
    return md5.hexdigest(), sha256.hexdigest()


def _tiny_archive_manifest(z):
    """Reject unsafe ZIP members and verify the complete original split layout."""
    prefix = 'tiny-imagenet-200/'
    infos = z.infolist()
    names = [info.filename for info in infos]
    if len(names) != len(set(names)):
        raise ValueError('Duplicate Tiny ImageNet ZIP members.')
    files = {}
    for info in infos:
        path = PurePosixPath(info.filename)
        if (not info.filename.startswith(prefix) or path.is_absolute() or
                '..' in path.parts or '\\' in info.filename or ':' in info.filename or
                (info.external_attr >> 16) & 0o170000 == 0o120000):
            raise ValueError('Unsafe or unexpected Tiny ImageNet ZIP member: '+info.filename)
        if not info.is_dir(): files[info.filename[len(prefix):]] = info
    ids = z.read(prefix+'wnids.txt').decode('utf-8').splitlines()
    if (len(ids) != TINY_IMAGENET_CLASSES or len(set(ids)) != len(ids) or
            any(re.fullmatch(r'n\d{8}', sid) is None for sid in ids)):
        raise ValueError('Tiny ImageNet must contain exactly 200 unique source synsets.')
    train = {name for name in files if name.startswith('train/') and name.endswith('.JPEG')}
    expected_train = {f'train/{sid}/images/{sid}_{i}.JPEG'
                      for sid in ids for i in range(TINY_IMAGENET_TRAIN_PER_CLASS)}
    if train != expected_train:
        raise ValueError('Tiny ImageNet training ZIP must have 500 original images in every class.')
    expected_val = {f'val_{i}.JPEG' for i in range(len(ids)*TINY_IMAGENET_VAL_PER_CLASS)}
    val = {name.removeprefix('val/images/') for name in files
           if name.startswith('val/images/') and name.endswith('.JPEG')}
    annotations = {}
    for line in z.read(prefix+'val/val_annotations.txt').decode('utf-8').splitlines():
        fields = line.split('\t')
        if len(fields) != 6 or fields[0] in annotations or fields[1] not in ids:
            raise ValueError('Invalid or duplicate Tiny ImageNet validation annotation.')
        annotations[fields[0]] = fields[1]
    if (val != expected_val or set(annotations) != val or
            Counter(annotations.values()) != Counter({sid:TINY_IMAGENET_VAL_PER_CLASS for sid in ids})):
        raise ValueError('Tiny ImageNet validation must align all 10,000 files and 200 class labels.')
    test = {name for name in files if name.startswith('test/images/') and name.endswith('.JPEG')}
    if test != {f'test/images/test_{i}.JPEG' for i in range(TINY_IMAGENET_TEST_IMAGES)}:
        raise ValueError('Incomplete original Tiny ImageNet unlabeled test files.')
    return {'files': files, 'class_ids': ids, 'train_images':len(train),
            'validation_images':len(val), 'test_images':len(test),
            'validation_annotations':annotations}


def _validate_tiny_tree(target, manifest):
    """Match extracted bytes to the checksum-verified ZIP, not just directories."""
    target = Path(target).resolve()
    if not target.is_dir(): raise FileNotFoundError('Tiny ImageNet extraction is absent.')
    actual_images = {str(p.relative_to(target).as_posix()) for p in target.rglob('*.JPEG')}
    expected_images = {name for name in manifest['files'] if name.endswith('.JPEG')}
    if actual_images != expected_images:
        raise ValueError('Tiny ImageNet image file set is incomplete or contains extra images.')
    actual_classes = {p.name for p in (target/'train').iterdir() if p.is_dir()}
    if actual_classes != set(manifest['class_ids']):
        raise ValueError('Tiny ImageNet training class directories differ from the original.')
    for name, info in manifest['files'].items():
        path = target/name
        if path.is_symlink() or not path.resolve().is_relative_to(target):
            raise ValueError('Tiny ImageNet extracted members must stay inside its own folder.')
        if not path.is_file() or path.stat().st_size != info.file_size:
            raise ValueError('Missing or truncated Tiny ImageNet file: '+name)
        crc = 0
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024*1024), b''): crc = zlib.crc32(chunk, crc)
        if crc & 0xffffffff != info.CRC:
            raise ValueError('Tiny ImageNet bytes differ from the verified original: '+name)
    return {'classes':len(manifest['class_ids']), 'train_images':manifest['train_images'],
            'validation_images':manifest['validation_images'], 'test_images':manifest['test_images'],
            'all_archive_files_byte_verified':True, 'validation_annotation_alignment_verified':True}


def ensure_tiny_imagenet(folder):
    """Validate full original data; recover incomplete extraction without deleting it."""
    folder = Path(folder).resolve()
    data = folder/'data'; data.mkdir(parents=True, exist_ok=True)
    data_root = data.resolve()
    target = data/'tiny-imagenet-200'
    if target.is_symlink() or not target.resolve().is_relative_to(data_root):
        raise ValueError('Tiny ImageNet recovery requires its own dataset directory inside data/.')
    archive = data/'tiny-imagenet-200.zip'
    if archive.is_file() and _tiny_digests(archive)[0] != TINY_IMAGENET_MD5:
        # Keep an existing mismatched download as recoverable evidence.
        archive.rename(data/('tiny-imagenet-200.invalid-'+uuid.uuid4().hex+'.zip'))
    download(TINY_IMAGENET_URL, archive)
    md5, sha256 = _tiny_digests(archive)
    if md5 != TINY_IMAGENET_MD5:
        raise ValueError('Official Tiny ImageNet ZIP checksum mismatch; no extraction/training performed.')
    recovered, quarantine = False, None
    with zipfile.ZipFile(archive) as z:
        manifest = _tiny_archive_manifest(z)
    try:
        evidence = _validate_tiny_tree(target, manifest)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print('Restoring complete original Tiny ImageNet data:', str(exc))
        staging = data/('.tiny-imagenet-repair-'+uuid.uuid4().hex)
        if not staging.resolve().is_relative_to(data_root): raise ValueError('Unsafe repair location.')
        staging.mkdir()
        safe_extract(archive, staging)
        replacement = staging/'tiny-imagenet-200'
        evidence = _validate_tiny_tree(replacement, manifest)
        if target.exists():
            quarantine = data/('tiny-imagenet-200.incomplete-'+uuid.uuid4().hex)
            # Resolve and check both absolute move targets before a directory move.
            if not all(p.resolve().is_relative_to(data_root) for p in [target, quarantine, replacement]):
                raise ValueError('Tiny ImageNet repair paths leave the intended data directory.')
            target.rename(quarantine)
        try:
            replacement.replace(target)
        except BaseException:
            if quarantine is not None and not target.exists(): quarantine.rename(target)
            raise
        recovered = True
    evidence.update(source_url=TINY_IMAGENET_URL, archive_md5=md5, archive_sha256=sha256,
                    checked_utc=datetime.now(timezone.utc).isoformat(), recovered_extraction=recovered,
                    preserved_incomplete_directory=None if quarantine is None else str(quarantine),
                    provider_course_completion_claimed=False)
    results = folder/'results'; results.mkdir(parents=True, exist_ok=True)
    record = results/'tiny-imagenet-integrity.json'
    temporary = record.with_suffix('.writing')
    temporary.write_text(json.dumps(evidence, indent=2), encoding='utf-8'); temporary.replace(record)
    print('Verified original Tiny ImageNet:', evidence['train_images'], 'train,', evidence['validation_images'], 'validation images.')
    return target


def setup_course(root, relative_folder, profile, notebook, use_drive=True, install=True):
    root = Path(root).resolve()
    folder = root / relative_folder
    os.chdir(folder)
    for p in [folder, root, root / '04_fastai_part2']:
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    if profile == 'google':
        if 'keras' in sys.modules and sys.modules['keras'].backend.backend() != 'torch':
            raise RuntimeError('Start a new runtime before switching from TensorFlow to this Keras/PyTorch notebook.')
        os.environ['KERAS_BACKEND'] = 'torch'
    elif profile == 'fairness':
        if 'tensorflow' in sys.modules or 'keras' in sys.modules:
            raise RuntimeError('Run fairness in a fresh Colab runtime so legacy Keras is selected before TensorFlow loads.')
        os.environ['TF_USE_LEGACY_KERAS'] = '1'
        os.environ['KERAS_BACKEND'] = 'tensorflow'
    elif profile == 'tensorflow' or notebook.startswith('TF_') or '_tf_' in notebook:
        os.environ['KERAS_BACKEND'] = 'tensorflow'
    if install:
        install_profile(profile)
    saved = Path('/content/drive/MyDrive/HaiLong_Colab_Results')
    on_drive = use_drive and Path('/content/drive/MyDrive').is_dir()
    for name in ['results', 'models']:
        destination = folder / name
        if on_drive:
            persistent = saved / relative_folder / name
            persistent.mkdir(parents=True, exist_ok=True)
            if not destination.exists():
                destination.symlink_to(persistent, target_is_directory=True)
            elif not destination.is_symlink():
                print(f'{destination} is local. The final cell will copy its files to Drive.')
        destination.mkdir(parents=True, exist_ok=True)
    (folder / 'data').mkdir(exist_ok=True)
    if profile == 'part2':
        # Original course notebooks share these data across fresh Colab runtimes.
        download('https://raw.githubusercontent.com/mnielsen/neural-networks-and-deep-learning/master/data/mnist.pkl.gz',
                 folder / 'data/mnist.pkl.gz')
        import torch
        if not torch.cuda.is_available():
            raise RuntimeError('This original Part 2 notebook contains CUDA exercises. Select Runtime > Change runtime type > T4 GPU, then rerun.')
        if notebook in TINY_IMAGENET_NOTEBOOKS:
            ensure_tiny_imagenet(folder)
        prerequisites = {
            '18_fid.ipynb': ['data_aug2.pkl', 'fashion_ddpm_mp.pkl'],
            '19_DDPM_v3.ipynb': ['data_aug2.pkl'],
            '20_DDIM.ipynb': ['data_aug2.pkl', 'fashion_ddpm3_25.pkl'],
            '22_cosine.ipynb': ['data_aug2.pkl'], '22_noise-pred.ipynb': ['data_aug2.pkl'],
            '23_karras.ipynb': ['data_aug2.pkl'], '25_superres.ipynb': ['inettiny-custom-25'],
            '26_diffusion_unet.ipynb': ['data_aug2.pkl'], '28_diffusion-attn-cond.ipynb': ['data_aug2.pkl'],
        }
        missing = [f for f in prerequisites.get(notebook, []) if not (folder/'models'/f).is_file()]
        if missing:
            raise FileNotFoundError('Train the prerequisite notebooks first; missing models: '+', '.join(missing)+'. See RUN_ORDER.md.')
        if notebook.startswith('31_'):
            data_root=folder/'data/ILSVRC'
            missing_metadata=[name for name in ['imagenet_lsvrc_2015_synsets.txt','words.txt'] if not (data_root/name).is_file()]
            if missing_metadata: raise FileNotFoundError('ImageNet metadata files required: '+', '.join(missing_metadata))
            mode=os.environ.get('IMAGENET_SOURCE','local')
            if mode=='local':
                if not (data_root/'Data/CLS-LOC').is_dir():
                    raise FileNotFoundError('The local ImageNet experiment requires your licensed data/ILSVRC/Data/CLS-LOC folder.')
            elif mode=='hf_stream':
                if os.environ.get('IMAGENET_APPROVED_ACCESS')!='1' or not os.environ.get('HF_TOKEN','').strip():
                    raise RuntimeError('ImageNet streaming requires explicitly approved access and a nonempty scoped HF_TOKEN. No dataset request was made.')
            else: raise ValueError('IMAGENET_SOURCE must be local or hf_stream.')
    versions = {}
    for name in ['numpy','pandas','torch','torchvision','tensorflow','keras','fastai','fastcore','accelerate','datasets','diffusers','transformers']:
        try: versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError: pass
    run = {'notebook': notebook, 'folder': str(folder), 'started_utc': datetime.now(timezone.utc).isoformat(),
           'quick_run': os.environ.get('COURSE_SMOKE') == '1', 'versions': versions,
           'drive_enabled': on_drive, 'status': 'started'}
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:6]
    record = folder / 'results' / f'{Path(notebook).stem}-{stamp}.json'
    context = {'root': root, 'folder': folder, 'record': record, 'run': run,
               'saved': saved/relative_folder, 'drive': on_drive,
               'artifact_budget_paths':[saved,Path('/content/drive/MyDrive/HaiLong_Course_Progress/2026-10-03')],
               'runtime_storage_path':Path('/content')}
    # Hooks may only write checkpoints after the caller's Drive context exists.
    from course_persistence import register_hooks
    run['training_persistence'] = register_hooks(context, profile)
    record.write_text(json.dumps(run, indent=2), encoding='utf-8')
    print('Exercise folder:', folder)
    print('Run mode:', 'QUICK CHECK (reduced/synthetic where documented)' if run['quick_run'] else 'FULL EXERCISE')
    print('Results:', (folder/'results').resolve())
    return context


def finish_run(context):
    run = context['run']
    run['finished_utc'] = datetime.now(timezone.utc).isoformat()
    run['status'] = 'reached_final_cell'
    run['provider_course_completion_claimed'] = False
    # Reaching this cell is not proof the learner ran every previous cell.
    context['record'].write_text(json.dumps(run, indent=2), encoding='utf-8')
    if context['drive']:
        for name in ['results', 'models']:
            src, dst = context['folder']/name, context['saved']/name
            if src.resolve() != dst.resolve():
                shutil.copytree(src, dst, dirs_exist_ok=True)
        from course_persistence import collect_reuse_evidence
        collect_reuse_evidence(context)
    print('Saved run settings. Save the notebook in Colab to keep its cell outputs.')


class LocalExperiment:
    """Small local replacement for the Comet methods used by the MIT notebooks."""
    def __init__(self, project_name='mit_exercise', **kwargs):
        self.path = Path('results') / (project_name + '-' + uuid.uuid4().hex[:8] + '.jsonl')
    def _write(self, kind, data):
        with self.path.open('a', encoding='utf-8') as f:
            f.write(json.dumps({'kind': kind, **data}, default=str) + '\n')
    def log_metric(self, name, value, **kwargs): self._write('metric', {'name': name, 'value': float(value), **kwargs})
    def log_parameter(self, name, value): self._write('parameter', {'name': name, 'value': value})
    def log_figure(self, figure=None, **kwargs):
        import matplotlib.pyplot as plt
        dest = self.path.with_name(self.path.stem + '-' + uuid.uuid4().hex[:6] + '.png')
        (figure if hasattr(figure, 'savefig') else plt).savefig(dest)
    def flush(self): pass
    def end(self): self._write('end', {})


def competition_data(name):
    """Use files the learner downloaded after accepting the competition rules."""
    folder = Path('data') / name
    required = ['train_images', 'test_images', 'sample_submission.csv'] if name == 'paddy-disease-classification' else ['train.csv', 'test.csv']
    if not all((folder / f).exists() for f in required):
        archive = Path('/content/drive/MyDrive') / f'{name}.zip'
        if not archive.exists():
            from google.colab import files
            print(f'Download the data from https://www.kaggle.com/competitions/{name}/data, then upload its ZIP.')
            uploaded = files.upload()
            archives = [Path(n) for n in uploaded if n.endswith('.zip')]
            if len(archives) != 1: raise ValueError('Select exactly one competition ZIP.')
            archive = archives[0]
        safe_extract(archive, folder)
    missing = [f for f in required if not (folder/f).exists()]
    if missing: raise FileNotFoundError(f'Incomplete competition data in {folder}: {missing}')
    return folder
