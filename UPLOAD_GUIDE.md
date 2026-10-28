# Maintaining the repository

The local checkout is `GitHub_Learning_Resources`. It is connected to the public
[learning-resource-exercises repository](https://github.com/long070904/learning-resource-exercises).
Open this folder in GitHub Desktop when updating the work.

## Adding new work

1. Put the source in its existing course folder.
2. Add a useful saved notebook or small output to `results`, and update the
   [work index](WORK_INDEX.md). Label unfinished or unsuccessful runs clearly.
3. Review the changed files for credentials, personal paths, large datasets and
   model checkpoints before committing.
4. Commit the changes and use **Push origin**. This checkout already has a
   remote; it does not need a nested repository.

The `.gitignore` covers common checkpoint, archive, credential and environment
files. Still review each upload, particularly notebooks with saved output.

## What belongs here

Keep runnable code, short instructions, useful figures, metrics and selected
saved notebooks. Keep course credits and local-adaptation notes with the work.

Store full checkpoints, raw datasets, environments and private assessment
documents in the offline backup or another suitable location. The parent
workspace contains more than the GitHub project and is not the upload folder.

## Full backups

`Offline_Backup_2026-10-27` contains the 1,778-file cloud snapshot, including
larger results, logs and checkpoints. Its `INDEX.html` opens the backup inventory.
`ALL_LEARNING_RESOURCES_2026-10-25` retains the original local review collection.
Both folders are separate from this checkout.

Historical hashes are retained in `provenance` and `results/RESULT_FILES.json`.
Preserve those records when editing documentation and refresh the current
[file checksums](FILES_SHA256.json).
