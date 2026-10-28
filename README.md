# Learning resource exercises and saved results

## Certificate evidence added 28 October 2026

[Open all six MathWorks certificate screenshots and the completed-courses overview](certificates/README.md).
The images and official certificate links are now included in this repository;
exact offline originals remain preserved. The verification date remains 27 October 2026.

Combined course code and selected results from Google Machine Learning Crash
Course, MIT 6.S191, fast.ai Parts 1 and 2, and MathWorks signal-processing study.
The collection brings together hosted Colab work and local execution evidence.
It was organised on 27 October 2026; no training was rerun during preparation.

Start with **[WORK_INDEX.md](WORK_INDEX.md)** to open an exercise and its saved
result. **[results/README.md](results/README.md)** explains the result copies and
the differences between original evidence and compact publication versions.

| Folder | What to open |
|---|---|
| `01_google_mlcc` | 7 Google exercise and companion source notebooks |
| `02_mit_6s191` | 12 MIT course and application source notebooks, plus helpers |
| `03_fastai` | 25 Part 1 exercise and companion source notebooks |
| `04_fastai_part2` | 40 Part 2 source notebooks, miniai and diffusion helpers |
| `certificates` | Original MathWorks certificate screenshots, completion overview and verification links |
| `05_mathworks` | Academy MATLAB exports, practice scripts and a Python companion |
| `results/saved_notebooks` | Saved outputs for all 64 audited exercises and the separate Python signal companion |
| `results/audio`, `results/figures`, `results/metrics` | Small selected outputs and bound evidence files |
| `local_variants` | Two reviewed local source fixes for pending Part 2 exercises |
| `scripts` | Colab setup and optional teaching-data download helpers |
| `completion_criteria`, `provenance` | Scope, source attribution, original hashes and publication changes |

## What has been executed

The audited 25 October snapshot records **64 of 84** exercise notebooks with
saved execution evidence: Google 7/7, MIT 11/12, fast.ai Part 1 24/25 and Part 2
22/40. Twenty remain pending. These counts do not establish provider certificates
or personal mastery. MathWorks hosted activities have separate progress and are
not included in the 84-notebook count.

The 27 October online backup was checked against the local collection. The newer
canonical source set already covers the useful online code. Older repair
launchers and repeated source archives were omitted. Both hosted and local native
result notebooks are represented; a later download date alone did not supersede
a newer validated local run. See [the merge record](provenance/ONLINE_OFFLINE_MERGE.json).

## MathWorks completion update — verified 27 October 2026

The refreshed authenticated [MathWorks My Courses](https://matlabacademy.mathworks.com/mycourses)
page shows **Completed (6)**: Signal Processing Onramp, the complete Core pathway
and all four constituent courses. This verifies the student's completion report;
all six official certificate views and their original screenshots are saved
offline. Original provider PDFs have not been downloaded. The two plan allocations total
**1 CP (0.33 + 0.67)** and **12 estimated study hours (4 + 8)**, with the reported
study period extended to 27 October. See the [MathWorks guide](05_mathworks/README.md).
The September account snapshot remains historical. This update does not alter
the 64/84 coding ledger or resolve native MATLAB startup error 5201.

## Run in Colab

Open [START_HERE_COLAB.ipynb](START_HERE_COLAB.ipynb). For a private repository,
download its source ZIP from GitHub using **Code → Download ZIP**, then upload
that ZIP when the bootstrap notebook requests it. Setup places the source and
helpers at `/content/HaiLong_Colab_Exercises`, the path expected by the exercise
notebooks. GitHub account credentials should not be entered in notebook cells.

The bootstrap prepares files; it does not start a batch training run. Open the
chosen exercise and use its existing setup in a fresh runtime. Read
[RUN_ORDER.md](RUN_ORDER.md) for framework profiles, prerequisite checkpoints and
dataset access. Larger external datasets and private service credentials are
obtained separately. The included downloader can restore five omitted Google
and MNIST teaching files and check their original hashes.

Saved result notebooks are evidence for reading. Some contain local execution
variants and historical runtime paths; use the main course folders as the source
launchers. Reviewed variants in `local_variants` remain pending full execution
and are not selected automatically by the 84-entry batch runner.

## What stays offline

The full `Offline_Backup_2026-10-27` folder preserves 1,778 cloud files
(4,244,772,328 bytes) with hashes, receipts and archive checks. The original
`ALL_LEARNING_RESOURCES_2026-10-25` collection also remains intact. They are
separate local folders and should not be included in this Git repository.

This repository omits large trained checkpoints, raw dataset archives, caches,
environments, repeated HTML previews, installation logs, old repair launches and
private assessment documents. Useful images, metrics and two music samples are
retained. The `.gitignore` protects against accidentally adding common heavy or
credential files later.

## Attribution and integrity

These files include instructor material and AI-assisted adaptations. See
[SOURCES.md](SOURCES.md), [EXERCISE_INDEX.md](EXERCISE_INDEX.md),
`exercise_manifest.json` and the retained upstream licence notices. No blanket
replacement licence is applied to this mixed-source collection.

Of the 84 main source notebooks, 83 retain their original bytes; the wearable
ethics source has a documented privacy edit. Compact result derivatives have
their original and publication hashes and change descriptions recorded in
`results/RESULT_FILES.json`. Existing scientific outputs were not regenerated.
`FILES_SHA256.json` lists the current repository payloads.

See [UPLOAD_GUIDE.md](UPLOAD_GUIDE.md) for the local folder and publication state.
