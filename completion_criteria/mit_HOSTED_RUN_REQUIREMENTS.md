# MIT lab execution requirements

This guide describes the full-run settings and evidence checks used for the
prepared MIT notebooks. It is not the current progress report: the
[saved-result index](../results/EXERCISE_RESULTS.md) records 11 of 12 MIT entries
with saved execution evidence. The separate Lab 3 service continuation remains
pending. Local syntax, shape and data-loading checks alone do not count as
completed training.

The nine original-course notebooks were arranged in this order:

1. `01_pt_tensor_and_gradient_exercises.ipynb`
2. `01_tf_tensor_and_gradient_exercises.ipynb`
3. `02_pt_music_generation.ipynb`
4. `02_tf_music_generation.ipynb`
5. `05_pt_lab2_mnist.ipynb`
6. `05_tf_lab2_mnist.ipynb`
7. `06_pt_lab2_debiasing.ipynb`
8. `06_tf_lab2_debiasing.ipynb`
9. `07_lab3_llm_finetuning.ipynb`

The wearable recurrent-model and Transformer/contrastive notebooks are separate
synthetic practice examples. They are not replacements for MIT Labs 2–3 or
completed physiological research implementations.

## Runtime and dependencies

For the hosted workflow, run one notebook kernel at a time with `QUICK_RUN=False`
and the shared `colab_runtime.py` setup. Start a fresh kernel when changing
frameworks. Avoid overlapping PyTorch and TensorFlow GPU allocations. The
recorded Colab setup used a T4 with about 15 GB GPU memory and 12.7 GB system RAM;
check the resources actually assigned before starting another run.

Keep Colab's working torch/torchvision/CUDA combination. The `mit` profile adds
`mitdeeplearning==0.7.5`, `torchsummary`, `h5py` and OpenCV. The course package
imports TensorFlow even in PyTorch notebooks, so TensorFlow must be importable
without taking over GPU memory during PyTorch training.

The prepared TensorFlow range permits 2.21. TensorFlow 2.21.0 has Linux cp313
wheels, so Python 3.13 should not be rejected merely because of an assumed lack
of a matching wheel. A successful install still needs an actual import and GPU
probe. See the [TensorFlow installation guide](https://www.tensorflow.org/install/pip)
and the [2.21.0 release files](https://pypi.org/project/tensorflow/2.21.0/).

## Exercise requirements

| Exercise | Full-run requirements |
|---|---|
| Music generation | Install `abcmidi`, `timidity` and `fluid-soundfont-gm` if needed. Generate ABC, render a nonempty WAV, display audio and retain ABC/MIDI/WAV files. An unsuccessful conversion leaves the exercise incomplete. |
| MNIST | Keep the original 60,000/10,000 split. Compare optimiser settings on 54,000 training and 6,000 validation examples for two epochs per candidate, then train the selected model afresh on all 60,000 examples. Final budgets are five epochs for the fully connected model and seven PyTorch/five TensorFlow epochs for the CNN. TensorFlow also runs the full explicit `GradientTape` epoch with batch size 12. Test data is not used for selection. |
| Debiasing | Use the official CelebA/ImageNet HDF5 teaching dataset, with no synthetic fallback. The loader streams `uint8` images and converts batches to `float32`. Adaptive sampling considers all positive faces in small latent chunks. Both classifier and DB-VAE use the full source dataset for two nominal epochs of balanced stochastic sampling, with `N//32` steps per epoch. This sampling budget does not guarantee that every example is visited. Download or schema failures stop the exercise. |
| Lab 3 training | Use public `LiquidAI/LFM2-1.2B` and the course Dolly/style data. The frozen base uses `float16`; rank-8 LoRA parameters and loss use `float32`. Settings are context 512, gradient checkpointing, batch size one and Lion learning rate `1e-4`. Each style requires 200 successful optimiser updates. Leprechaun and Yoda runs start independently from the original base weights. |
| Lab 3 local judge | The adapted judge is `Qwen/Qwen2.5-3B-Instruct` in `float16`, with context bounded to 1,536 tokens. The recorded T4 budget allowed roughly 6 GB of judge weights alongside roughly 2.4 GB for the performer. Release the judge before checkpoint restoration. Preserve a real memory failure; do not quietly replace the judge or omit evaluation. |

Lab 3 uses `transformers>=4.55,<5`, `peft>=0.17,<1`, `accelerate>=1,<2`,
`datasets>=3,<5`, `lion-pytorch` and `mitdeeplearning==0.7.5`. The public models
do not require a mandatory Hugging Face token. Optional accelerated LFM2
convolution kernels are not required for the compatibility check.

## Lab 3 service work

Local Qwen scores and JSON traces are adaptations of the original hosted judge
and Opik tasks. They do not establish Gemini/OpenRouter scores or completion of
the hosted services. `RUN_HOSTED_JUDGE=False` and `RUN_OPIK_REMOTE=False` are the
defaults, and no paid API calls are made by default. The final record leaves
`official_service_exercises_completed` false unless both service modes run.

The [service-continuation guide](../02_mit_6s191/08_lab3_service_continuation_README.md)
sets out the account, saved-training and UI checks still required. No competition
submission is part of this workflow.

## Saved evidence

Each original notebook writes a unique
`results/<notebook>/<UTC-run-id>/task_evidence.json` and its model artifacts.
Required checks must be present before `finish_run` writes a final record.
Runtime versions and Colab provenance are recorded. Keep the executed notebook,
including any errors, alongside the JSON evidence. Filled solution code, a
download, an empty final cell or a synthetic practice result is not sufficient
evidence of the original lab's completion.

The [read-only audit helper](audit_mit_hosted.py) inspects existing files without
importing ML packages, running cells or loading checkpoints. It also requires
`service_scope_audit.json`, which is not included in this repository. Supply the
matching source criteria from the original run with `--scope`; without them,
the helper cannot complete its audit. `--output` writes only the named report;
otherwise it prints JSON.

## Original sources

- [MIT course repository](https://github.com/MITDeepLearning/introtodeeplearning)
- [Music exercise](https://github.com/MITDeepLearning/introtodeeplearning/blob/master/lab1/PT_Part2_Music_Generation.ipynb)
- [HDF5 loader and test groups](https://github.com/MITDeepLearning/introtodeeplearning/blob/master/mitdeeplearning/lab2.py)
- [Dolly/style loader](https://github.com/MITDeepLearning/introtodeeplearning/blob/master/mitdeeplearning/lab3.py)
- [Original Lab 3](https://github.com/MITDeepLearning/introtodeeplearning/blob/master/lab3/LLM_Finetuning.ipynb)
- [Performer model card](https://huggingface.co/LiquidAI/LFM2-1.2B)
- [Adapted judge model card](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct)
- [Chat-template guidance](https://huggingface.co/docs/transformers/chat_templating)
- [Opik custom metric interface](https://www.comet.com/docs/opik/python-sdk-reference/evaluation/metrics/BaseMetric.html)
