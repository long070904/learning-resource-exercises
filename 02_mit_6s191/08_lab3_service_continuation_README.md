# Lab 3 hosted-service continuation

[08_lab3_service_continuation.ipynb](08_lab3_service_continuation.ipynb) is prepared
code for the service tasks that follow the saved Lab 3 training run. This entry
remains pending, with no completed service run recorded. It is listed in
`exercise_manifest.json`; the batch runner requires explicit service
authorisation and the configured credentials before it can proceed.

The [original MIT lab](https://github.com/MITDeepLearning/introtodeeplearning/blob/master/lab3/LLM_Finetuning.ipynb)
uses an OpenRouter judge, an Opik custom metric, monitored inference with feedback
and inspection of the Opik interface. Local Qwen scores and JSON traces do not
complete these tasks. The Dropbox contest submission is separate and is not
included here.

## Before running

Use a Colab GPU runtime after the main training batch has finished. Add your own
`OPENROUTER_API_KEY` and `OPIK_API_KEY` to Colab Secrets and grant this notebook
access. The same environment variables are an alternative. `OPIK_WORKSPACE`
optionally selects an existing workspace. Keep keys out of notebook cells,
outputs, Drive artifacts and logs.

The notebook makes no service calls while `AUTHORIZE_SERVICE_CALLS=False`.
Enable it only when you intend to send the reviewed requests through your own
accounts. Paid judging has a separate `ALLOW_PAID_JUDGE` gate.

| Parent-runner setting | Purpose |
|---|---|
| `HAILONG_AUTHORIZE_LAB3_SERVICES=1` | Enables the service-call gate. |
| `HAILONG_ALLOW_PAID_LAB3_JUDGE=1` | Separately allows a paid judge. |
| `HAILONG_LAB3_JUDGE_MODEL` | Selects one of the two documented judge models. |
| `HAILONG_LAB3_TRAINING_RUN_ID` | Selects the exact saved training run to verify. |

These settings are disabled or absent by default. An authorised parent runner
can pass the two required keys and settings to the continuation's subprocess.
The fresh notebook kernel reads environment keys first. Do not print the
environment or pass these credentials to other course notebooks.

## Judge, quotas and resuming

The configured default is `google/gemma-2-9b-it:free`, a larger model than the
1.2B performer. The alternative `google/gemini-2.5-flash` needs
`ALLOW_PAID_JUDGE=True` and account credit. Check the provider's current model
availability, prices and account quotas before starting; the model identifier
and earlier free-tier assumptions are not a guarantee of service availability.

The notebook's own defaults permit 45 requests per session and rolling 24 hours,
with at least 3.2 seconds between new requests. Other applications share the
same account quota, so run one continuation at a time and leave headroom.
Failed requests may also consume quota.

The original three probes, 20/20/20 comparison and monitored example require
64 logical evaluations. The continuation adds nine rubric trials, twelve
matched training-duration trials and three monitored questions: 87 logical
evaluations in total. Exact duplicate text/rubric requests can reuse saved real
responses, so fewer new API calls may be needed. A quota-limited run may need
more than one day.

Requests, raw responses, normalised scores, failure types and remaining steps
are saved in Drive. Automatic OpenAI SDK retries are disabled. A delivery-uncertain
request requires `RETRY_UNCERTAIN_REQUESTS=True` before another attempt; a failed
request or malformed score requires `RETRY_FAILED_REQUESTS=True`. Neither is
silently retried or given an invented score. A server 429 stops further requests
for 24 hours.

Relevant provider pages:

- [Configured Gemma judge](https://openrouter.ai/google/gemma-2-9b-it:free)
- [Alternative Gemini judge](https://openrouter.ai/google/gemini-2.5-flash)
- [OpenRouter free-tier guidance](https://openrouter.ai/blog/tutorials/how-to-get-the-lowest-cost-llm-inference-on-openrouter/)
- [Opik cloud quickstart](https://www.comet.com/docs/opik/quickstart)
- [Opik plans](https://www.comet.com/site/pricing/)
- [Opik SDK configuration](https://www.comet.com/docs/opik/tracing/advanced/sdk_configuration)

This continuation uses Opik cloud authentication. A self-hosted Opik server is
a vendor-supported alternative, but this notebook does not deploy one. Check
the account's current limits and retention settings rather than relying on an
old plan allowance.

## Verifying the saved training run

Before reading keys or sending requests, the notebook checks:

- The runner record, every executed code cell, full-run mode, the saved output
  notebook hash and the approved prepared-source hash.
- A matching run ID, original exercise evidence, two real 200-update histories,
  saved adapters and the adapter restoration check.
- The hashes of the training JSON, generation/control CSVs, training-duration
  texts and adapter files. Changed artifacts prevent resumption.

The approved prepared Lab 3 source hash is
`de35ad31546210e89f3b1355b08f3d58ffed9029cf6e1092d944209dd20a6f6a`.
If that source changes, review the change and update the approved hash before
using the continuation. An incomplete or reduced training run must finish its
training requirements first. The continuation neither loads an unrelated
adapter nor starts a new training run.

Service outputs are stored under:

```text
MyDrive/HaiLong_Colab_Results/02_mit_6s191/results/07_lab3_llm_finetuning/<actual-training-run-id>/official_services_<judge-id-hash>/
```

The shared quota ledger is `results/lab3_openrouter_attempt_ledger.json`. Resume
with the same training run and judge. The original rubric, probes, held-out
generations, positive/negative controls, distributions, rubric comparison,
100/200-update comparison and monitored question remain explicit. Verified
generation texts may be reused; old local judge scores are discarded. Genuine
Opik tracing covers the initial inference. If a saved answer is reused after a
quota interruption, the new trace records the reuse and initial trace ID.

## Feedback and the Opik interface

Actual Opik traces are flushed and fetched back from the server. Their output,
feedback score and trace ID must agree with the saved inference. The project
link comes from `Opik.get_project_url()`. Open it and inspect the trace input,
output and feedback before setting `OPIK_UI_INSPECTED=True` and entering a brief
observation. Server/API completion and this personal UI check are separate.

The API judge compares the 100-update and 200-update adapters on six matched
held-out questions, selecting the higher mean score; ties retain 200 updates.
Both adapters must come from the verified training run. This is a small
validation comparison, not a general performance claim. The selected adapter
then re-runs the original unchanged Yoda test-text next-token negative log
likelihood. If the 200-update adapter is retained, the measurement must agree
with the saved run. The test text is not used to select an adapter.

## Source and audit support

[08_lab3_service_continuation.py](08_lab3_service_continuation.py) is the readable
cell-based source for the standalone notebook. Its code cells have empty outputs
and no execution counts. Local checks covered syntax, notebook structure,
default refusal to make unauthorised calls, JSON score parsing and missing-root
audit behaviour. They do not establish a successful hosted-service run.

The separate [read-only MIT audit helper](../completion_criteria/audit_mit_hosted.py)
examines saved files without importing ML packages, running cells or loading
checkpoints. Its required `service_scope_audit.json` is not bundled here; supply
the matching original criteria through `--scope`. `--output` writes only the
named JSON report; otherwise results go to standard output. The helper keeps
the nine original course notebooks separate from the two synthetic prototypes.
