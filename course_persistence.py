"""Drive-backed state checkpoints for genuine fastai/miniai training fits.

Hooks add observation callbacks only. Recovery is explicit, restricted to a
completed epoch of the same source/architecture/optimizer/fit configuration,
and requires the caller to confirm the input data have not changed.
"""
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
import hashlib
import inspect
import json
import os
import random
import re
import shutil
import sys
import time
import uuid

_context = None
_ipython_hook = None
_DEMO_NAMES = {'singlebatchcb', 'lrfinder', 'lrfindercb', 'lrfindercallback'}
REUSE_CONTRACT_VERSION = 1
# Original exported models are retained separately from hook checkpoints.
SOURCE_EXPORTS = {
    '03_fastai/00_image_classifier.ipynb':['results/image_classifier.pkl'],
    '03_fastai/08_chapter4_coding_questions_and_mnist.ipynb':['models/mnist_full.pt'],
    '03_fastai/09_wearable_training_and_ethics.ipynb':['results/wearable_fastai.pkl'],
    '03_fastai/15_collaborative_filtering.ipynb':[f'models/{name}_full_movielens.pt' for name in ['nn_mse','nn_cross_entropy','nn_mse_with_genres']],
    '03_fastai/16_convolutions.ipynb':[f'models/{norm}_{order}_seed{seed}.pt' for seed in [42,43,44]
                                     for norm,order in [('none','norm_relu'),('batch','relu_norm'),('batch','norm_relu'),
                                                        ('group','norm_relu'),('instance','norm_relu'),('layer','norm_relu')]],
    '03_fastai/17_original_00_bird_classifier.ipynb':['models/17_original_00_bird_classifier/bird_classifier.pkl'],
    '03_fastai/19_original_02_save_pet_model.ipynb':['models/19_original_02_save_pet_model/model.pkl'],
    '03_fastai/22_original_05_titanic_from_scratch.ipynb':[f'models/22_original_05_titanic_from_scratch/manual_experiment_{i:02d}.pt' for i in range(1,7)],
    '03_fastai/23_original_06_titanic_framework.ipynb':['models/23_original_06_titanic_framework/standalone.pkl']+[f'models/23_original_06_titanic_framework/ensemble_{i}.pkl' for i in range(1,6)],
    '04_fastai_part2/14_augment.ipynb':['models/'+f for f in ['data_aug.pkl','randcopy1.pkl','randcopy2.pkl','data_aug2.pkl']],
    '04_fastai_part2/15_DDPM.ipynb':['models/fashion_ddpm.pkl'],
    '04_fastai_part2/17_DDPM_v2.ipynb':['models/fashion_ddpm2.pkl','models/fashion_ddpm_mp.pkl'],
    '04_fastai_part2/19_DDPM_v3.ipynb':['models/fashion_ddpm3_25.pkl'],
    '04_fastai_part2/22_cosine.ipynb':['models/fashion_cos.pkl'],
    '04_fastai_part2/22_noise-pred.ipynb':['models/noisepred_sig.pkl','models/fashion_no-t.pkl'],
    '04_fastai_part2/24_imgnet_tiny-wide.ipynb':['models/inettiny-wide-50'],
    '04_fastai_part2/24_imgnet_tiny-widish.ipynb':['models/inettiny-widish-50'],
    '04_fastai_part2/24_imgnet_tiny.ipynb':['models/inettiny-basic-25','models/inettiny-custom-25','models/inettiny-trivaug-50'],
    '04_fastai_part2/24a_imgnet_tiny-200.ipynb':['models/inettiny-trivaug-200'],
    '04_fastai_part2/25_superres.ipynb':['models/superres-pcp.pkl','models/superres-cross.pkl'],
    '04_fastai_part2/30_lsun_diffusion-simple.ipynb':['models/lsun_diffusion-prog-64.pkl'],
    '04_fastai_part2/31_imgnet_latents-widish.ipynb':['models/imgnet-latents'],
}
SOURCE_DEPENDENCIES = {
    '03_fastai/02_export_and_reload_model.ipynb':[('03_fastai/00_image_classifier.ipynb','results/image_classifier.pkl')],
    '04_fastai_part2/18_fid.ipynb':[('04_fastai_part2/14_augment.ipynb','models/data_aug2.pkl'),('04_fastai_part2/17_DDPM_v2.ipynb','models/fashion_ddpm_mp.pkl')],
    '04_fastai_part2/20_DDIM.ipynb':[('04_fastai_part2/14_augment.ipynb','models/data_aug2.pkl'),('04_fastai_part2/19_DDPM_v3.ipynb','models/fashion_ddpm3_25.pkl')],
    '04_fastai_part2/25_superres.ipynb':[('04_fastai_part2/24_imgnet_tiny.ipynb','models/inettiny-custom-25')],
}
for _consumer in ['19_DDPM_v3.ipynb','22_cosine.ipynb','22_noise-pred.ipynb','23_karras.ipynb','26_diffusion_unet.ipynb','28_diffusion-attn-cond.ipynb']:
    SOURCE_DEPENDENCIES['04_fastai_part2/'+_consumer]=[('04_fastai_part2/14_augment.ipynb','models/data_aug2.pkl')]


def helper_fingerprints(root, relative):
    """Inputs used by future fast.ai records; other courses keep legacy reuse."""
    root=Path(root)
    if not relative.startswith(('03_fastai/','04_fastai_part2/')): return {}
    paths=[root/'colab_runtime.py',root/'course_persistence.py']
    paths+=list((root/'03_fastai').glob('*.py'))
    if relative.startswith('04_fastai_part2/'):
        paths+=list((root/'04_fastai_part2/miniai').glob('*.py'))
    return {p.relative_to(root).as_posix():_file_hash(p) for p in sorted(paths) if p.is_file()}


def _relative_notebook(context):
    return (context['folder'].relative_to(context['root'])/context['run']['notebook']).as_posix()


def _producer_manifest(saved_course, producer):
    return Path(saved_course)/'results/source_artifacts'/ (Path(producer).stem+'.json')


def _read_dependency(root, results_root, producer, artifact, consumer):
    course=Path(producer).parts[0]; saved_course=Path(results_root)/course
    path=saved_course/artifact; manifest=_producer_manifest(saved_course,producer)
    if not manifest.is_file(): raise FileNotFoundError(f'Run the full prerequisite {producer}; verified source-export provenance is missing.')
    data=json.loads(manifest.read_text(encoding='utf-8'))
    if data.get('helper_sha256')!=helper_fingerprints(root,producer) or data.get('source_sha256')!=_file_hash(Path(root)/producer):
        raise ValueError(f'Prerequisite {producer} was produced with different source/helpers; rerun it in full.')
    matches=[v for v in data.get('artifact_index',[]) if v['relative_persistent_path']==artifact]
    if len(matches)!=1 or not path.is_file() or _file_hash(path)!=matches[0]['sha256']:
        raise ValueError(f'Prerequisite artifact {producer}: {artifact} is missing or changed; rerun its producer.')
    return {'producer_notebook':producer,'artifact_path':str(path),'expected_sha256':matches[0]['sha256'],
            'producer_source_sha256':data['source_sha256'],'consumer_notebook':consumer}


def prepare_reuse_evidence(context):
    relative=_relative_notebook(context)
    if not relative.startswith(('03_fastai/','04_fastai_part2/')): return
    results_root=context['saved'].parent
    deps=[_read_dependency(context['root'],results_root,p,a,relative) for p,a in SOURCE_DEPENDENCIES.get(relative,[])]
    context['source_export_start']={a:(context['saved']/a).stat().st_mtime_ns if (context['saved']/a).is_file() else None
                                  for a in SOURCE_EXPORTS.get(relative,[])}
    context['run']['reuse_dependencies']=deps
    context['run']['helper_sha256']=helper_fingerprints(context['root'],relative)


def collect_reuse_evidence(context):
    """Called after original cells/exports, or by the runner's final evidence cell."""
    relative=_relative_notebook(context)
    if not relative.startswith(('03_fastai/','04_fastai_part2/')): return {}
    run=context['run']; source=_file_hash(context['root']/relative)
    if run.get('helper_sha256')!=helper_fingerprints(context['root'],relative):
        raise ValueError('Course helpers changed while this notebook ran.')
    if any(not fit['all_requested_epochs_observed'] for fit in run.get('fits',[])):
        raise RuntimeError('A required non-demonstration fit did not finish its complete original schedule.')
    exports=[]
    for a in SOURCE_EXPORTS.get(relative,[]):
        path=context['saved']/a
        if not path.is_file(): raise FileNotFoundError('Required original source export missing: '+str(path))
        if context.get('source_export_start',{}).get(a)==path.stat().st_mtime_ns:
            raise ValueError('Required export was not written by this run: '+str(path))
        exports.append({'relative_persistent_path':a,'sha256':_file_hash(path),'bytes':path.stat().st_size,
                        'producer_notebook':relative,'producer_run_id':run.get('started_utc'),
                        'producer_source_sha256':source,'role':'original_source_export','required_for_reuse':True,
                        'consumers':[c for c,ds in SOURCE_DEPENDENCIES.items() if (relative,a) in ds]})
    # Current fits were appended as they completed; no old/user files are claimed.
    index=[a for a in run.get('artifact_index',[]) if a.get('role')!='original_source_export']+exports
    run['artifact_index']=index
    evidence={'contract_version':REUSE_CONTRACT_VERSION,'notebook':relative,'source_sha256':source,
              'helper_sha256':run['helper_sha256'],'persistent_course_root':str(context['saved']),
              'artifact_index':index,'reuse_dependencies':run.get('reuse_dependencies',[]),
              'fits':run.get('fits',[]),'provider_course_completion_claimed':False}
    if exports:
        manifest=_producer_manifest(context['saved'],relative);manifest.parent.mkdir(parents=True,exist_ok=True)
        _atomic_json(evidence,manifest)
    run['reuse_evidence']=evidence
    _atomic_json(run,context['record'])
    return evidence


def verify_reuse_evidence(evidence, root, relative, persistent_course_root):
    """Pure file validation for the root runner; no training/importing torch."""
    if not relative.startswith(('03_fastai/','04_fastai_part2/')): return True
    try:
        if (evidence.get('contract_version')!=REUSE_CONTRACT_VERSION or evidence.get('notebook')!=relative
            or evidence.get('source_sha256')!=_file_hash(Path(root)/relative)
            or evidence.get('helper_sha256')!=helper_fingerprints(root,relative)): return False
        saved=Path(persistent_course_root).resolve()
        if any(not fit.get('all_requested_epochs_observed') for fit in evidence.get('fits',[])): return False
        for item in evidence.get('artifact_index',[]):
            if not item.get('required_for_reuse'): continue
            path=saved/item['relative_persistent_path']
            if not path.resolve().is_relative_to(saved) or not path.is_file() or _file_hash(path)!=item['sha256']: return False
        expected=set(SOURCE_EXPORTS.get(relative,[]))
        present={a['relative_persistent_path'] for a in evidence.get('artifact_index',[]) if a.get('role')=='original_source_export'}
        if expected!=present: return False
        current=[_read_dependency(root,saved.parent,p,a,relative) for p,a in SOURCE_DEPENDENCIES.get(relative,[])]
        return current==evidence.get('reuse_dependencies',[])
    except (OSError,ValueError,KeyError,TypeError): return False


def reuse_evidence_summary(evidence, root, relative, persistent_course_root):
    """Cheap aggregate status; deliberately does NOT claim current byte integrity."""
    result={'helper_match':False,'required_artifacts_present_with_recorded_sizes':False,
            'artifact_integrity_status':'last_verified_at_execution_or_reuse',
            'fresh_artifact_hash_validation_performed':False,'currently_reusable':None}
    if not relative.startswith(('03_fastai/','04_fastai_part2/')): return result
    try:
        result['helper_match']=evidence.get('helper_sha256')==helper_fingerprints(root,relative)
        saved=Path(persistent_course_root).resolve();present=True
        for a in evidence.get('artifact_index',[]):
            if a.get('required_for_reuse'):
                path=saved/a['relative_persistent_path']
                present &= path.resolve().is_relative_to(saved) and path.is_file() and path.stat().st_size==a['bytes']
        for dep in evidence.get('reuse_dependencies',[]):present &= Path(dep['artifact_path']).is_file()
        result['required_artifacts_present_with_recorded_sizes']=bool(present) and evidence.get('contract_version')==REUSE_CONTRACT_VERSION
    except (OSError,ValueError,KeyError,TypeError): pass
    return result


def _ref(obj):
    cls = obj if isinstance(obj, type) else type(obj)
    return f'{cls.__module__}.{cls.__qualname__}'


def _stable(value):
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if isinstance(value, dict):
        return {str(k): _stable(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_stable(v) for v in value]
    if callable(value):
        return {'callable': getattr(value, '__module__', '')+'.'+getattr(value, '__qualname__', type(value).__qualname__),
                'repr': re.sub(r'0x[0-9a-fA-F]+', '<address>', repr(value))}
    return {'class': _ref(value), 'repr': re.sub(r'0x[0-9a-fA-F]+', '<address>', repr(value))}


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


def _cpu(value):
    import torch
    if isinstance(value, torch.Tensor): return value.detach().cpu()
    if isinstance(value, dict): return {k: _cpu(v) for k, v in value.items()}
    if isinstance(value, list): return [_cpu(v) for v in value]
    if isinstance(value, tuple): return tuple(_cpu(v) for v in value)
    return value


def _architecture(model):
    return {'class': _ref(model), 'repr': repr(model),
            'state': {k: {'shape': list(v.shape), 'dtype': str(v.dtype)} for k, v in model.state_dict().items()},
            'trainable': {k: p.requires_grad for k, p in model.named_parameters()}}


def _callbacks(value):
    if value is None: return []
    if isinstance(value, (list, tuple)) or type(value).__name__ == 'L': return list(value)
    return [value]


def _is_demo(cbs):
    return any(base.__name__.lower() in _DEMO_NAMES for cb in cbs for base in type(cb).__mro__)


def _optimizer_groups(opt):
    if hasattr(opt, 'param_lists'): return [len(group) for group in opt.param_lists]
    if _teaching_optimizer(opt): return [len(opt.params)]
    return [len(group['params']) for group in opt.param_groups]


def _teaching_optimizer(opt):
    # Lesson 12 deliberately builds these optimizers without a state_dict API.
    return (not hasattr(opt, 'state_dict') and type(opt).__name__ in {'SGD','RMSProp','Adam'}
            and hasattr(opt, 'params') and hasattr(opt, 'i') and hasattr(opt, 'opt_step')
            and hasattr(opt, 'reg_step') and all(hasattr(opt, k) for k in ['lr','wd']))


def _optimizer_state(opt):
    if opt is None: return None
    if hasattr(opt, 'state_dict'): return _cpu(opt.state_dict())
    if not _teaching_optimizer(opt): raise TypeError('The optimizer has no supported checkpoint API.')
    attributes = {k:_cpu(v) for k,v in vars(opt).items() if k != 'params'}
    allowed = {'lr','wd','i','sqr_mom','eps','beta1','beta2'}
    if set(attributes)-allowed: raise ValueError('Teaching optimizer state has unknown attributes; recovery cannot be guaranteed.')
    return {'teaching_optimizer_schema':1, 'class':_ref(opt), 'attributes':attributes,
            'parameter_moments':[{k:_cpu(getattr(p,k)) for k in ['avg','sqr_avg'] if hasattr(p,k)} for p in opt.params]}


def _restore_optimizer(opt, state, device):
    if state is None: return
    if _teaching_optimizer(opt):
        if state.get('teaching_optimizer_schema') != 1 or state['class'] != _ref(opt):
            raise ValueError('Teaching optimizer class differs from the checkpoint.')
        if len(state['parameter_moments']) != len(opt.params): raise ValueError('Teaching optimizer parameter count changed.')
        for k,v in state['attributes'].items(): setattr(opt,k,v)
        for p, moments in zip(opt.params,state['parameter_moments']):
            for k in ['avg','sqr_avg']:
                if k in moments: setattr(p,k,moments[k].to(p.device))
                elif hasattr(p,k): delattr(p,k)
    else:
        value = _move(state,device) if type(opt).__module__.startswith('fastai.') else state
        opt.load_state_dict(value)


def _tensor_bytes(value):
    import torch
    if isinstance(value, torch.Tensor): return value.numel()*value.element_size()
    if isinstance(value, dict): return sum(_tensor_bytes(v) for v in value.values())
    if isinstance(value, (tuple,list)): return sum(_tensor_bytes(v) for v in value)
    return 0


def _file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()


def _artifact_usage(roots):
    # Explicit local byte accounting; Drive's filesystem free space is not quota.
    seen, total = set(), 0
    for root in roots:
        root = Path(root)
        if not root.exists(): continue
        for base, dirs, files in os.walk(root, followlinks=False, onerror=lambda e: (_ for _ in ()).throw(e)):
            for name in files:
                p = Path(base)/name
                if p.is_symlink(): continue
                resolved = p.resolve()
                if resolved not in seen:
                    total += p.stat().st_size; seen.add(resolved)
    return total


class ArtifactStorageError(RuntimeError):
    """A full fit cannot retain its required state within the configured budget."""


def _storage_gate(context, required, *, phase, details=None):
    roots = context.get('artifact_budget_paths', [context['saved'].parent])
    budget = context.get('artifact_budget_bytes')
    if budget is None:
        budget = int(float(os.environ.get('HAILONG_DRIVE_ARTIFACT_BUDGET_GB','9'))*1_000_000_000)
    if budget <= 0: raise ValueError('HAILONG_DRIVE_ARTIFACT_BUDGET_GB must be positive.')
    used = _artifact_usage(roots)
    runtime_path = Path(context.get('runtime_storage_path', '/content' if Path('/content').is_dir() else context['root']))
    free = shutil.disk_usage(runtime_path).free
    report = {'phase':phase, 'used_artifact_bytes':used, 'configured_artifact_budget_bytes':budget,
              'required_additional_estimate_bytes':int(required), 'runtime_free_bytes':free,
              'budget_is_cloud_quota':False, 'measured_utc':datetime.now(timezone.utc).isoformat(),
              'details':details or {}, 'fits_artifact_budget':used+required<=budget,
              'fits_runtime_storage':required<=free}
    context['run'].setdefault('storage_checks',[]).append(report)
    print(f'Storage check ({phase}): artifacts {used/1e9:.3f} GB; configured budget {budget/1e9:.3f} GB; '
          f'additional estimate {required/1e9:.3f} GB; runtime free {free/1e9:.3f} GB. Budget is not Drive quota.')
    if used+required > budget or required > free:
        raise ArtifactStorageError('Full fit blocked before further training: persistent/runtime storage cannot retain '
            f'{required:,} additional bytes (used {used:,}, configured artifact budget {budget:,}, runtime free {free:,}). '
            'Free storage or explicitly increase HAILONG_DRIVE_ARTIFACT_BUDGET_GB after checking Drive quota; no epochs were reduced.')
    return report


def _estimate_fit_storage(learn, overhead):
    model = _tensor_bytes(learn.model.state_dict())
    params = sum(p.numel()*p.element_size() for p in learn.model.parameters() if p.requires_grad)
    opt = getattr(learn,'opt',None)
    name = ('' if opt is None else _ref(opt))+' '+repr(getattr(learn,'opt_func',''))
    if 'adam' in name.lower(): multiplier=2
    elif 'sgd' in name.lower(): multiplier=1
    elif 'rms' in name.lower(): multiplier=2
    else: multiplier=4  # Unknown optimizer: conservative future-state allowance.
    existing = _tensor_bytes(_optimizer_state(opt))
    optimizer = max(existing,params*multiplier)
    slot = model+optimizer+params+overhead
    return {'measured_model_bytes':model, 'trainable_parameter_bytes':params,
            'measured_existing_optimizer_bytes':existing, 'estimated_optimizer_bytes':optimizer,
            'snapshot_slot_estimate_bytes':slot, 'active_slots':2, 'atomic_replacement_slots':1,
            'metadata_allowance_bytes':overhead, 'estimated_peak_additional_bytes':3*slot+overhead}


def _data_signature(learn):
    result = {}
    for split in ['train', 'valid']:
        dl = getattr(getattr(learn, 'dls', None), split, None)
        if dl is None: continue
        # Accelerator wraps the same input loader during before_fit. Compare the
        # underlying dataset and effective batch size across the wrapping step.
        while getattr(dl, 'base_dataloader', None) is not None:
            dl = dl.base_dataloader
        ds = getattr(dl, 'dataset', None)
        batch_size = getattr(dl,'bs',None) or getattr(dl,'batch_size',None) or getattr(getattr(dl,'batch_sampler',None),'batch_size',None)
        item = {'loader_class': _ref(dl), 'dataset_class': _ref(ds),
                'batch_size': batch_size}
        try: item['batches'] = len(dl)
        except TypeError: pass
        try: item['rows'] = len(ds)
        except TypeError: pass
        # Ordered filenames/indices are cheap to compare, even for large image sets.
        values = getattr(ds, 'files', getattr(ds, 'items', None))
        if values is not None:
            hasher = hashlib.sha256()
            for value in values: hasher.update((str(value)+'\n').encode())
            item['ordered_items_sha256'] = hasher.hexdigest()
        result[split] = _stable(item)
    return result


def _source(context):
    path = context['folder'] / context['run']['notebook']
    if not path.is_file(): raise FileNotFoundError(f'Checkpoint source notebook missing: {path}')
    return {'notebook': context['run']['notebook'], 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def _rng_state(learn):
    import torch
    result = {'python': random.getstate(), 'torch': torch.get_rng_state()}
    if torch.cuda.is_available(): result['cuda'] = torch.cuda.get_rng_state_all()
    if 'numpy' in sys.modules:
        state = sys.modules['numpy'].random.get_state()
        result['numpy'] = (state[0], state[1].tolist(), state[2], state[3], state[4])
    result['loader_generators'] = {}
    for split in ['train', 'valid']:
        dl = getattr(getattr(learn, 'dls', None), split, None)
        generator = getattr(dl, 'generator', None)
        if generator is not None: result['loader_generators'][split] = generator.get_state()
    return result


def _restore_rng(learn, state):
    import torch
    random.setstate(state['python']); torch.set_rng_state(state['torch'])
    if 'cuda' in state and torch.cuda.is_available(): torch.cuda.set_rng_state_all(state['cuda'])
    if 'numpy' in state:
        import numpy as np
        s = state['numpy']; np.random.set_state((s[0], np.array(s[1], dtype=np.uint32), s[2], s[3], s[4]))
    for split, value in state.get('loader_generators', {}).items():
        dl = getattr(getattr(learn, 'dls', None), split, None)
        generator = getattr(dl, 'generator', None)
        if generator is None: raise ValueError(f'Recovery needs the original {split} loader generator.')
        generator.set_state(value)


def _callback_states(cbs):
    states = {}
    for index, cb in enumerate(cbs):
        attrs = {}
        for attr in ['sched', 'schedo', 'scaler']:
            value = getattr(cb, attr, None)
            if hasattr(value, 'state_dict'): attrs[attr] = _cpu(value.state_dict())
        acc_scaler = getattr(getattr(cb, 'acc', None), 'scaler', None)
        if hasattr(acc_scaler, 'state_dict'): attrs['acc.scaler'] = _cpu(acc_scaler.state_dict())
        if attrs: states[f'{index}:{_ref(cb)}'] = attrs
    return states


def _restore_callbacks(cbs, states):
    for key, attrs in states.items():
        index = int(key.split(':', 1)[0]); cb = cbs[index]
        if key != f'{index}:{_ref(cb)}': raise ValueError('Checkpoint callback order or classes changed.')
        for attr, state in attrs.items():
            value = getattr(getattr(cb, 'acc', None), 'scaler', None) if attr == 'acc.scaler' else getattr(cb, attr, None)
            if not hasattr(value, 'load_state_dict'): raise ValueError(f'Missing recovery state handler: {key}.{attr}')
            value.load_state_dict(state)


def _atomic_json(value, path):
    temp = path.with_name(path.name+'.writing')
    temp.write_text(json.dumps(value, indent=2, default=str), encoding='utf-8')
    temp.replace(path)


def _load_owned_checkpoint(path, context):
    import torch
    path = Path(path).resolve()
    trusted = (context['saved'] / 'models' / 'training_state').resolve()
    if not path.is_relative_to(trusted):
        raise ValueError('Recovery accepts only this course folder\'s own Drive training_state checkpoints.')
    # Files are produced by this hook in the caller's own persistent course folder.
    state = torch.load(path, map_location='cpu', weights_only=False)
    if state.get('schema') == 2:
        raise ValueError('This completed-fit artifact stores exact final model weights only; it has no optimizer state for interrupted-fit recovery.')
    if state.get('schema') != 1: raise ValueError('Unsupported checkpoint format.')
    return state


def resume_next_fit(learn, checkpoint, *, confirm_same_data=False):
    """Explicitly recover one interrupted fit from its completed epoch snapshot.

    Recreate the same learner/callbacks/data, call this function, then call the
    original fit with its original total epochs and arguments. No fit resumes
    automatically. Step/partial-epoch snapshots are inspection/recovery evidence
    only: exact mid-epoch dataloader replay is not implemented.
    """
    if not _context or not _context['drive']: raise RuntimeError('Drive-backed setup_course is required first.')
    if not confirm_same_data: raise ValueError('Confirm unchanged original input data with confirm_same_data=True.')
    state = _load_owned_checkpoint(checkpoint, _context)
    if not state['metadata']['epoch_completed']: raise ValueError('Use latest_epoch.pt; mid-epoch replay is not supported.')
    if state['metadata']['source'] != _source(_context): raise ValueError('Source notebook differs from the saved fit.')
    if state['metadata']['architecture'] != _architecture(learn.model): raise ValueError('Model architecture or trainable groups differ.')
    if state['metadata']['data_signature'] != _data_signature(learn): raise ValueError('Dataset/loader structure or ordered items differ.')
    learn._course_pending_resume = state
    return {'next_epoch': state['metadata']['epoch']+1, 'original_total_epochs': state['metadata']['total_epochs'],
            'note': 'The next matching genuine fit will restore the saved state. Input byte identity is confirmed by the caller.'}


class _FitSession:
    def __init__(self, learn, context, framework, config, cbs, total_epochs):
        self.learn, self.context, self.framework = learn, context, framework
        self.config, self.cbs, self.total = config, cbs, total_epochs
        self.started = time.monotonic(); self.last_save = self.started
        self.steps = 0; self.completed_epoch = -1; self.epoch_cancelled = False
        self.completed_epochs = set(); self.epoch_started = self.started
        self.initialized = False; self.resumed_from = None
        self.owned_files = set(); self.owned_signatures = {}; self.storage_estimate = None
        fit_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'-'+uuid.uuid4().hex[:8]
        self.path = context['saved']/'models'/'training_state'/Path(context['run']['notebook']).stem/fit_id

    def before_fit(self):
        self.source = _source(self.context)
        self.architecture = _architecture(self.learn.model)
        self.data = _data_signature(self.learn)
        overhead = int(self.context.get('checkpoint_metadata_allowance_bytes',8*1024*1024))
        self.storage_estimate = _estimate_fit_storage(self.learn,overhead)
        _storage_gate(self.context,self.storage_estimate['estimated_peak_additional_bytes'],phase='before_fit',details=self.storage_estimate)
        # A UUID leaf must be new. Compaction never acquires an old fit directory.
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.path.mkdir(exist_ok=False)
        self.initialized = True
        pending = getattr(self.learn, '_course_pending_resume', None)
        if pending is not None:
            meta = pending['metadata']
            if meta['source'] != self.source or meta['architecture'] != self.architecture or meta['data_signature'] != self.data:
                raise ValueError('Recovery source, model or dataset signature changed before fit.')
            if meta['fit_config'] != self.config or meta['total_epochs'] != self.total:
                raise ValueError('Recovery requires the original fit arguments and total epoch count.')
            opt = getattr(self.learn, 'opt', None)
            if meta['optimizer_class'] != (None if opt is None else _ref(opt)) or meta['optimizer_groups'] != ([] if opt is None else _optimizer_groups(opt)):
                raise ValueError('Recovery optimizer class or parameter groups differ.')
            if meta['versions'] != self._versions(): raise ValueError('Recovery package versions changed; start a new fit.')
            self.learn.model.load_state_dict(pending['model'], strict=True)
            device = next(self.learn.model.parameters()).device
            # PyTorch optimizers cast their own tensor states, including special
            # CPU step counters. fastai's optimizer loads the mapping directly.
            if opt is not None: _restore_optimizer(opt,pending['optimizer'],device)
            for name, param in self.learn.model.named_parameters():
                grad = pending.get('gradients', {}).get(name)
                param.grad = None if grad is None else grad.to(device)
            _restore_callbacks(self.cbs, pending['callback_states'])
            _restore_rng(self.learn, pending['rng'])
            self.completed_epoch = meta['epoch']; self.steps = meta['training_batches']
            self.completed_epochs = set(meta['completed_epochs'])
            self.resumed_from = meta['checkpoint_id']
            if self.framework == 'miniai': self.learn.epochs = range(self.completed_epoch+1, self.total)
            del self.learn._course_pending_resume
            print('Explicit checkpoint recovery: next epoch', self.completed_epoch+1, 'of', self.total)
        self.save('initial_state.pt', 'fit_started', epoch_completed=False)

    def _versions(self):
        return {k: v for k, v in self.context['run'].get('versions', {}).items() if k in ['torch','torchvision','fastai','fastcore','accelerate']}

    def after_batch(self):
        if not getattr(self.learn, 'training', False): return
        self.steps += 1
        interval = max(60, int(self.context.get('checkpoint_interval_seconds', 600)))
        if time.monotonic()-self.last_save >= interval:
            self.save('latest_step.pt', 'training_step', epoch_completed=False)

    def before_epoch(self):
        self.epoch_cancelled = False
        if self.framework == 'fastai' or getattr(self.learn,'training',False):
            self.epoch_started = time.monotonic()

    def after_epoch(self):
        epoch = int(getattr(self.learn, 'epoch', -1))
        if self.framework == 'miniai' and getattr(self.learn, 'training', False) and self.config.get('valid', True):
            self.save('latest_train_phase.pt', 'training_phase_finished', epoch_completed=False)
        elif not self.epoch_cancelled:
            self.completed_epoch = epoch
            self.completed_epochs.add(epoch)
            self.save('latest_epoch.pt', 'epoch_finished', epoch_completed=True)
        self.epoch_cancelled = False

    def save(self, filename, status, *, epoch_completed):
        if not self.initialized: return
        import torch
        # Bound future storage to two full snapshots per fit. Never delete any
        # existing/user-authored checkpoints: overwrite only this fit's slots.
        event = filename
        filename = 'latest_epoch.pt' if filename == 'latest_epoch.pt' else 'latest_state.pt'
        opt = getattr(self.learn, 'opt', None)
        epoch = int(getattr(self.learn, 'epoch', self.completed_epoch))
        meta = {'checkpoint_id': str(self.path.name)+'/'+filename, 'framework': self.framework,
                'source': self.source, 'architecture': self.architecture, 'optimizer_class': None if opt is None else _ref(opt),
                'optimizer_groups': [] if opt is None else _optimizer_groups(opt), 'fit_config': self.config, 'data_signature': self.data,
                'total_epochs': self.total, 'epoch': epoch, 'completed_epoch': self.completed_epoch,
                'completed_epochs': sorted(self.completed_epochs),
                'epoch_completed': epoch_completed, 'training_batches': self.steps,
                'epoch_elapsed_seconds': time.monotonic()-self.epoch_started,
                'elapsed_seconds': time.monotonic()-self.started, 'saved_utc': datetime.now(timezone.utc).isoformat(),
                'status': status, 'quick_run': self.context['run']['quick_run'], 'versions': self._versions(),
                'snapshot_event': event,
                'resumed_from': self.resumed_from, 'provider_course_completion_claimed': False,
                'mid_epoch_resume_supported': False}
        state = {'schema': 1, 'metadata': meta, 'model': _cpu(self.learn.model.state_dict()),
                 'optimizer': _optimizer_state(opt), 'gradients': {n: _cpu(p.grad) for n,p in self.learn.model.named_parameters() if p.grad is not None},
                 'callback_states': _callback_states(self.cbs), 'rng': _rng_state(self.learn)}
        target = self.path/filename; temp = target.with_name(target.name+'.writing')
        self._check_write(state)
        torch.save(state, temp); temp.replace(target)
        _atomic_json(meta, target.with_suffix('.json'))
        self.owned_files.update([target,target.with_suffix('.json')])
        for file in [target,target.with_suffix('.json')]:
            stat=file.stat();self.owned_signatures[file]=(stat.st_size,stat.st_mtime_ns)
        _atomic_json({'checkpoint': str(target), **meta}, self.path/'latest.json')
        with (self.path/'events.jsonl').open('a',encoding='utf-8') as out:
            out.write(json.dumps({'checkpoint':str(target),**meta},default=str)+'\n')
        self.last_save = time.monotonic()

    def _check_write(self,state):
        allowance = int(self.context.get('checkpoint_metadata_allowance_bytes',8*1024*1024))
        required = _tensor_bytes(state)+allowance
        _storage_gate(self.context,required,phase='checkpoint_write',details={'fit_directory':str(self.path)})

    def _metrics(self):
        result = {}
        recorder = getattr(self.learn,'recorder',None)
        if recorder is not None:
            result['recorder_metric_names'] = _stable(getattr(recorder,'metric_names',None))
            result['recorder_values'] = _stable(getattr(recorder,'values',None))
        for index, cb in enumerate(self.cbs):
            metrics = getattr(cb,'all_metrics',None)
            if isinstance(metrics,dict):
                result[f'{index}:{_ref(cb)}'] = {}
                for k,v in metrics.items():
                    if hasattr(v,'compute'):
                        value=_cpu(v.compute())
                        result[f'{index}:{_ref(cb)}'][str(k)]=_stable(value.tolist() if hasattr(value,'tolist') else value)
        return result

    def _compact_completed(self):
        import torch
        # Completion must be independently observed, not just a normal return.
        if self.completed_epochs != set(range(self.total)): raise ValueError('Incomplete fits cannot be compacted.')
        meta = {'source':self.source,'architecture':self.architecture,'fit_config':self.config,
                'data_signature':self.data,'total_epochs':self.total,'completed_epochs':sorted(self.completed_epochs),
                'training_batches':self.steps,'framework':self.framework,'versions':self._versions(),
                'all_requested_epochs_observed':True,'quick_run':self.context['run']['quick_run'],
                'optimizer_resume_supported':False,'saved_utc':datetime.now(timezone.utc).isoformat(),
                'provider_course_completion_claimed':False,'resumed_from':self.resumed_from,
                'elapsed_seconds':time.monotonic()-self.started,'metrics':self._metrics()}
        state = {'schema':2,'metadata':meta,'model':_cpu(self.learn.model.state_dict())}
        self._check_write(state)
        target = self.path/'final_model.pt'; temp = target.with_name(target.name+'.writing')
        torch.save(state,temp); temp.replace(target)
        artifact = {'relative_persistent_path':str(target.relative_to(self.context['saved']).as_posix()),
                    'sha256':_file_hash(target),'bytes':target.stat().st_size,
                    'producer_notebook':self.context['run']['notebook'],
                    'producer_run_id':self.context['run'].get('started_utc'),
                    'producer_source_sha256':self.source['sha256'],'role':'completed_fit_final_model',
                    'required_for_reuse':True,'consumers':[]}
        _atomic_json(meta,self.path/'final_model.json')
        retired=[]
        for file in sorted(self.owned_files):
            # Only our recorded two slots in this newly-created leaf are retired.
            if file.parent.resolve()!=self.path.resolve() or not file.resolve().is_relative_to(self.path.resolve()):
                raise ValueError('Checkpoint compaction target escaped its owned fit directory.')
            if file.name not in {'latest_epoch.pt','latest_epoch.json','latest_state.pt','latest_state.json'}:
                raise ValueError('Unexpected compaction candidate.')
            if file.is_symlink(): raise ValueError('Never compact a replaced checkpoint symlink.')
            if file.exists():
                stat=file.stat()
                if (stat.st_size,stat.st_mtime_ns)!=self.owned_signatures[file]:
                    raise ValueError('A checkpoint slot changed outside this fit; compaction will not remove it.')
                file.unlink(); retired.append(file.name)
        self.context['run'].setdefault('artifact_index',[]).append(artifact)
        _atomic_json({'checkpoint':str(target),**meta,'artifact':artifact,'retired_owned_checkpoint_slots':retired},self.path/'latest.json')
        return artifact,retired

    def finalize(self, returned, error=None):
        complete = returned and self.completed_epochs == set(range(self.total))
        if self.initialized:
            artifact, retired = None, []
            if complete: artifact,retired = self._compact_completed()
            else:
                try:self.save('final_state.pt','fit_interrupted_or_partial',epoch_completed=False)
                except Exception as checkpoint_error:
                    if error is None: raise
                    # Preserve the original cancellation/error and all last valid
                    # snapshots if the device filled while saving interruption.
                    self.context['run'].setdefault('checkpoint_save_errors',[]).append(str(checkpoint_error))
                    print('Interruption checkpoint could not replace its slot; previous snapshots retained:',str(checkpoint_error))
            summary = {'fit_returned': returned, 'all_requested_epochs_observed': complete,
                       'error': None if error is None else str(error), 'elapsed_seconds': time.monotonic()-self.started,
                       'provider_course_completion_claimed': False, 'notebook': self.context['run']['notebook'],
                       'fit_directory':str(self.path),'total_epochs':self.total,'completed_epochs':sorted(self.completed_epochs),
                       'storage_estimate':self.storage_estimate,'final_model_artifact':artifact,
                       'retired_owned_checkpoint_slots':retired,'interrupted_optimizer_recovery_preserved':not complete}
            _atomic_json(summary, self.path/'fit_summary.json')
            self.context['run'].setdefault('fits',[]).append(summary)
            _atomic_json(self.context['run'],self.context['record'])
            if returned and not complete:
                raise RuntimeError('A non-demonstration fit returned without observing every requested epoch; full-fit completion is unverified.')


def _move(value, device):
    import torch
    if isinstance(value, torch.Tensor): return value.to(device)
    if isinstance(value, dict): return {k:_move(v,device) for k,v in value.items()}
    if isinstance(value, list): return [_move(v,device) for v in value]
    if isinstance(value, tuple): return tuple(_move(v,device) for v in value)
    return value


def _callback(session, framework):
    if framework == 'fastai':
        from fastai.callback.core import Callback
        class CourseCheckpointCallback(Callback):
            order = 10000
            def before_fit(self): session.before_fit()
            def after_batch(self): session.after_batch()
            def before_epoch(self): session.before_epoch()
            def after_cancel_epoch(self): session.epoch_cancelled = True
            def after_epoch(self): session.after_epoch()
        return CourseCheckpointCallback()
    class CourseCheckpointCB:
        order = 10000
        def before_fit(self, learn): session.before_fit()
        def before_epoch(self, learn): session.before_epoch()
        def after_batch(self, learn): session.after_batch()
        def after_epoch(self, learn): session.after_epoch()
    return CourseCheckpointCB()


def _patch(cls, framework):
    original = getattr(cls, 'fit', None)
    if original is None or getattr(original, '_course_checkpoint_hook', False): return
    signature = inspect.signature(original)
    if 'cbs' not in signature.parameters: return
    @wraps(original)
    def fit(learn, *args, **kwargs):
        if not _context or not _context['drive']: return original(learn, *args, **kwargs)
        bound = signature.bind(learn, *args, **kwargs); bound.apply_defaults()
        added = _callbacks(bound.arguments.get('cbs'))
        cbs = _callbacks(getattr(learn, 'cbs', None))+added
        total = bound.arguments.get('n_epochs', bound.arguments.get('n_epoch', 0))
        if _is_demo(cbs) or not bound.arguments.get('train', True) or total <= 0:
            if getattr(learn, '_course_pending_resume', None) is not None:
                raise ValueError('Checkpoint recovery cannot be applied to an LR-finder, single-batch or evaluation fit.')
            return original(*bound.args, **bound.kwargs)
        config = {k:_stable(v) for k,v in bound.arguments.items() if k not in ['self','learn','cbs','start_epoch']}
        config.update({'learner_class': _ref(learn), 'callbacks': [_ref(c) for c in cbs], 'learner_lr': _stable(getattr(learn,'lr',None)),
                       'optimizer_factory': _stable(getattr(learn,'opt_func',None))})
        session = _FitSession(learn, dict(_context), framework, config, cbs, int(total))
        pending = getattr(learn, '_course_pending_resume', None)
        if pending is not None and framework == 'fastai':
            next_epoch = pending['metadata']['epoch']+1
            if next_epoch >= total: raise ValueError('This fit has already finished all requested epochs.')
            bound.arguments['start_epoch'] = next_epoch
        if pending is not None and pending['metadata']['epoch']+1 >= total:
            raise ValueError('This fit has already finished all requested epochs.')
        bound.arguments['cbs'] = added+[_callback(session, framework)]
        returned = False; error = None
        try:
            result = original(*bound.args, **bound.kwargs); returned = True
            return result
        except BaseException as exc:
            error = exc; raise
        finally:
            session.finalize(returned, error)
    fit._course_checkpoint_hook = True
    cls.fit = fit


def _patch_current_classes(*_):
    if not _context or not _context['drive']: return
    modules = [sys.modules.get('miniai.learner'), sys.modules.get('fastai.learner')]
    for module in modules:
        if module is not None:
            for cls in list(vars(module).values()):
                if isinstance(cls, type) and hasattr(cls, 'fit'):
                    _patch(cls, 'fastai' if cls.__module__.startswith('fastai.') else 'miniai')
    # Lesson 09 defines/patches Learner in notebook cells. Later lessons import it.
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip is not None:
            for cls in list(ip.user_ns.values()):
                if isinstance(cls, type) and cls.__module__ == '__main__' and hasattr(cls,'fit') and hasattr(cls,'callback') and hasattr(cls,'one_epoch'):
                    _patch(cls, 'miniai')
    except ImportError: pass


def register_hooks(context, profile):
    """Register after setup_course has established its Drive context."""
    global _context, _ipython_hook
    _context = context if context.get('drive') and profile in ['fastai','book','part2'] else None
    if _context is None: return {'enabled': False}
    prepare_reuse_evidence(context)
    if profile in ['fastai','book']:
        import fastai.learner
    else:
        import miniai.learner
    _patch_current_classes()
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip is not None and _ipython_hook is None:
            ip.events.register('post_run_cell', _patch_current_classes)
            _ipython_hook = _patch_current_classes
    except ImportError: pass
    return {'enabled': True, 'location': str(context['saved']/'models'/'training_state'),
            'epoch_checkpoints': True, 'step_interval_seconds': context.get('checkpoint_interval_seconds',600),
            'completed_fit_compaction':'exact_final_model_only_current_owned_fit',
            'artifact_budget_gb':float(os.environ.get('HAILONG_DRIVE_ARTIFACT_BUDGET_GB','9')),
            'automatic_resume': False, 'provider_course_completion_claimed': False}
