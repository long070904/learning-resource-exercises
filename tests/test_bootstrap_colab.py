"""Bounded fixtures for source ZIP safety; never run course/model code."""
import hashlib
import importlib.util
import json
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE if (HERE/'scripts/bootstrap_colab.py').is_file() else HERE.parent
SPEC=importlib.util.spec_from_file_location('owned_bootstrap',ROOT/'scripts/bootstrap_colab.py')
bootstrap=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bootstrap)


class BootstrapSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='learning-bootstrap-fixture-')
        self.root=Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def fixture(self,name='source.zip',wrapper='repo-main/',extra=()):
        path=self.root/name
        with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as archive:
            for module in bootstrap.REQUIRED_HELPERS:
                archive.writestr(wrapper+module,"raise RuntimeError('Downloaded code must not execute during setup')\n")
            archive.writestr(wrapper+'exercise_manifest.json',json.dumps([{'path':'01_google_mlcc/example.ipynb','gpu':False}]))
            archive.writestr(wrapper+'01_google_mlcc/example.ipynb',json.dumps({'nbformat':4,'cells':[]}))
            archive.writestr(wrapper+'README.md','Fixture source repository')
            for item,data in extra:
                if isinstance(item,zipfile.ZipInfo):archive.writestr(item,data)
                else:archive.writestr(wrapper+item,data)
        return path

    def test_wrapped_source_extracts_and_records_provenance_without_import(self):
        archive=self.fixture()
        destination=self.root/'course'
        result=bootstrap.prepare_from_zip(archive,destination)
        self.assertEqual(result,destination.resolve())
        self.assertTrue((destination/'colab_runtime.py').is_file())
        self.assertFalse((destination/'repo-main').exists())
        receipt=json.loads((destination/bootstrap.RECEIPT_NAME).read_text())
        self.assertEqual(receipt['archive_sha256'],hashlib.sha256(archive.read_bytes()).hexdigest())
        self.assertFalse(receipt['course_code_executed'])
        self.assertFalse(receipt['credentials_used'])

    def test_unwrapped_source_is_supported(self):
        archive=self.fixture(wrapper='')
        bootstrap.prepare_from_zip(archive,self.root/'course')
        self.assertTrue((self.root/'course/01_google_mlcc/example.ipynb').is_file())

    def test_repeat_same_zip_preserves_user_results(self):
        archive=self.fixture()
        destination=bootstrap.prepare_from_zip(archive,self.root/'course')
        marker=destination/'my_results.txt'
        marker.write_text('keep my result')
        bootstrap.prepare_from_zip(archive,destination)
        self.assertEqual(marker.read_text(),'keep my result')

    def test_existing_destination_is_never_overwritten(self):
        archive=self.fixture()
        destination=self.root/'course'
        destination.mkdir()
        marker=destination/'my_results.txt'
        marker.write_text('preserved')
        with self.assertRaises(FileExistsError):bootstrap.prepare_from_zip(archive,destination)
        self.assertEqual(marker.read_text(),'preserved')

    def test_traversal_absolute_windows_and_alias_paths_rejected(self):
        for index,bad in enumerate(('../escape.txt','nested/../../escape.txt','/escape.txt','C:/escape.txt',r'..\escape.txt','AUX.txt','folder./item.txt')):
            with self.subTest(path=bad):
                archive=self.fixture(name=f'bad{index}.zip',wrapper='',extra=[(bad,'unsafe')])
                destination=self.root/f'course{index}'
                with self.assertRaises(ValueError):bootstrap.prepare_from_zip(archive,destination)
                self.assertFalse(destination.exists())
        self.assertFalse((self.root/'escape.txt').exists())

    def test_symlink_and_special_members_rejected(self):
        for index,mode in enumerate((stat.S_IFLNK|0o777,stat.S_IFIFO|0o600)):
            item=zipfile.ZipInfo('repo-main/unsafe-link')
            item.create_system=3
            item.external_attr=mode<<16
            archive=self.fixture(name=f'special{index}.zip',extra=[(item,'../../outside')])
            with self.assertRaises(ValueError):bootstrap.prepare_from_zip(archive,self.root/f'course{index}')

    def test_case_and_file_directory_collisions_rejected(self):
        variants=[[('A.txt','a'),('a.txt','b')],[('folder','file'),('folder/child.txt','child')]]
        for index,extra in enumerate(variants):
            archive=self.fixture(name=f'collision{index}.zip',extra=extra)
            with self.assertRaises(ValueError):bootstrap.prepare_from_zip(archive,self.root/f'course{index}')

    def test_outside_wrapper_payload_rejected(self):
        archive=self.fixture()
        with zipfile.ZipFile(archive,'a') as package:package.writestr('outside.txt','outside repository')
        with self.assertRaises(ValueError):bootstrap.prepare_from_zip(archive,self.root/'course')

    def test_size_and_member_limits_enforced_before_destination_write(self):
        archive=self.fixture()
        limits=(('MAX_TOTAL_BYTES',1),('MAX_MEMBER_BYTES',1),('MAX_FILES',1))
        for name,limit in limits:
            previous=getattr(bootstrap,name)
            try:
                setattr(bootstrap,name,limit)
                with self.assertRaises(ValueError):bootstrap.prepare_from_zip(archive,self.root/'course')
                self.assertFalse((self.root/'course').exists())
            finally:setattr(bootstrap,name,previous)

    def test_notebook_json_source_matches_helper_and_has_no_saved_outputs(self):
        notebook=json.loads((ROOT/'START_HERE_COLAB.ipynb').read_text(encoding='utf-8'))
        self.assertEqual(notebook['nbformat'],4)
        helper=(ROOT/'scripts/bootstrap_colab.py').read_text(encoding='utf-8').split("\nif __name__ == '__main__':",1)[0].rstrip()+'\n'
        setup=''.join(notebook['cells'][1]['source'])
        self.assertEqual(setup.split('\n',1)[1],helper)
        for index,cell in enumerate(notebook['cells']):
            if cell['cell_type']=='code':
                compile(''.join(cell['source']),f'notebook-cell-{index}','exec')
                self.assertIsNone(cell['execution_count'])
                self.assertEqual(cell['outputs'],[])


if __name__=='__main__':unittest.main(verbosity=2)
