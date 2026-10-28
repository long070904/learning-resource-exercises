# Saved exercise results

This folder brings together saved outputs from Colab and local runs. Use the
[exercise results table](EXERCISE_RESULTS.md) to inspect a result, or the main
[code and result index](../WORK_INDEX.md) to find both its source and output.

The audit dated 25 October 2026 records **64 saved executions from 84 exercises**,
with **20 still pending**:

| Resource | Saved executions | Exercise entries |
|---|---:|---:|
| Google MLCC | 7 | 7 |
| MIT 6.S191 | 11 | 12 |
| fast.ai Part 1 | 24 | 25 |
| fast.ai Part 2 | 22 | 40 |

These counts describe the saved exercise collection. They do not establish
provider course certification, lecture attendance or personal understanding.
The fast.ai wearable-training notebook also has an unfilled personal ethics
response, despite its saved technical outputs.

## What is included

- `saved_notebooks/`: all 64 course result notebooks and a separate synthetic
  Python signal-processing companion.
- `audio/`: two original generated music WAV files from the MIT exercises.
- `figures/`: selected saved images and teaching plots.
- `metrics/`: selected numerical results and supporting validation records.

Of the 64 course result notebooks, 42 are exact copies of the original saved
files. The other 22 have documented privacy or file-size changes. Their code,
execution counts and existing scientific outputs are preserved. Where a large
duplicate image encoding or inline audio was removed, the publication record
identifies that change.

## Checking a file

[RESULT_FILES.json](RESULT_FILES.json) lists the original and published hashes,
file sizes, changes and associated evidence. Use its published-file hashes to
check copies in this repository. The older hashes in
[EXERCISE_STATUS.csv](EXERCISE_STATUS.csv) and
[PROGRESS_SNAPSHOT.json](PROGRESS_SNAPSHOT.json) identify the original saved
files. [PUBLISHED_RESULT_INDEX.csv](PUBLISHED_RESULT_INDEX.csv) maps all 84 source
entries to their published results, where available.

DDPM15 retains the error from its original validation-curve check. A separate
recovery audit supports its saved completion record; the notebook itself is
not an error-free execution. Other outputs may retain historical runtime paths
or settings. Use the main course source folders when starting a new run.

The complete original notebooks, repeated run histories, dataset archives and
model checkpoints remain in the separate local collection and verified offline
cloud backup. No training or inference was performed to prepare these publication
copies. The wearable-style and signal-processing examples use synthetic data;
their plots and scores are teaching results, not physiological research findings.
