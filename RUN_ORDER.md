# Running the exercises

Start with [the Colab setup notebook](START_HERE_COLAB.ipynb), then choose an
exercise from the [work index](WORK_INDEX.md). Each notebook has its own package
profile. A fresh runtime helps avoid conflicts when switching between
TensorFlow, PyTorch and fast.ai.

Save outputs and checkpoints before ending a temporary Colab session. Use the
main course folders for runnable sources and `results/saved_notebooks` to read
earlier outputs.

## Google MLCC

Notebooks 01-04 can be run individually. Use a fresh runtime for
`05_fairness_income_colab.ipynb`: it installs matching TensorFlow/tf-keras
packages and uses MinDiff. Notebook 05b is a separate PyTorch MMD adaptation.
Notebook 06 tests participant-level evaluation with synthetic data.

The [teaching-data downloader](scripts/download_teaching_data.py) can restore
the five omitted public Google/MNIST files and check their original hashes.
Other datasets are obtained through the relevant notebook.

## MIT 6.S191

For Lab 1, run the tensor and gradient exercises before music generation.
PyTorch and TensorFlow versions are included, and each music notebook prepares
its own vocabulary and model. Notebooks 03-04 are wearable modelling companions.

Lab 2 covers MNIST in notebook 05 and facial detection/debiasing in notebook 06.
Choose one framework at a time. The face-data exercise downloads a large
teaching dataset and needs a GPU; it addresses detection and debiasing rather
than face identification.

Lab 3 notebook 07 covers tokenisation, generation, LoRA fine-tuning and a local
judge/tracing adaptation. Notebook 08 contains the separate OpenRouter and Opik
continuation. It needs accounts and Colab Secrets named `OPENROUTER_API_KEY`
and `OPIK_API_KEY`. Read its
[setup notes](02_mit_6s191/08_lab3_service_continuation_README.md) before enabling
service calls. Local judge scores and JSON traces do not replace the service
exercises.

## fast.ai Part 1

Run image notebook 00 before 02 or 03, using the same `QUICK_RUN` value so their
image folders match. Keep the exported learner in persistent storage. In a new
session, notebook 00 also recreates the local images. Notebooks 04-09 can be run
independently.

Notebooks 10-13 cover *Road to the Top*, parts 1-4. Obtain the
[Paddy dataset](https://www.kaggle.com/competitions/paddy-disease-classification/data),
accept its access terms, and place `paddy-disease-classification.zip` at the top
of My Drive or upload it when prompted. These exercises use the competition
data. Batch sizes were reduced for Colab GPUs, but notebook 12's larger model
comparisons and ensemble may still exceed a free T4 session's memory or time.

Notebook 14 needs `us-patent-phrase-to-phrase-matching.zip` from the
[Patent competition](https://www.kaggle.com/competitions/us-patent-phrase-to-phrase-matching/data).
Notebooks 15 and 16 download MovieLens and MNIST automatically. Their
`QUICK_RUN` option uses smaller real-data samples and one epoch per model.
Deployment account setup and personal ethics responses remain learner tasks.

Notebooks 17-24 contain the full course22 clean notebooks 00-07, alongside the
shorter companions 00-07. They retain training and export steps, historical timm
benchmark analysis, manual network experiments, Titanic model comparisons and
ensemble work, and random forests. The full Titanic exercises use public copies
of the original 891 training and 418 test rows. They save predictions without
making a competition submission. Work through 17-24 in order, then the other
full exercises 08-16 as needed.

## fast.ai Part 2

Begin with the three notebooks in `diffusion_intro` for Lessons 9-10, then work
through the numbered notebooks in the main folder. The included `miniai`
package supports imports without rerunning nbdev exports. Original numbering
is kept, including 16A/16B and the variants of 22, 24 and 30.

Use a GPU for the longer image runs. The supplied settings use batches of 8 for
heavy image work and 32 for smaller Fashion MNIST work, retaining the original
training durations. These batch changes affect the experiment conditions.
`QUICK_RUN` does not shorten the Part 2 loops. Full diffusion or ImageNet work
may need several sessions.

Some later notebooks depend on earlier saved models:

| Notebook | Prerequisite work | Files needed in the persistent models folder |
|---|---|---|
| 18_fid | 14_augment and 17_DDPM_v2 | `data_aug2.pkl`, `fashion_ddpm_mp.pkl` |
| 19_DDPM_v3 | 14_augment | `data_aug2.pkl` |
| 20_DDIM | 14_augment and 19_DDPM_v3 | `data_aug2.pkl`, `fashion_ddpm3_25.pkl` |
| 22 variants, 23, 26 and 28 | 14_augment | `data_aug2.pkl` |
| 25_superres | 24_imgnet_tiny | `inettiny-custom-25` and local Tiny ImageNet data |

Setup reports missing checkpoints before long training starts. Whole-model
pickle files contain executable Python objects, so load only trusted outputs.

Notebook 31 is the full ImageNet latent experiment. Its local route needs
original CLS-LOC images at `data/ILSVRC/Data/CLS-LOC`, plus
`imagenet_lsvrc_2015_synsets.txt` and `words.txt` in `data/ILSVRC`. The optional
official Hugging Face streaming route needs approved access, a scoped
`HF_TOKEN` and the original synset metadata. It pins the dataset revision and
checks the label mapping.

The full experiment uses 1,281,167 training and 50,000 validation examples.
Streaming reduces raw-image storage, but the float32 latent cache still needs
about 27.26 GB on the runtime disk. Only manifests, checkpoints and results
persist to Drive. Tiny ImageNet and LSUN exercises also need substantial disk
space. Temporary inputs disappear when the runtime is deleted.

## Scope

The [source index](EXERCISE_INDEX.md) lists the 84 exercises included here:
MIT Labs 1-3, the listed Part 1 exercises and companions, the numbered
course22p2 notebooks, and three diffusion introductions. Archived extra labs,
scratch notebooks and every book chapter are outside this collection.
Google quizzes and interactive widgets remain on the provider's site, with
completion separate from the Python notebooks.
