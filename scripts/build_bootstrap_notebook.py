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
  cell('markdown', '''# Set up the learning resources in Colab

Repository: https://github.com/long070904/learning-resource-exercises

This setup notebook unpacks the source repository and lists its exercises. It does **not** install every course environment, start training, or establish that an exercise is complete.

## Private repository: use a downloaded ZIP

1. While signed in to GitHub, open the repository and choose **Code → Download ZIP**.
2. Open this `START_HERE_COLAB.ipynb` in Colab. Use a fresh runtime.
3. Run the next three code cells. When the upload picker opens, choose that one repository ZIP.

No GitHub token, password, Google Drive mount, or fixed historical ZIP hash is needed. Files are extracted into `/content/HaiLong_Colab_Exercises`. Existing work at that destination is preserved; another ZIP requires a fresh runtime or another destination.

The bootstrap requires Python 3.10 or newer. Course notebooks have their own package and hardware requirements. A T4 GPU is useful for GPU exercises; basic data exercises can use a CPU runtime.
'''),
  cell('code', '# Safe source-package setup helpers. This cell does not download or run course code.\n'+definitions),
  cell('code', '''# Upload exactly the repository ZIP downloaded while signed in to GitHub.
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
  cell('markdown', '''## Open and run an exercise

Use the paths listed above and `EXERCISE_INDEX.md` to select an exercise. Read `RUN_ORDER.md` and its own setup cell before running it.

Colab notebooks can have separate runtimes. Setting up this notebook does not guarantee that another notebook has these files. In the exercise notebook, insert and run the **setup-helper cell and ZIP-upload cell above** before its existing setup cell. That creates `/content/HaiLong_Colab_Exercises` in the runtime that will execute the exercise. Then follow the exercise's own cells and package profile.

The teaching-data downloader restores the five omitted public CSV/MNIST inputs, about 117 MB in total. Run it only if the selected exercise needs those files:

```python
import subprocess, sys
subprocess.run([sys.executable, str(repository / 'scripts/download_teaching_data.py'), '--all'], check=True)
```

Competition datasets, restricted ImageNet data, service credentials and full model checkpoints are not in this source ZIP. Follow the relevant exercise instructions and progress records for those requirements. Save outputs and logs to your own persistent storage before a temporary Colab runtime ends.

## Optional route if the repository is made public

After running the setup-helper cell, you can use the following **instead of** the ZIP-upload cell, only when the repository is publicly readable:

```python
repository = prepare_public_clone()
exercise_sources = list_exercises(repository)
```

An unauthenticated clone does not provide access to a private repository. The signed-in GitHub ZIP route above works without placing credentials in notebook code.

## Local use

From an existing local source checkout, list exercises without extracting anything:

```text
python scripts/bootstrap_colab.py --list .
```

Or unpack a downloaded repository ZIP into a new local directory:

```text
python scripts/bootstrap_colab.py --zip path/to/download.zip --destination path/to/new-course-folder
```
''')
 ]
}
assert len({row['id'] for row in notebook['cells']})==len(notebook['cells'])
(ROOT/'START_HERE_COLAB.ipynb').write_text(json.dumps(notebook,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print('Wrote START_HERE_COLAB.ipynb with source cells and empty outputs')
