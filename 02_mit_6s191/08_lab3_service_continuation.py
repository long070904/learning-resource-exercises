# %% [markdown]
# # MIT 6.S191 Lab 3: service continuation
# This resumes the original OpenRouter judge and genuine Opik exercises after
# the full real-data training notebook has passed in hosted Colab. It never
# retrains the model. Missing, changed, partial, or reduced-run evidence stops
# execution. Existing local Qwen scores are not reused as API judge scores.
#
# Source: [MIT Lab 3](https://github.com/MITDeepLearning/introtodeeplearning/blob/master/lab3/LLM_Finetuning.ipynb),
# MIT Introduction to Deep Learning, 2026, MIT License.
# The official rubric, probe texts, 20/20/20 comparison, monitored example,
# Opik metric, and unchanged Yoda test measurement are retained below.
# Free OpenRouter judges are allowed by the source. The free allowance currently
# supports 50 requests/day and 20/minute; this notebook reserves headroom and
# saves every attempt before sending it. Resume the same run on a later day.
# No external service calls occur with the default authorization switch.

# %%
import os
AUTHORIZE_SERVICE_CALLS = False  #@param {type:"boolean"}
ALLOW_PAID_JUDGE = False  #@param {type:"boolean"}
JUDGE_MODEL_ID = "google/gemma-2-9b-it:free"  #@param {type:"string"}
OPIK_WORKSPACE = ""  #@param {type:"string"}
TRAINING_RUN_ID = ""  #@param {type:"string"}
MAX_REQUESTS_THIS_SESSION = 45  #@param {type:"integer"}
MAX_REQUESTS_PER_ROLLING_DAY = 45  #@param {type:"integer"}
MIN_SECONDS_BETWEEN_REQUESTS = 3.2  #@param {type:"number"}
RETRY_FAILED_REQUESTS = False  #@param {type:"boolean"}
RETRY_UNCERTAIN_REQUESTS = False  #@param {type:"boolean"}
APPROVED_PREPARED_SOURCE_SHA256 = "de35ad31546210e89f3b1355b08f3d58ffed9029cf6e1092d944209dd20a6f6a"
ORIGINAL_SOURCE_SHA256 = "388e2ecfd48bf8d60f3239162a973c35973af6040e5bf8ae258d16f1b46a50bd"
MYDRIVE = "/content/drive/MyDrive"
PROGRESS_ROOT = MYDRIVE + "/HaiLong_Course_Progress/2026-10-03"
MIT_ROOT = MYDRIVE + "/HaiLong_Colab_Results/02_mit_6s191"
MODEL_ID = "LiquidAI/LFM2-1.2B"
STEM = "07_lab3_llm_finetuning"

# An authorized parent may pass flags/keys only into this notebook's fresh
# subprocess. Colab Secret lookup below is only an interactive fallback.
AUTHORIZE_SERVICE_CALLS = AUTHORIZE_SERVICE_CALLS or os.environ.get("HAILONG_AUTHORIZE_LAB3_SERVICES") == "1"
ALLOW_PAID_JUDGE = ALLOW_PAID_JUDGE or os.environ.get("HAILONG_ALLOW_PAID_LAB3_JUDGE") == "1"
JUDGE_MODEL_ID = os.environ.get("HAILONG_LAB3_JUDGE_MODEL", JUDGE_MODEL_ID)
TRAINING_RUN_ID = os.environ.get("HAILONG_LAB3_TRAINING_RUN_ID", TRAINING_RUN_ID)
OPIK_WORKSPACE = OPIK_WORKSPACE or os.environ.get("OPIK_WORKSPACE", "")

if not AUTHORIZE_SERVICE_CALLS:
    raise RuntimeError("Review this notebook, configure your own Colab Secrets, and explicitly authorize the service calls first.")
if not JUDGE_MODEL_ID.endswith(":free") and not ALLOW_PAID_JUDGE:
    raise RuntimeError("A paid judge requires separate explicit ALLOW_PAID_JUDGE=True authorization. The default judge is free.")
assert JUDGE_MODEL_ID in ("google/gemma-2-9b-it:free", "google/gemini-2.5-flash"), "Review another judge's official model size/service scope first; the judge must be larger than the 1.2B performer."
assert 0 < MAX_REQUESTS_THIS_SESSION <= 1000
assert 0 < MAX_REQUESTS_PER_ROLLING_DAY <= 1000
assert MIN_SECONDS_BETWEEN_REQUESTS >= 3.1
if JUDGE_MODEL_ID.endswith(":free"):
    assert MAX_REQUESTS_PER_ROLLING_DAY <= 50, "Free account capacity is shared; choose at most 50, normally 45."
from google.colab import drive, userdata
from pathlib import Path
if not Path(MYDRIVE).is_dir():
    drive.mount("/content/drive", force_remount=True, timeout_ms=300000)

# %% [markdown]
# Verify the saved source, every executed code cell, full-mode Colab record,
# both 200-update training histories, original exercise evidence, and adapters.
# A source hash change requires review and an updated approved hash; do not
# remove this check. This notebook does not invent a completed training run.

# %%
import csv, gc, hashlib, importlib.util, json, math, os, statistics, time
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    temporary.replace(path)

def read_csv(path):
    with Path(path).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))

def write_csv(path, rows):
    if not rows:
        raise ValueError("No rows to save.")
    with Path(path).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

required_training_tasks = [
    "tokenizer_and_template", "tokenizer_round_trip", "next_token_prediction",
    "autoregressive_generation", "question_and_temperature_experiments", "lora",
    "real_style_data_leprechaun", "leprechaun_training", "leprechaun_generation",
    "real_style_data_yoda", "yoda_training", "judge_setup", "judge_probe_sentences",
    "heldout_yoda_generation", "judge_controls_and_generations", "judge_prompt_experiments",
    "training_duration_experiments", "inference_monitoring", "official_yoda_test_nll",
    "saved_style_adapters", "adapter_checkpoint_round_trip", "experiment_analysis",
]
runner_record_path = Path(PROGRESS_ROOT) / "records/02_mit_6s191" / (STEM + ".json")
executed_path = Path(PROGRESS_ROOT) / "notebooks/02_mit_6s191" / (STEM + ".ipynb")
runner_record = read_json(runner_record_path)
assert runner_record["status"] == "executed_without_errors", "Finish the full training notebook first."
assert runner_record["execution_location"] == "hosted_colab"
assert runner_record["source_sha256"] == APPROVED_PREPARED_SOURCE_SHA256, "Review the changed training source before reuse."
assert runner_record["output_sha256"] == sha256_file(executed_path), "Saved executed notebook hash changed."
assert runner_record["runtime_evidence"]["quick_run"] is False
assert runner_record["runtime_evidence"].get("course_smoke", "0") in ("0", "")
BASE_MODEL_REVISION = runner_record["runtime_evidence"].get("base_model_commit")
if BASE_MODEL_REVISION:
    assert isinstance(BASE_MODEL_REVISION, str) and len(BASE_MODEL_REVISION) == 40
    assert all(character in "0123456789abcdef" for character in BASE_MODEL_REVISION.lower())
executed_notebook = read_json(executed_path)
code_cells = [cell for cell in executed_notebook["cells"]
              if cell["cell_type"] == "code" and "".join(cell["source"]).strip()
              and "hailong-runtime-probe" not in cell.get("metadata", {}).get("tags", [])]
# Accept the actual runner tag spelling, while excluding only its diagnostic cell.
code_cells = [cell for cell in code_cells
              if not "".join(cell["source"]).startswith("# Added by the course runner: inspect the executed runtime")]
assert len(code_cells) == runner_record["expected_code_cells"]
assert all(cell.get("execution_count") is not None for cell in code_cells)
assert not any(output.get("output_type") == "error" for cell in code_cells for output in cell.get("outputs", []))

result_root = Path(MIT_ROOT) / "results"
candidates = []
for path in result_root.glob(STEM + "-*.json"):
    record = read_json(path)
    env = record.get("execution_environment", {})
    run_id = env.get("run_id")
    if (run_id and (not TRAINING_RUN_ID or run_id == TRAINING_RUN_ID)
            and record.get("full_real_data_exercise_checks_passed") is True
            and env.get("in_colab") is True
            and record.get("status") == "reached_final_cell"):
        candidates.append((path, record))
assert candidates, "No complete full-mode hosted training record exists; run the original prepared Lab 3 first."
# The newest completed course record must refer to the executed notebook currently
# verified above. Earlier runs are available only with an explicit run ID and a
# matching output record; mismatches are refused instead of mixing evidence.
training_record_path, training_record = max(candidates, key=lambda pair: pair[0].stat().st_mtime)
TRAINING_RUN_ID = training_record["execution_environment"]["run_id"]
TRAIN_DIR = result_root / STEM / TRAINING_RUN_ID
TRAIN_MODELS = Path(MIT_ROOT) / "models" / STEM / TRAINING_RUN_ID
training_tasks = read_json(TRAIN_DIR / "task_evidence.json")
assert all(task in training_tasks for task in required_training_tasks)
assert training_record["exercise_evidence"] == training_tasks
assert any(TRAINING_RUN_ID in "".join(output.get("text", []))
           for cell in code_cells for output in cell.get("outputs", [])
           if output.get("output_type") == "stream"), "Selected training run differs from the saved executed notebook."
for style in ("leprechaun", "yoda"):
    assert training_tasks[style + "_training"]["updates"] == 200
    assert training_tasks[style + "_training"]["real_course_data"] is True
    rows = read_csv(TRAIN_DIR / (style + "_training.csv"))
    assert len(rows) == 200 and [int(row["update"]) for row in rows] == list(range(1, 201))
    assert all(math.isfinite(float(row["loss"])) for row in rows)
assert training_tasks["heldout_yoda_generation"]["examples"] == 20
assert training_tasks["heldout_yoda_generation"]["questions_from_training"] is False
assert training_tasks["adapter_checkpoint_round_trip"]["passed"] is True
assert training_tasks["saved_style_adapters"]["base_model"] == MODEL_ID
assert training_tasks["official_yoda_test_nll"]["original_text_unchanged"] is True
assert math.isfinite(training_tasks["official_yoda_test_nll"]["mean_negative_log_likelihood"])

verified_files = [runner_record_path, executed_path, training_record_path, TRAIN_DIR / "task_evidence.json"]
for filename in ("leprechaun_training.csv", "yoda_training.csv", "heldout_generations.csv",
                 "paired_controls.csv", "yoda_training_duration_experiments.csv"):
    verified_files.append(TRAIN_DIR / filename)
for adapter in ("leprechaun_step200", "yoda_step100", "yoda_step200", "yoda_final"):
    directory = TRAIN_MODELS / adapter
    config = read_json(directory / "adapter_config.json")
    assert config["base_model_name_or_path"] == MODEL_ID and config["r"] == 8
    assert (directory / "adapter_model.safetensors").stat().st_size > 0
    verified_files.extend(sorted(path for path in directory.iterdir() if path.is_file()))
verification = {
    "run_id": TRAINING_RUN_ID,
    "prepared_source_sha256": APPROVED_PREPARED_SOURCE_SHA256,
    "original_template_sha256": ORIGINAL_SOURCE_SHA256,
    "files": {str(path): sha256_file(path) for path in verified_files},
}
verification_id = hashlib.sha256(json.dumps(verification, sort_keys=True).encode()).hexdigest()
judge_slug = hashlib.sha256(JUDGE_MODEL_ID.encode()).hexdigest()[:12]
SERVICE_DIR = TRAIN_DIR / ("official_services_" + judge_slug)
SERVICE_DIR.mkdir(exist_ok=True)
verification_path = SERVICE_DIR / "training_verification.json"
if verification_path.exists():
    assert read_json(verification_path) == verification, "Training artifacts changed since this service run began."
else:
    atomic_json(verification_path, verification)
EVIDENCE_PATH = SERVICE_DIR / "service_task_evidence.json"
SERVICE_TASKS = read_json(EVIDENCE_PATH) if EVIDENCE_PATH.exists() else {}

def record_service_task(name, **evidence):
    SERVICE_TASKS[name] = {"recorded_utc": utc_now(), **evidence}
    atomic_json(EVIDENCE_PATH, SERVICE_TASKS)

record_service_task("verified_full_training", run_id=TRAINING_RUN_ID, verification_id=verification_id,
                    required_tasks=len(required_training_tasks), updates_per_style=200)
print("Verified saved full training run:", TRAINING_RUN_ID)
print("Resumable service results:", SERVICE_DIR)

# %% [markdown]
# Use the user's own `OPENROUTER_API_KEY` and `OPIK_API_KEY` Colab Secrets.
# Never paste a key into a cell or notebook output. Environment variables are
# an explicit alternative. Only these two named keys are read; nothing is
# saved or printed. This configuration follows genuine Opik cloud SDK usage.

# %%
import subprocess, sys
missing_packages = [name for name in ("openai", "opik", "transformers", "peft", "mitdeeplearning")
                    if importlib.util.find_spec(name) is None]
if missing_packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", *missing_packages])

def configured_secret(name):
    value = os.environ.get(name)
    if not value:
        try:
            value = userdata.get(name)
        except Exception:
            raise RuntimeError("Configure and grant this notebook access to Colab Secret " + name + ".") from None
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError("Missing user-configured " + name + ".")
    return value.strip()

os.environ["OPIK_API_KEY"] = configured_secret("OPIK_API_KEY")
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"
os.environ["OPIK_ANALYTICS_ENABLE"] = "false"
os.environ["OPIK_CONSOLE_LOGGING_LEVEL"] = "WARNING"
os.environ["OPIK_TRACK_DISABLE"] = "false"
os.environ["OPIK_PROJECT_NAME"] = "6S191_Lab3_" + TRAINING_RUN_ID
if OPIK_WORKSPACE:
    os.environ["OPIK_WORKSPACE"] = OPIK_WORKSPACE
from openai import OpenAI
import opik
from opik import opik_context, track
from opik.evaluation.metrics import base_metric, score_result
router = OpenAI(base_url="https://openrouter.ai/api/v1",
                api_key=configured_secret("OPENROUTER_API_KEY"), max_retries=0, timeout=90)
opik_client = opik.Opik(project_name=os.environ["OPIK_PROJECT_NAME"], batching=False)
# Read-only account access check. No judge request is issued here.
try:
    opik_client.auth_check()
except Exception:
    raise RuntimeError("Opik authentication/workspace access failed. Check your own key and workspace settings.") from None
project_url = opik_client.get_project_url()
record_service_task("service_configuration", judge=JUDGE_MODEL_ID, free_judge=JUDGE_MODEL_ID.endswith(":free"),
                    project_name=os.environ["OPIK_PROJECT_NAME"], opik_project_url=project_url,
                    keys_saved=False, sdk="genuine_opik", automatic_api_retries=0)

# %% [markdown]
# An API attempt is written before sending it. A successful response is saved
# before score parsing, so an interrupted or malformed result remains visible.
# Failed and uncertain attempts never silently consume additional requests.
# Quota pauses are expected; run the notebook again later with the same training
# run and judge. Successful cached responses are reused without an API call.
# The quota ledger includes all continuations made by this notebook. Other
# applications can consume account quota too; leave suitable headroom.

# %%
QUOTA_PATH = Path(MIT_ROOT) / "results/lab3_openrouter_attempt_ledger.json"
REQUEST_DIR = SERVICE_DIR / "requests"
REQUEST_DIR.mkdir(exist_ok=True)
session_attempts = 0
last_send_monotonic = None
retried_request_ids_this_session = set()

class ServicePause(RuntimeError):
    pass

def parse_judge_score(response):
    payload = json.loads(response)
    raw = payload["score"]
    if isinstance(raw, bool) or not isinstance(raw, (float, int)) or not math.isfinite(raw):
        raise ValueError("Judge score must be a finite JSON number.")
    # Preserve the course's normalization/clipping, without inventing a score.
    return float(raw), max(0.0, min(float(raw) / 10.0, 1.0))

def quota_status():
    ledger = read_json(QUOTA_PATH) if QUOTA_PATH.exists() else {"attempts": []}
    cutoff = time.time() - 24 * 3600
    recent = [attempt for attempt in ledger["attempts"] if attempt["timestamp"] > cutoff]
    return ledger, recent

def api_judge_response(text, rubric):
    global session_attempts, last_send_monotonic
    identity = {"verification_id": verification_id, "model": JUDGE_MODEL_ID,
                "system_prompt": rubric, "user_prompt": "Evaluate this text: " + text,
                "temperature": 0, "max_tokens": 96}
    request_id = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    request_path = REQUEST_DIR / (request_id + ".json")
    saved = read_json(request_path) if request_path.exists() else {"identity": identity, "attempts": []}
    assert saved["identity"] == identity
    if saved.get("response") is not None:
        if not saved.get("score_parse_failed") or not RETRY_FAILED_REQUESTS:
            return saved["response"], request_id
        # The raw response remains in its original attempt; an explicit retry
        # does not erase evidence or convert invalid JSON into a made-up score.
        saved.pop("response")
        saved.pop("score_parse_failed", None)
    previous = saved["attempts"][-1] if saved["attempts"] else None
    if previous:
        uncertain = previous["status"] in ("pending", "uncertain_delivery")
        allowed = RETRY_UNCERTAIN_REQUESTS if uncertain else RETRY_FAILED_REQUESTS
        if not allowed or request_id in retried_request_ids_this_session:
            raise ServicePause("A previous request failed or its delivery is uncertain. Its record is preserved. Review it and explicitly allow one retry before continuing.")
        if previous.get("http_status") == 429 and time.time() - previous["timestamp"] < 24 * 3600:
            raise ServicePause("A prior quota/rate-limit response is preserved. Resume after 24 hours; no retry was sent.")
        retried_request_ids_this_session.add(request_id)
    ledger, recent = quota_status()
    if session_attempts >= MAX_REQUESTS_THIS_SESSION or len(recent) >= MAX_REQUESTS_PER_ROLLING_DAY:
        record_service_task("quota_pause", attempts_this_session=session_attempts,
                            attempts_last_24h=len(recent), next_request_id=request_id)
        raise ServicePause("Request budget reached; completed responses are saved in Drive. Resume this same notebook on a later day.")
    if last_send_monotonic is not None:
        remaining = MIN_SECONDS_BETWEEN_REQUESTS - (time.monotonic() - last_send_monotonic)
        if remaining > 0:
            time.sleep(remaining)
    attempt = {"request_id": request_id, "timestamp": time.time(), "utc": utc_now(),
               "model": JUDGE_MODEL_ID, "status": "pending", "service_directory": str(SERVICE_DIR)}
    saved["attempts"].append(attempt.copy())
    atomic_json(request_path, saved)
    ledger["attempts"].append(attempt.copy())
    atomic_json(QUOTA_PATH, ledger)
    session_attempts += 1
    last_send_monotonic = time.monotonic()
    try:
        response = router.chat.completions.create(
            model=JUDGE_MODEL_ID,
            messages=[{"role": "system", "content": rubric},
                      {"role": "user", "content": identity["user_prompt"]}],
            temperature=0, max_tokens=96)
        content = response.choices[0].message.content
        if not isinstance(content, str) or not content.strip():
            raise ValueError("Judge returned no text.")
        saved.update(response=content, provider_response_id=response.id,
                     usage=response.usage.model_dump() if response.usage else None,
                     completed_utc=utc_now())
        saved["attempts"][-1].update(response=content, provider_response_id=response.id,
                                     usage=saved["usage"])
        status = "response_saved"
    except Exception as error:
        # Do not save SDK exception text or request headers: they can expose keys.
        status = "uncertain_delivery" if type(error).__name__ in ("APITimeoutError", "APIConnectionError") else "failed"
        saved["attempts"][-1].update(exception_type=type(error).__name__,
                                     http_status=getattr(error, "status_code", None))
    saved["attempts"][-1]["status"] = status
    ledger["attempts"][-1].update(saved["attempts"][-1])
    atomic_json(request_path, saved)
    atomic_json(QUOTA_PATH, ledger)
    if status != "response_saved":
        raise ServicePause("Judge request failed. A redacted failure record was saved; no automatic retry was made.") from None
    return saved["response"], request_id

class LLMJudgeEvaluator(base_metric.BaseMetric):
    def __init__(self, system_prompt):
        super().__init__(name="StyleScore", track=False)
        self.system_prompt = system_prompt

    def score(self, text, system_override=None, **ignored_kwargs):
        rubric = system_override if system_override is not None else self.system_prompt
        response, request_id = api_judge_response(text, rubric)
        try:
            raw, value = parse_judge_score(response)
        except (ValueError, KeyError, TypeError):
            path = REQUEST_DIR / (request_id + ".json")
            saved = read_json(path)
            saved["score_parse_failed"] = True
            saved["attempts"][-1]["status"] = "invalid_score_json"
            atomic_json(path, saved)
            record_service_task("invalid_judge_json", request_id=request_id)
            raise ServicePause("The actual judge response is saved but is not valid score JSON. Inspect it; no score was fabricated or fallback judge used.") from None
        path = REQUEST_DIR / (request_id + ".json")
        saved = read_json(path)
        saved.update(raw_score=raw, normalized_score=value)
        atomic_json(path, saved)
        return score_result.ScoreResult(name="StyleScore", value=value,
                                       reason="OpenRouter response " + request_id)

# %% [markdown]
# The original judge rubric and probes are used verbatim. The response budget
# is increased from 20 to 96 tokens to avoid truncating a numeric JSON answer;
# its required score scale and output format remain unchanged.

# %%
system_prompt = """
You are an impartial judge that evaluates if text was written by {style}.

An example piece of text from {style} is:
{example}

Now, analyze some new text carefully and respond on if it follows the
same style of {style}. Be critical to identify any issues in the text.
Then convert your feedback into a number between 0 and 10: 10 if the text
is written exactly in the style of {style}, 5 if mixed faithfulness to the
style, or 0 if the text is not at all written in the style of {style}.

Directly answer with the score formatted in a dictionary.
The format of your response should only be the dictionary and nothing else:
{{"score": <score between 0 and 10>}}
"""
example = "The very Republic is threatened, if involved the Sith are. Hard to see, the dark side is. Discover who this assassin is, we must. With this Naboo queen you must stay, Qui-Gon. Protect her. May the Force be with you. A vergence, you say? But you do! Revealed your opinion is. Trained as a Jedi, you request for him? Good, good, young one."
system_prompt = system_prompt.format(style="Yoda", example=example)
judge = LLMJudgeEvaluator(system_prompt)
record_service_task("genuine_opik_custom_metric", base_class=type(judge).__mro__[1].__module__,
                    score_scale="clipped score/10", rubric=system_prompt)
test_texts = ["Tennis is a fun sport. But you must concentrate.",
              "Fun sport, tennis is. But work hard, you must.",
              "Hard to see, the dark side is."]
probe_rows = [{"text": text, "score": judge.score(text).value} for text in test_texts]
write_csv(SERVICE_DIR / "judge_probe_sentences.csv", probe_rows)
record_service_task("judge_probe_sentences", examples=3, rows=probe_rows)
print(probe_rows)

# %% [markdown]
# Re-score the saved full-run texts with the real API judge: 20 held-out model
# generations, 20 base-style controls, and 20 true-Yoda training controls.
# Controls are paired on the same question. The saved generation/control
# files were hashed above; local scores from the training run are discarded.

# %%
heldout_rows = read_csv(TRAIN_DIR / "heldout_generations.csv")
control_rows = read_csv(TRAIN_DIR / "paired_controls.csv")
assert len(heldout_rows) == len(control_rows) == 20
assert all(row["generated"].strip() for row in heldout_rows)
assert all(row["base"].strip() and row["style"].strip() for row in control_rows)
assert set(row["question"] for row in heldout_rows).isdisjoint(row["question"] for row in control_rows)
evaluation_rows = []
for label, rows, column in (("Base", control_rows, "base"),
                            ("Generated", heldout_rows, "generated"),
                            ("Style", control_rows, "style")):
    for index, row in enumerate(rows):
        scored = {"type": label, "index": index, "question": row["question"],
                  "text": row[column], "score": judge.score(row[column]).value}
        evaluation_rows.append(scored)
        # Also save the partial table; a quota pause retains useful visible work.
        write_csv(SERVICE_DIR / "judge_controls_and_generations.csv", evaluation_rows)
summary = []
for label in ("Base", "Generated", "Style"):
    values = [row["score"] for row in evaluation_rows if row["type"] == label]
    assert len(values) == 20
    summary.append({"type": label, "examples": 20, "mean": statistics.mean(values),
                    "std": statistics.pstdev(values)})
write_csv(SERVICE_DIR / "style_score_summary.csv", summary)
record_service_task("judge_controls_and_generations", judge=JUDGE_MODEL_ID, groups=summary,
                    generated_held_out=True, paired_controls=True, score_source="real_API_responses")
import matplotlib.pyplot as plt
plt.figure()
for label in ("Base", "Generated", "Style"):
    plt.hist([row["score"] for row in evaluation_rows if row["type"] == label],
             bins=[0, .2, .4, .6, .8, 1], alpha=.5, label=label)
plt.xlabel("Normalized Yoda style score"); plt.ylabel("Number of texts")
plt.legend(); plt.title("OpenRouter judge: " + JUDGE_MODEL_ID)
plt.savefig(SERVICE_DIR / "judge_score_distribution.png"); plt.show()
plt.figure()
plt.bar([row["type"] for row in summary], [row["mean"] for row in summary],
        yerr=[row["std"] for row in summary])
plt.ylim(0, 1); plt.ylabel("Mean normalized score")
plt.savefig(SERVICE_DIR / "judge_score_comparison.png"); plt.show()
print(summary)

# %% [markdown]
# Change only the rubric for three fixed probes. Compare the actual 100-update
# and 200-update Yoda adapters using the saved six matched held-out questions
# and generated texts from the verified full-run experiment. Reuse text, not
# earlier local judge scores. Select the adapter with the better measured mean
# on these six held-out questions; ties retain the original 200-update model.
# The official test text is never used for model selection.

# %%
prompt_variants = {
    "course_example": system_prompt,
    "strict_syntax": 'Score how closely text matches Yoda speech, emphasizing natural object-subject-verb inversions and wise concise phrasing. Do not reward mere keywords. Return only JSON {"score": number from 0 to 10}.',
    "balanced_content": 'Score Yoda style from 0 to 10, considering inverted syntax, distinctive wise tone, readability and coherent meaning together. Return only JSON {"score": number from 0 to 10}.',
}
prompt_rows = []
for label, rubric in prompt_variants.items():
    for text in test_texts:
        prompt_rows.append({"rubric": label, "text": text, "score": judge.score(text, system_override=rubric).value})
        write_csv(SERVICE_DIR / "judge_prompt_experiments.csv", prompt_rows)
record_service_task("judge_prompt_experiments", trials=9, fixed_probe_texts=True)
duration_source = read_csv(TRAIN_DIR / "yoda_training_duration_experiments.csv")
assert len(duration_source) == 12
questions_by_duration = {updates: [row["question"] for row in duration_source if int(row["updates"]) == updates]
                         for updates in (100, 200)}
assert questions_by_duration[100] == questions_by_duration[200] == [row["question"] for row in heldout_rows[:6]]
duration_rows = []
for row in duration_source:
    assert row["text"].strip()
    duration_rows.append({"updates": int(row["updates"]), "question": row["question"], "text": row["text"],
                          "score": judge.score(row["text"]).value})
    write_csv(SERVICE_DIR / "yoda_training_duration_experiments.csv", duration_rows)
duration_summary = []
for updates in (100, 200):
    values = [row["score"] for row in duration_rows if row["updates"] == updates]
    duration_summary.append({"updates": updates, "mean": statistics.mean(values), "std": statistics.pstdev(values)})
write_csv(SERVICE_DIR / "training_duration_summary.csv", duration_summary)
selected_duration = max(duration_summary, key=lambda row: (row["mean"], row["updates"]))
SELECTED_UPDATES = selected_duration["updates"]
SELECTED_ADAPTER = TRAIN_MODELS / ("yoda_final" if SELECTED_UPDATES == 200 else "yoda_step100")
record_service_task("training_duration_experiments", trials=12, groups=duration_summary,
                    matched_questions=True, generation_temperature=.7, generated_texts_reused_from_verified_training=True,
                    selected_adapter=str(SELECTED_ADAPTER), selected_updates=SELECTED_UPDATES,
                    selection_rule="Higher API-judge mean on six fixed held-out questions; ties prefer 200 updates.",
                    official_test_used_for_selection=False)
print("Rubric results:", prompt_rows)
print("Training-duration results:", duration_summary)

# %% [markdown]
# Load the actual verified LoRA adapter selected by the measured API judge into
# the original public model. Both snapshots came from the full training run.
# This needs a Colab GPU but performs no training. Save generated monitoring
# answers before judging them, so a quota pause does not repeat generation.

# %%
import torch
from torch.nn import functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import mitdeeplearning as mdl
assert torch.cuda.is_available(), "Choose a hosted Colab GPU to load the saved performer."
tokenizer = AutoTokenizer.from_pretrained(TRAIN_MODELS / "yoda_final")
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token
base_model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16,
                                                device_map={"": "cuda"}, low_cpu_mem_usage=True,
                                                **({"revision": BASE_MODEL_REVISION} if BASE_MODEL_REVISION else {}))
if BASE_MODEL_REVISION:
    assert base_model.config._commit_hash == BASE_MODEL_REVISION
record_service_task("restored_performer", public_base_model=MODEL_ID,
                    revision_used=getattr(base_model.config, "_commit_hash", None),
                    original_training_revision_recorded=bool(BASE_MODEL_REVISION),
                    verified_adapter_path=str(SELECTED_ADAPTER), selected_updates=SELECTED_UPDATES)
model = PeftModel.from_pretrained(base_model, SELECTED_ADAPTER, is_trainable=False).eval()
model.config.use_cache = True
assert sum(parameter.numel() for parameter in model.parameters()) < 2_000_000_000

def question_prompt(question):
    return tokenizer.apply_chat_template([{"role": "user", "content": question}],
                                         tokenize=False, add_generation_prompt=True)

def chat(question, max_new_tokens=32, temperature=.7, only_answer=True):
    inputs = tokenizer(question_prompt(question), return_tensors="pt", add_special_tokens=False,
                       truncation=True, max_length=512).to(model.device)
    torch.manual_seed(42)
    with torch.inference_mode():
        outputs = model.generate(**inputs, do_sample=temperature > 0, max_new_tokens=max_new_tokens,
                                 **({"temperature": temperature} if temperature > 0 else {}),
                                 use_cache=True, pad_token_id=tokenizer.pad_token_id)
    tokens = outputs[0, inputs.input_ids.shape[1]:] if only_answer else outputs[0]
    return tokenizer.decode(tokens, skip_special_tokens=True)

# %% [markdown]
# Genuine `@opik.track` inference writes the normalized judge feedback score.
# After flushing, retrieve the actual trace from the server and check its
# output and feedback. The displayed project link comes from the Opik SDK.
# Inspect the trace IDs in that UI before recording the final human check.

# %%
MONITOR_PATH = SERVICE_DIR / "monitored_inference.json"
monitored = read_json(MONITOR_PATH) if MONITOR_PATH.exists() else {}
monitor_questions = [
    "Who was the only non-Jedi to wield a lightsaber in the original Star Wars trilogy?",
    "Explain why practice matters.",
    "Give advice about learning a new skill.",
]

def prepare_monitor_answer(question):
    monitor_id = hashlib.sha256(question.encode()).hexdigest()
    if monitor_id not in monitored:
        monitored[monitor_id] = {"question": question,
                                 "max_new_tokens": 32, "temperature": .7, "adapter_verification_id": verification_id,
                                 "selected_updates": SELECTED_UPDATES}
        atomic_json(MONITOR_PATH, monitored)
    return monitor_id

@track(project_name=os.environ["OPIK_PROJECT_NAME"], capture_input=True, capture_output=True)
def inference_chat(question, monitor_id):
    item = monitored[monitor_id]
    assert item["question"] == question and item["adapter_verification_id"] == verification_id
    assert item["selected_updates"] == SELECTED_UPDATES, "Do not reuse monitoring answers from another selected adapter."
    trace_id = opik_context.get_current_trace_data().id
    item["trace_id"] = trace_id
    atomic_json(MONITOR_PATH, monitored)
    reused = "answer" in item
    if not reused:
        answer = chat(question, max_new_tokens=32, temperature=.7, only_answer=True)
        assert answer.strip()
        item.update(answer=answer, generated_utc=utc_now(), initial_inference_trace_id=trace_id)
        atomic_json(MONITOR_PATH, monitored)
    # A retry after a quota pause reuses this exact adapter/input answer.
    result = item["answer"]
    value = judge.score(result).value
    item.update(score=value, scored_utc=utc_now())
    atomic_json(MONITOR_PATH, monitored)
    opik_context.update_current_trace(
        output={"answer": result}, metadata={"training_run_id": TRAINING_RUN_ID,
            "judge": JUDGE_MODEL_ID, "verification_id": verification_id, "selected_updates": SELECTED_UPDATES,
            "generated_answer_reused": reused, "initial_inference_trace_id": item["initial_inference_trace_id"]},
        feedback_scores=[{"name": "Yoda style eval", "value": value}])
    return {"answer": result}

def verify_opik_trace(monitor_id):
    item = monitored[monitor_id]
    # The decorator's cached client is explicitly flushed too; it can use a
    # different batching configuration than the explicit verification client.
    opik.flush_tracker(timeout=45)
    assert opik_client.flush(timeout=45), "Opik delivery did not flush completely. Resume verification later."
    # Eventual consistency: bounded read-only retries do not issue judge calls.
    observed = None
    for attempt in range(5):
        try:
            trace = opik_client.get_trace_content(item["trace_id"])
            observed = trace.model_dump(mode="json")
            scores = observed.get("feedback_scores") or []
            matching = [score for score in scores if score.get("name") == "Yoda style eval"]
            if (observed.get("id") == item["trace_id"] and observed.get("output", {}).get("answer") == item["answer"]
                    and matching and abs(float(matching[0]["value"]) - item["score"]) < 1e-9):
                break
            observed = None
        except Exception:
            observed = None
        if attempt < 4:
            time.sleep(2)
    if observed is None:
        raise ServicePause("Opik trace/feedback is not yet verified on the server. The ID is saved; resume this cell without new judge calls.")
    trace_path = SERVICE_DIR / ("opik_server_trace_" + item["trace_id"] + ".json")
    atomic_json(trace_path, observed)
    item.update(server_verified=True, verified_utc=utc_now(), project_url=project_url,
                server_trace_file=str(trace_path), server_trace_sha256=sha256_file(trace_path))
    atomic_json(MONITOR_PATH, monitored)

for question in monitor_questions:
    monitor_id = prepare_monitor_answer(question)
    item = monitored[monitor_id]
    if not item.get("server_verified"):
        if "score" not in item:
            inference_chat(question, monitor_id)
        elif not item.get("trace_id"):
            raise RuntimeError("A scored monitor result lacks a real Opik trace ID; review this inconsistent artifact.")
        verify_opik_trace(monitor_id)
    print("Trace:", item["trace_id"], "score:", item["score"], "answer:", item["answer"])
record_service_task("inference_monitoring", examples=3, trace_ids=[item["trace_id"] for item in monitored.values()],
                    server_verified=True, project_url=project_url, original_example_question_included=True)
from IPython.display import Markdown, display
display(Markdown("[Open the genuine Opik project and inspect these trace IDs](" + project_url + ")"))

# %% [markdown]
# Re-execute the official unchanged test-text measurement on the restored
# selected adapter. This is mean next-token negative log likelihood, although
# the original course label calls it loglikelihood. No test text is modified.

# %%
yoda_test_text = mdl.lab3.yoda_test_text
model.config.use_cache = False
tokens = tokenizer(yoda_test_text, return_tensors="pt").to(model.device)
with torch.no_grad():
    outputs = model(**tokens)
    logits = outputs.logits[:, :-1]
    targets = tokens.input_ids[:, 1:]
    loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
nll = float(loss)
assert math.isfinite(nll)
saved_nll = training_tasks["official_yoda_test_nll"]["mean_negative_log_likelihood"]
if SELECTED_UPDATES == 200:
    assert abs(nll - saved_nll) < .01, "Restored final adapter does not reproduce the saved original test measurement."
record_service_task("official_yoda_test_nll", mean_negative_log_likelihood=nll,
                    mean_log_likelihood=-nll, perplexity=math.exp(nll),
                    test_tokens=int(targets.numel()), original_text_unchanged=True,
                    selected_updates=SELECTED_UPDATES, original_200_update_measurement=saved_nll,
                    prior_200_update_measurement_matches=(abs(nll - saved_nll) < .01) if SELECTED_UPDATES == 200 else None)
print("Yoda test mean negative log likelihood:", nll)
del outputs, logits, targets, model, base_model
gc.collect(); torch.cuda.empty_cache()

# %% [markdown]
# Record measured analysis and identify what the judge comparison supports.
# Scores from different judges are not directly comparable. Positive controls
# are training texts, while generated questions are held out. Rubric sensitivity
# and the fixed 100/200-update experiment select the measured better adapter,
# without
# tuning against the official test text. Personal understanding is not claimed.

# %%
analysis = (
    "MIT Lab 3 service continuation using verified training run " + TRAINING_RUN_ID + ".\n\n"
    "Judge: " + JUDGE_MODEL_ID + "; actual OpenRouter responses and genuine Opik metric.\n\n"
    "Control/generation mean and population standard deviation: " + json.dumps(summary) + ".\n\n"
    "Fixed-probe rubric experiment: " + json.dumps(prompt_rows) + ".\n\n"
    "100/200-update matched held-out-question experiment: " + json.dumps(duration_summary) + ".\n\n"
    "Selected adapter: " + str(SELECTED_UPDATES) + " updates, using the larger mean API-judge score on six matched held-out questions. "
    "Ties prefer the original 200-update adapter. This small validation comparison may be noisy; it is not official-test tuning. "
    "Increasing judge scores does not prove factual correctness or generalization. "
    "Training controls, held-out generations, different rubrics, and judge models have different interpretation limits.\n\n"
    "Unmodified official test-text mean NLL: " + str(nll) + "; lower is better.\n\n"
    "Verified Opik project: " + project_url + ". Trace IDs: "
    + json.dumps([item["trace_id"] for item in monitored.values()]) + ".\n"
)
(SERVICE_DIR / "exercise_analysis.md").write_text(analysis, encoding="utf-8")
record_service_task("experiment_analysis", path=str(SERVICE_DIR / "exercise_analysis.md"),
                    measured_results=True, training_comparison_used=True)

# %% [markdown]
# After opening the genuine Opik UI, inspect at least the original monitored
# question, generated answer, normalized feedback, and trace ID. Only then
# set the checkbox and write a brief observation. This final cell can be run
# on its own after the preceding cells; it does not send more API requests.

# %%
OPIK_UI_INSPECTED = False  #@param {type:"boolean"}
OPIK_UI_OBSERVATION = ""  #@param {type:"string"}
needed_service_tasks = ["verified_full_training", "service_configuration", "genuine_opik_custom_metric",
                        "judge_probe_sentences", "judge_controls_and_generations", "judge_prompt_experiments",
                        "training_duration_experiments", "inference_monitoring", "official_yoda_test_nll",
                        "experiment_analysis"]
assert all(task in SERVICE_TASKS for task in needed_service_tasks)
assert all(item.get("server_verified") and item.get("trace_id") for item in monitored.values())
observed_ui = OPIK_UI_INSPECTED and bool(OPIK_UI_OBSERVATION.strip())
if observed_ui:
    record_service_task("opik_ui_inspection", observed_by="user_or_authorized_browser_operator",
                        observation=OPIK_UI_OBSERVATION.strip(), project_url=project_url,
                        trace_ids=[item["trace_id"] for item in monitored.values()], checked_utc=utc_now())
completion = {
    "recorded_utc": utc_now(), "training_run_id": TRAINING_RUN_ID,
    "verification_id": verification_id, "judge": JUDGE_MODEL_ID,
    "selected_performer_updates": SELECTED_UPDATES,
    "official_api_metric_and_server_trace_exercises_completed": True,
    "opik_ui_inspection_recorded": observed_ui,
    "official_lab3_service_exercises_completed": observed_ui,
    "full_provider_course_completion_claimed": False,
    "personal_understanding_or_authorship_claimed": False,
    "competition_entry_submitted": False,
    "service_task_evidence_path": str(EVIDENCE_PATH),
    "opik_project_url": project_url,
    "trace_ids": [item["trace_id"] for item in monitored.values()],
    "judge_attempt_count_for_this_continuation": sum(len(read_json(path)["attempts"]) for path in REQUEST_DIR.glob("*.json")),
}
atomic_json(SERVICE_DIR / "service_completion.json", completion)
print(json.dumps(completion, indent=2))
if not observed_ui:
    print("API scoring and actual Opik server traces passed; the explicit UI inspection remains to be recorded.")
