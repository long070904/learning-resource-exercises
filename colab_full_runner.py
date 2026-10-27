"""Run the real course notebooks in Colab and persist execution evidence per cell.

This runner never equates a prepared file, a final-cell marker, or a reduced
practice run with completion of the original course.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys
import traceback
import argparse
import importlib.util
import time

import nbformat
from nbclient import NotebookClient

COURSE_ROOT = Path('/content/HaiLong_Colab_Exercises')
DRIVE_ROOT = Path('/content/drive/MyDrive')
PROGRESS_ROOT = DRIVE_ROOT / 'HaiLong_Course_Progress/2026-10-03'
MANIFEST = COURSE_ROOT / 'exercise_manifest.json'
KERNEL_NAME = os.environ.get('HAILONG_KERNEL_NAME', 'hailong-full')
RUNNER_EVIDENCE_VERSION = 2
PROBE_TAG = 'hailong-runner-evidence'
PROBE_PREFIX = '__HAILONG_RUNTIME_EVIDENCE__'
IMAGENET_NOTEBOOK = '04_fastai_part2/31_imgnet_latents-widish.ipynb'
SERVICE_NOTEBOOK = '02_mit_6s191/08_lab3_service_continuation.ipynb'
SCOPED_INPUTS = {
    IMAGENET_NOTEBOOK: {'HF_TOKEN', 'IMAGENET_SOURCE', 'IMAGENET_APPROVED_ACCESS', 'IMAGENET_HF_REVISION'},
    SERVICE_NOTEBOOK: {'OPENROUTER_API_KEY', 'OPIK_API_KEY', 'OPIK_WORKSPACE',
        'HAILONG_AUTHORIZE_LAB3_SERVICES', 'HAILONG_LAB3_JUDGE_MODEL', 'HAILONG_ALLOW_PAID_LAB3_JUDGE'},
}


def notebook_environment(relative_path, approved_inputs=None):
    """Credentials are scoped to one explicitly configured child, never records."""
    environment = os.environ.copy()
    for key in set().union(*SCOPED_INPUTS.values()) | {'HUGGING_FACE_HUB_TOKEN', 'HUGGINGFACE_HUB_TOKEN'}:
        environment.pop(key, None)
    allowed = SCOPED_INPUTS.get(relative_path, set())
    supplied = approved_inputs or {}
    if set(supplied) - allowed:
        raise ValueError('The supplied child inputs are not permitted for this notebook.')
    environment.update({key: str(value) for key, value in supplied.items()})
    environment['COURSE_SMOKE'] = '0'
    return environment


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def atomic_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.writing')
    temp.write_text(text, encoding='utf-8')
    temp.replace(path)


def save_json(path, value):
    atomic_text(path, json.dumps(value, indent=2, ensure_ascii=False, default=str) + '\n')


def source_code_cells(nb):
    """Blank placeholders are deliberately not executed by nbclient."""
    return [c for c in nb.cells if c.cell_type == 'code' and c.source.strip()
            and PROBE_TAG not in c.metadata.get('tags', [])]


def cell_counts(nb):
    cells = source_code_cells(nb)
    executed = [c for c in cells if c.execution_count is not None]
    failed = [c for c in executed if any(o.output_type == 'error' for o in c.outputs)]
    return {'executed_code_cells': len(executed),
            'successfully_executed_code_cells': len(executed) - len(failed),
            'failed_code_cells': len(failed)}


def execution_location():
    # Tests and local invocations must not manufacture hosted-Colab evidence.
    try:
        is_colab = importlib.util.find_spec('google.colab') is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        is_colab = False
    return 'hosted_colab' if is_colab and Path('/content').is_dir() else 'local'


def fastai_evidence_state(old, check_artifact_hashes=True):
    relative = old.get('notebook', '')
    if not relative.startswith(('03_fastai/', '04_fastai_part2/')):
        return {'required': False, 'valid': True}
    state = {'required': True, 'valid': False, 'helper_match': False,
             'artifacts_present': False, 'dependency_metadata_match': False,
             'artifact_integrity_status': 'not_verified',
             'fresh_artifact_hash_validation_performed': False,
             'currently_reusable': None}
    try:
        spec = importlib.util.spec_from_file_location('_hailong_persistence_review', COURSE_ROOT / 'course_persistence.py')
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        evidence = old.get('runtime_evidence', {}).get('fastai_reuse_evidence', {})
        saved = DRIVE_ROOT / 'HaiLong_Colab_Results' / Path(relative).parts[0]
        state['helper_match'] = evidence.get('helper_sha256') == helper.helper_fingerprints(COURSE_ROOT, relative)
        if (evidence.get('contract_version') != helper.REUSE_CONTRACT_VERSION
                or evidence.get('notebook') != relative
                or evidence.get('source_sha256') != old.get('source_sha256')
                or not state['helper_match']
                or any(not fit.get('all_requested_epochs_observed') for fit in evidence.get('fits', []))):
            return state
        for item in evidence.get('artifact_index', []):
            if not item.get('required_for_reuse'):
                continue
            path = saved / item['relative_persistent_path']
            if (not path.resolve().is_relative_to(saved.resolve()) or not path.is_file()
                    or path.stat().st_size != item['bytes'] or not item.get('sha256')):
                return state
        expected = set(helper.SOURCE_EXPORTS.get(relative, []))
        actual = {a['relative_persistent_path'] for a in evidence.get('artifact_index', [])
                  if a.get('role') == 'original_source_export'}
        if expected != actual:
            return state
        state['artifacts_present'] = True
        dependencies = evidence.get('reuse_dependencies', [])
        expected_dependencies = helper.SOURCE_DEPENDENCIES.get(relative, [])
        if len(dependencies) != len(expected_dependencies):
            return state
        for producer, artifact in expected_dependencies:
            producer_saved = saved.parent / Path(producer).parts[0]
            manifest = helper._producer_manifest(producer_saved, producer)
            data = json.loads(manifest.read_text(encoding='utf-8'))
            source_hash = hashlib.sha256((COURSE_ROOT / producer).read_bytes()).hexdigest()
            if (data.get('source_sha256') != source_hash
                    or data.get('helper_sha256') != helper.helper_fingerprints(COURSE_ROOT, producer)):
                return state
            matches = [a for a in data.get('artifact_index', []) if a['relative_persistent_path'] == artifact]
            recorded = [d for d in dependencies if d.get('producer_notebook') == producer
                        and d.get('artifact_path') == str(producer_saved / artifact)]
            path = producer_saved / artifact
            if (len(matches) != 1 or len(recorded) != 1 or not path.is_file()
                    or path.stat().st_size != matches[0]['bytes']
                    or recorded[0].get('expected_sha256') != matches[0]['sha256']
                    or recorded[0].get('producer_source_sha256') != source_hash):
                return state
        state['dependency_metadata_match'] = True
        if check_artifact_hashes:
            state['valid'] = helper.verify_reuse_evidence(evidence, COURSE_ROOT, relative, saved)
            state['fresh_artifact_hash_validation_performed'] = True
            state['currently_reusable'] = state['valid']
            state['artifact_integrity_status'] = 'fresh_sha256_validation' if state['valid'] else 'sha256_validation_failed'
        else:
            state['valid'] = bool(old.get('artifact_integrity_checked_utc'))
            state['artifact_integrity_status'] = 'last_verified_at_execution_or_reuse'
            state['integrity_last_verified_utc'] = old.get('artifact_integrity_checked_utc')
    except (OSError, ValueError, KeyError, TypeError, AttributeError, ImportError):
        pass
    return state


def prior_execution_is_reusable(old, source_hash, output_path, check_fastai_artifacts=True):
    """A record alone is insufficient: its corresponding outputs must survive."""
    if not (old.get('status') == 'executed_without_errors'
            and old.get('source_sha256') == source_hash
            and old.get('runner_evidence_version') == RUNNER_EVIDENCE_VERSION
            and old.get('runtime_evidence', {}).get('quick_run') is False
            and output_path.is_file() and old.get('output_sha256')):
        return False
    try:
        return (hashlib.sha256(output_path.read_bytes()).hexdigest() == old['output_sha256']
                and fastai_evidence_state(old, check_fastai_artifacts)['valid'])
    except OSError:
        return False


def runtime_probe_cell():
    return nbformat.v4.new_code_cell(
        "# Added by the course runner: inspect the executed runtime, not coursework.\n"
        "import os as _hailong_os, json as _hailong_json, platform as _hailong_platform\n"
        "_hailong_evidence = {\n"
        "    'python': _hailong_platform.python_version(),\n"
        "    'quick_run': bool(globals().get('QUICK_RUN', False)),\n"
        "    'course_smoke': _hailong_os.environ.get('COURSE_SMOKE', '0'),\n"
        "    'keras_backend': _hailong_os.environ.get('KERAS_BACKEND'),\n"
        "    'legacy_keras': _hailong_os.environ.get('TF_USE_LEGACY_KERAS'),\n"
        "    'base_model_commit': getattr(getattr(globals().get('model'), 'config', None), '_commit_hash', None),\n"
        "}\n"
        "_hailong_context = globals().get('COLAB_CONTEXT')\n"
        "if _hailong_context and _hailong_context['folder'].relative_to(_hailong_context['root']).as_posix().startswith(('03_fastai', '04_fastai_part2')):\n"
        "    from course_persistence import collect_reuse_evidence as _hailong_collect\n"
        "    _hailong_evidence['fastai_reuse_evidence'] = _hailong_context['run'].get('reuse_evidence') or _hailong_collect(_hailong_context)\n"
        f"print({PROBE_PREFIX!r} + _hailong_json.dumps(_hailong_evidence))\n",
        metadata={'tags': [PROBE_TAG]})


def read_runtime_evidence(nb):
    for output in nb.cells[-1].get('outputs', []):
        if output.output_type == 'stream':
            for line in output.text.splitlines():
                if line.startswith(PROBE_PREFIX):
                    return json.loads(line[len(PROBE_PREFIX):])
    raise RuntimeError('Executed runtime mode could not be verified.')


class SavingClient(NotebookClient):
    def __init__(self, nb, output_path, row, progress_path, **kwargs):
        super().__init__(nb, **kwargs)
        self.saved_output_path = Path(output_path)
        self.progress_row = row
        self.saved_progress_path = Path(progress_path)
        self.last_partial_save = 0.0

    def process_message(self, msg, cell, cell_index):
        result = super().process_message(msg, cell, cell_index)
        if (msg['msg_type'] in {'stream', 'display_data', 'execute_result', 'update_display_data'}
                and time.monotonic() - self.last_partial_save >= 60):
            self.last_partial_save = time.monotonic()
            self.progress_row['active_cell_number'] = cell_index + 1
            self.progress_row['last_output_update_utc'] = utc_now()
            atomic_text(self.saved_output_path, nbformat.writes(self.nb))
            save_json(self.saved_progress_path, self.progress_row)
            print('SAVED ACTIVE CELL OUTPUT:', self.progress_row['notebook'],
                  cell_index + 1, self.progress_row['last_output_update_utc'], flush=True)
        return result

    async def async_execute_cell(self, cell, cell_index, execution_count=None,
                                 store_history=True):
        try:
            return await super().async_execute_cell(cell, cell_index,
                execution_count=execution_count, store_history=store_history)
        finally:
            self.progress_row['last_cell_index'] = cell_index
            self.progress_row['last_cell_number'] = cell_index + 1
            self.progress_row['last_update_utc'] = utc_now()
            self.progress_row.update(cell_counts(self.nb))
            atomic_text(self.saved_output_path, nbformat.writes(self.nb))
            save_json(self.saved_progress_path, self.progress_row)
            if cell.cell_type == 'code' and cell.source.strip():
                print('SAVED CELL:', self.progress_row['notebook'], cell_index + 1,
                      'executed:', self.progress_row['executed_code_cells'],
                      'errors:', self.progress_row['failed_code_cells'], flush=True)


def dataset_preflight(relative_path, environment=None):
    stem = Path(relative_path).name
    drive_root = DRIVE_ROOT
    if relative_path.startswith('03_fastai/') and stem.startswith(('10_', '11_', '12_', '13_')):
        data = COURSE_ROOT / '03_fastai/data/paddy-disease-classification'
        if not (drive_root / 'paddy-disease-classification.zip').is_file() and not (data / 'train_images').is_dir():
            return 'Original Paddy Disease Classification competition ZIP/data are required.'
    if relative_path.startswith('03_fastai/14_'):
        data = COURSE_ROOT / '03_fastai/data/us-patent-phrase-to-phrase-matching'
        if not (drive_root / 'us-patent-phrase-to-phrase-matching.zip').is_file() and not (data / 'train.csv').is_file():
            return 'Original US Patent Phrase Matching competition ZIP/data are required.'
    if relative_path == IMAGENET_NOTEBOOK:
        environment = environment if environment is not None else os.environ
        data = COURSE_ROOT / '04_fastai_part2/data/ILSVRC'
        if not all((data / name).is_file() for name in ('imagenet_lsvrc_2015_synsets.txt', 'words.txt')):
            return 'Original ImageNet synset and words metadata files are required for a verified label mapping.'
        mode = environment.get('IMAGENET_SOURCE', 'local')
        if mode == 'local' and not (data / 'Data/CLS-LOC').is_dir():
            return 'Original ImageNet CLS-LOC data are required; no substitute is used.'
        if mode == 'hf_stream' and not (
                environment.get('IMAGENET_APPROVED_ACCESS') == '1'
                and environment.get('HF_TOKEN', '').strip()):
            return 'Approved official ImageNet access and a scoped Hugging Face token are required for streaming.'
        if mode not in ('local', 'hf_stream'):
            return 'ImageNet source must be the original local input or approved official streaming input.'
    return None


def service_preflight(relative_path, environment=None):
    """Keep the official remote Lab 3 continuation gated in unattended batches."""
    if relative_path != SERVICE_NOTEBOOK:
        return None
    environment = environment if environment is not None else os.environ
    if environment.get('HAILONG_AUTHORIZE_LAB3_SERVICES') != '1':
        return ('service_authorization_required',
                'Official OpenRouter/Opik continuation requires explicit service authorization and configured keys.')
    if not all(environment.get(key) for key in ('OPENROUTER_API_KEY', 'OPIK_API_KEY')):
        return ('service_keys_required',
                'Configure OPENROUTER_API_KEY and OPIK_API_KEY through Colab Secrets; do not put keys in progress records.')
    judge = environment.get('HAILONG_LAB3_JUDGE_MODEL', 'google/gemma-2-9b-it:free')
    if not judge.endswith(':free') and environment.get('HAILONG_ALLOW_PAID_LAB3_JUDGE') != '1':
        return ('paid_service_authorization_required',
                'The selected judge is not a free model; separate authorization is required before paid requests.')
    return None


def run_one(entry, rerun=False, approved_inputs=None):
    relative = entry['path']
    if Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise ValueError('Manifest notebook paths must stay inside the course folder.')
    source = COURSE_ROOT / relative
    record_path = PROGRESS_ROOT / 'records' / Path(relative).with_suffix('.json')
    output_path = PROGRESS_ROOT / 'notebooks' / relative
    row = {'notebook': relative, 'source_sha256': None,
           'started_utc': utc_now(), 'status': 'started',
           'execution_location': execution_location(), 'quick_run': None,
           'requested_quick_run': False, 'run_action': 'attempted',
           'runner_evidence_version': RUNNER_EVIDENCE_VERSION,
           'provider_course_completion_claimed': False,
           'personal_understanding_or_authorship_claimed': False,
           'full_course_completion_claimed': False,
           'output_notebook_path': str(output_path), 'profile': entry['profile']}
    nb = None
    try:
        kernel_environment = notebook_environment(relative, approved_inputs)
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        row['source_sha256'] = source_hash
        if record_path.exists() and not rerun:
            try:
                old = json.loads(record_path.read_text(encoding='utf-8'))
            except (OSError, ValueError):
                old = {}
            if prior_execution_is_reusable(old, source_hash, output_path):
                if relative.startswith(('03_fastai/', '04_fastai_part2/')):
                    old['artifact_integrity_checked_utc'] = utc_now()
                    save_json(record_path, old)
                print('Already executed this exact source with saved outputs:', relative, flush=True)
                return {**old, 'run_action': 'reused_verified_outputs'}
        blocked = dataset_preflight(relative, kernel_environment)
        if blocked:
            row.update(status='dataset_required', reason=blocked)
            print('DATA REQUIRED:', relative, blocked, flush=True)
            return row
        service_gate = service_preflight(relative, kernel_environment)
        if service_gate:
            row.update(status=service_gate[0], reason=service_gate[1])
            print('SERVICE INPUT REQUIRED:', relative, service_gate[1], flush=True)
            return row
        nb = nbformat.read(source, as_version=4)
        nbformat.validate(nb)
        for cell in nb.cells:
            if cell.cell_type == 'code':
                cell.execution_count = None
                cell.outputs = []
        row['total_source_code_cells'] = sum(c.cell_type == 'code' for c in nb.cells)
        row['expected_code_cells'] = len(source_code_cells(nb))
        row['empty_code_cells'] = row['total_source_code_cells'] - row['expected_code_cells']
        row['tagged_skipped_nonempty_code_cells'] = sum(
            'skip-execution' in c.metadata.get('tags', []) for c in source_code_cells(nb))
        if not row['expected_code_cells']:
            raise RuntimeError('Notebook has no executable source code cells.')
        nb.cells.append(runtime_probe_cell())
        row.update(status='running', kernel_name=KERNEL_NAME)
        os.environ['COURSE_SMOKE'] = '0'
        save_json(record_path, row)
        atomic_text(output_path, nbformat.writes(nb))
        print('\nSTART FULL NOTEBOOK:', relative, utc_now(), flush=True)
        client = SavingClient(nb, output_path, row, record_path,
            timeout=None, startup_timeout=180, kernel_name=KERNEL_NAME,
            allow_errors=False, force_raise_errors=True, record_timing=True,
            resources={'metadata': {'path': str(source.parent)}})
        client.execute(env=kernel_environment)
        executed = cell_counts(nb)['executed_code_cells']
        errors = [o for c in nb.cells if c.cell_type == 'code' for o in c.outputs if o.output_type == 'error']
        if executed != row['expected_code_cells'] or errors:
            raise RuntimeError('Not every nonempty source code cell executed successfully.')
        evidence = read_runtime_evidence(nb)
        row['runtime_evidence'] = evidence
        row['quick_run'] = evidence['quick_run']
        if evidence['quick_run'] or evidence['course_smoke'] not in ('0', ''):
            raise RuntimeError('Notebook selected a reduced/QUICK_RUN mode; full execution evidence is not valid.')
        if relative.startswith(('03_fastai/', '04_fastai_part2/')):
            artifact_state = fastai_evidence_state(row)
            if not artifact_state['valid']:
                raise RuntimeError('Full fast.ai fit/export/dependency evidence could not be verified: ' + json.dumps(artifact_state))
            row['artifact_integrity_checked_utc'] = utc_now()
        row.update(status='executed_without_errors', executed_code_cells=executed,
                   run_action='executed',
                   completion_interpretation='Full-mode notebook execution passed. Check its course/task evidence and any required learner activity separately.')
        print('EXECUTED:', relative, 'all', executed, 'code cells', flush=True)
    except KeyboardInterrupt:
        row.update(status='interrupted', error='Execution interrupted; partial outputs preserved.')
        raise
    except Exception as exc:
        row.update(status='execution_failed', exception_type=type(exc).__name__,
                   error=str(exc), traceback=traceback.format_exc())
        print('FAILED:', relative, type(exc).__name__, str(exc)[-2000:], flush=True)
    finally:
        # A verified reuse retains its original record and execution timestamp.
        if row['status'] != 'started' or nb is not None:
            row['finished_utc'] = utc_now()
            if nb is not None:
                atomic_text(output_path, nbformat.writes(nb))
                row['output_sha256'] = hashlib.sha256(output_path.read_bytes()).hexdigest()
                row.update(cell_counts(nb))
            save_json(record_path, row)
    return row


def run_all(prefix=None, rerun=False, per_notebook_inputs=None):
    if not DRIVE_ROOT.is_dir():
        raise RuntimeError('Connect Drive before running; checkpoint persistence is required.')
    if not MANIFEST.is_file():
        raise FileNotFoundError('Upload and extract the repaired course ZIP first.')
    os.environ['COURSE_SMOKE'] = '0'
    os.environ['WANDB_MODE'] = 'offline'
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    entries = json.loads(MANIFEST.read_text(encoding='utf-8'))
    if prefix:
        entries = [e for e in entries if e['path'].startswith(prefix)]
    # Execute the full Part 1 sources first; the shorter earlier companions
    # remain additional work. Lessons 9-10 precede from-scratch diffusion.
    def part1_rank(path):
        if not path.startswith('03_fastai/'):
            return 0
        if Path(path).name.startswith(tuple(f'{i:02d}_original_' for i in range(17, 25))):
            return 0
        number = Path(path).name.split('_', 1)[0]
        return 1 if number.isdigit() and int(number) >= 8 else 2
    entries.sort(key=lambda e: (
        0 if e['path'].startswith('01_google_mlcc/') else
        1 if e['path'].startswith('02_mit_6s191/') else
        2 if e['path'].startswith('03_fastai/') else
        3 if '/diffusion_intro/' in e['path'] else 4,
        part1_rank(e['path']), e['path']))
    PROGRESS_ROOT.mkdir(parents=True, exist_ok=True)
    rows = []
    for entry in entries:
        rows.append(run_one(entry, rerun=rerun,
            approved_inputs=(per_notebook_inputs or {}).get(entry['path'])))
        counts = {}
        for row in rows:
            counts[row['status']] = counts.get(row['status'], 0) + 1
        save_json(PROGRESS_ROOT / 'execution_summary.json', {
            'updated_utc': utc_now(), 'scope_prefix': prefix,
            'requested_notebooks': len(entries), 'processed_notebooks': len(rows),
            'counts': counts, 'notebooks': rows,
            'all_coursework_complete': False})
        save_overall_progress()
        print('SAVED SUMMARY:', counts, flush=True)
    return rows


def save_overall_progress():
    """Aggregate every manifest entry, independently of the last prefix run."""
    entries = json.loads(MANIFEST.read_text(encoding='utf-8'))
    rows, counts, course_counts = [], {}, {}
    current_records = 0
    found_records = 0
    verified_successes = 0
    for entry in entries:
        relative = entry['path']
        source = COURSE_ROOT / relative
        record_path = PROGRESS_ROOT / 'records' / Path(relative).with_suffix('.json')
        output_path = PROGRESS_ROOT / 'notebooks' / relative
        course = Path(relative).parts[0]
        course_counts[course] = course_counts.get(course, 0) + 1
        row = {'notebook': relative, 'profile': entry['profile'],
               'status': 'not_started', 'current_source_record': False,
               'verified_successful_execution': False}
        if record_path.is_file():
            found_records += 1
            try:
                old = json.loads(record_path.read_text(encoding='utf-8'))
                if not isinstance(old, dict):
                    raise ValueError('Progress record is not an object.')
                row['recorded_status'] = old.get('status')
                row['record_finished_utc'] = old.get('finished_utc')
                if not source.is_file():
                    row['status'] = 'source_missing'
                else:
                    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
                    row['source_sha256'] = source_hash
                    if old.get('source_sha256') != source_hash:
                        row['status'] = 'stale_source_record'
                    else:
                        row['current_source_record'] = True
                        current_records += 1
                        if old.get('status') == 'executed_without_errors':
                            verified = prior_execution_is_reusable(old, source_hash, output_path, check_fastai_artifacts=False)
                            row['artifact_evidence'] = fastai_evidence_state(old, check_artifact_hashes=False)
                            row['verified_successful_execution'] = verified
                            row['status'] = 'executed_without_errors' if verified else 'saved_execution_evidence_invalid'
                            verified_successes += int(verified)
                        else:
                            row['status'] = old.get('status') or 'invalid_record'
            except (OSError, ValueError, TypeError):
                row['status'] = 'invalid_record'
        elif not source.is_file():
            row['status'] = 'source_missing'
        counts[row['status']] = counts.get(row['status'], 0) + 1
        rows.append(row)
    summary = {'updated_utc': utc_now(), 'scope': 'all_manifest_notebooks',
        'expected_manifest_notebooks': len(entries), 'course_notebook_counts': course_counts,
        'persistent_manifest_records_found': found_records,
        'current_source_record_count': current_records,
        'verified_successful_notebooks': verified_successes,
        'counts': counts, 'notebooks': rows,
        'all_coursework_complete': False,
        'provider_course_completion_claimed': False,
        'interpretation': 'Current source/helper records and saved output hashes are checked across the entire manifest. Fast.ai artifact existence, size, and dependency metadata are checked here; full artifact hashes are validated after execution and before actual reuse, with the last verification time recorded. Execution success does not certify all course tasks or learner activities.'}
    save_json(PROGRESS_ROOT / 'overall_progress.json', summary)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('prefix', nargs='?', help='Optional course folder prefix')
    parser.add_argument('--rerun', action='store_true', help='Run even verified unchanged sources again')
    arguments = parser.parse_args()
    run_all(prefix=arguments.prefix, rerun=arguments.rerun)
