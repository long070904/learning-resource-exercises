# Learning resource exercises

Course notebooks, small experiments and saved results for my wearable
emotion-recognition project. The work covers Google MLCC, MIT 6.S191, fast.ai
Parts 1 and 2, and MathWorks signal processing. Results come from both Colab and
local runs.

Start with the **[exercise and results index](WORK_INDEX.md)** to open a notebook
and its saved output. The **[MathWorks certificates](certificates/README.md)** are
listed separately.

## Browse the courses

| Resource | What's included |
|---|---|
| [Google MLCC](01_google_mlcc/README.md) | Regression, classification, numerical data, fairness and participant-level evaluation |
| [MIT 6.S191](02_mit_6s191/README.md) | Tensors, music generation, computer vision, language models and wearable modelling examples |
| [fast.ai Part 1](03_fastai/README.md) | Image and tabular models, Paddy classification, NLP, collaborative filtering and companions |
| [fast.ai Part 2](04_fastai_part2/README.md) | Neural-network foundations, diffusion, style transfer and latent-image experiments |
| [MathWorks](05_mathworks/README.md) | Academy lesson exports, signal-processing practice and a separate Python companion |

## Progress


MathWorks is outside this notebook count. Onramp and all four Core courses are
complete, along with the overlapping Core learning path. Completion was checked
on **27 October 2026**. Six certificate views and the completed-courses overview
are in the certificate folder. Local MATLAB startup error 5201 remains
unresolved; the Python companion has its own saved results.

## Run an exercise in Colab

1. Open [START_HERE_COLAB.ipynb](START_HERE_COLAB.ipynb) in Colab.
2. Follow its instructions to set up the files at
   `/content/HaiLong_Colab_Exercises`.
3. Choose an exercise and read its setup cell and the [run guide](RUN_ORDER.md).

This repository is public, so the source ZIP and public-clone route are
available without a GitHub token. Each course has its own packages, datasets
and checkpoint requirements. Setup lists the exercises; training starts when
the chosen exercise is run.

Use the main course folders for runnable sources. Copies in
[`results/saved_notebooks`](results/saved_notebooks) are useful for reading
outputs, but some retain paths and settings from their original environments.
The two [local variants](local_variants/README.md) still need full execution.

## Files and backups

This repository keeps code, selected figures and metrics, two generated music
samples and the MathWorks certificate captures. Large checkpoints, raw dataset
archives, caches, environments and private assessment documents are stored
separately. Full online and local backups remain outside this checkout.

[UPLOAD_GUIDE.md](UPLOAD_GUIDE.md) explains how to maintain this smaller copy.
The [merge record](provenance/ONLINE_OFFLINE_MERGE.json) describes how Colab and
local results were brought together.

## Sources and adaptations

The collection includes instructor material and AI-assisted adaptations.
[SOURCES.md](SOURCES.md), [the source index](EXERCISE_INDEX.md) and retained
licence notices identify the original resources. Synthetic wearable examples
are teaching exercises, rather than evaluations on physiological benchmarks.

Original source hashes and publication changes are recorded in
[`provenance`](provenance). Some result copies were made smaller or had private
paths removed for publication; [RESULT_FILES.json](results/RESULT_FILES.json)
records those edits. Current checksums are in [FILES_SHA256.json](FILES_SHA256.json).
