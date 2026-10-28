"""Generate the source-only Colab setup notebook from the reviewed helper."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE if (HERE/'scripts/bootstrap_colab.py').is_file() else HERE.parent
helper=(ROOT/'scripts/bootstrap_colab.py').read_text(encoding='utf-8')
definitions=helper.split("\nif __name__ == '__main__':",1)[0].rstrip()+'\n'

def cell(kind,text):
    cell_id='setup-'+hashlib.sha256((kind+'\n'+text).encode('utf-8')).hexdigest()[:16]
    row={'cell_type':kind,'id':cell_id,'metadata':{},'source':text.splitlines(keepends=True)}
    if kind=='code':row.update(execution_count=None,outputs=[])
    return row

notebook={
 'nbformat':4,'nbformat_minor':5,
 'metadata':{'colab':{'name':'START_HERE_COLAB.ipynb'},
             'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
             'language_info':{'name':'python'}},
 'cells':[
  cell('markdown', '''# Set up the exercises in Colab

Repository: https://github.com/long070904/learning-resource-exercises

Download the source ZIP from GitHub using **Code → Download ZIP**, then open this
notebook in a fresh Colab runtime. The repository is public, so no GitHub token
is needed.

1. Run the setup-helper cell below.
2. Run the upload cell and choose the repository ZIP.
3. Run the listing cell to see the available exercises.

Files are unpacked into `/content/HaiLong_Colab_Exercises`, the location used by
the course notebooks. Existing files there are preserved; use a fresh runtime
or a different destination for another source ZIP.

This step prepares the files. Package installation and training happen in the
chosen course notebook. Setup needs Python 3.10 or newer; each exercise lists
its own package and hardware requirements. Basic data exercises can use a CPU,
while longer training work generally needs a GPU.
'''),
  cell('code', '# Safe source-package setup helpers. This cell does not download or run course code.\n'+definitions),
  cell('code', '''# Upload the repository source ZIP.
from google.colab import files
from pathlib import Path

uploaded = files.upload()
zip_names = [name for name in uploaded if name.lower().endswith('.zip')]
if len(uploaded) != 1 or len(zip_names) != 1:
    raise ValueError('Upload one repository ZIP, not datasets or model checkpoints.')
repository = prepare_from_zip(Path(zip_names[0]))
print('Repository ready:', repository)
print('Required helper module files are present; none were imported or executed.')
'''),
  cell('code', '''# List source notebooks only. No training or dependency installation starts here.
exercise_sources = list_exercises(repository)
'''),
  cell('markdown', '''## Run an exercise

Choose a source notebook from the list or `EXERCISE_INDEX.md`, then read its setup
cell and `RUN_ORDER.md`.

Colab notebooks may use separate runtimes. If the chosen exercise cannot find
the course files, copy the **setup-helper and ZIP-upload cells** from this
notebook into that exercise and run them before its existing setup. The files
then live in the runtime that will execute the exercise.

### Public-clone option

After running the setup-helper cell, this is another way to obtain the public
repository. Use it in place of the ZIP-upload cell:

```python
repository = prepare_public_clone()
exercise_sources = list_exercises(repository)
```

### Data and saved work

The teaching-data downloader restores five omitted public Google/MNIST files,
about 117 MB in total. Run it if the chosen exercise needs them:

```python
import subprocess, sys
subprocess.run([sys.executable, str(repository / 'scripts/download_teaching_data.py'), '--all'], check=True)
```

Competition datasets, restricted ImageNet data, service credentials and full
checkpoints are supplied separately. Follow the relevant exercise's instructions,
and save outputs and logs to persistent storage before ending the runtime.

### Local use

List exercises from an existing local checkout:

```text
python scripts/bootstrap_colab.py --list .
```

Or unpack a source ZIP into a new directory:

```text
python scripts/bootstrap_colab.py --zip path/to/download.zip --destination path/to/new-course-folder
```
''')
 ]
}
assert len({row['id'] for row in notebook['cells']})==len(notebook['cells'])
(ROOT/'START_HERE_COLAB.ipynb').write_text(json.dumps(notebook,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print('Wrote START_HERE_COLAB.ipynb with source cells and empty outputs')
