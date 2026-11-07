"""Meaningful updater regression tests; test-only data never enters profile assets."""
import contextlib
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import update_activity as activity
import visuals

class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        (self.root/'docs').mkdir()
        self.out=self.root/'assets/stats'
        self.patches=[patch.object(activity,'ROOT',self.root),patch.object(activity,'OUT',self.out),patch.object(visuals,'OUT',self.out),patch('sys.argv',['update_activity.py'])]
        for p in self.patches:p.start()
    def tearDown(self):
        for p in reversed(self.patches):p.stop()
        self.temp.cleanup()
    def repo(self,**kwargs):
        return dict({'owner':{'login':'abhisheksureshnair'},'private':False,'fork':False,'language':'Python','stargazers_count':2},**kwargs)
    def run_with(self,repos,events=None):
        with patch.object(activity,'fetch',side_effect=[repos,events or []]),contextlib.redirect_stdout(io.StringIO()):activity.main()
    def files(self):return {str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
    def test_scopes_and_null_languages(self):
        self.run_with([self.repo(),self.repo(fork=True,stargazers_count=99),self.repo(private=True),self.repo(owner={'login':'elsewhere'}),self.repo(language=None)])
        data=json.loads((self.out/'activity.json').read_text())
        self.assertEqual(data['public_repositories'],3)
        self.assertEqual(data['non_fork_repositories'],2)
        self.assertEqual(data['stars_on_non_forks'],4)
        self.assertEqual(data['primary_languages'],{'Python':1})
    def test_unchanged_values_keep_timestamp_and_files(self):
        self.run_with([self.repo()]);before=self.files()
        class Future(datetime):
            @classmethod
            def now(cls,tz=None):return cls(2099,1,1,tzinfo=timezone.utc)
        with patch.object(activity,'datetime',Future):self.run_with([self.repo()])
        self.assertEqual(before,self.files())
    def test_network_failure_preserves_every_output(self):
        self.run_with([self.repo()]);before=self.files()
        with patch.object(activity,'fetch',side_effect=[[self.repo()],OSError('unavailable')]):
            with self.assertRaises(OSError):activity.main()
        self.assertEqual(before,self.files())
    def test_pagination_and_empty_languages(self):
        with patch.object(activity,'fetch',side_effect=[[self.repo(language=None)]*100,[self.repo(language=None)],[]]) as fetch:
            activity.main()
            self.assertEqual(fetch.call_count,3)
        data=json.loads((self.out/'activity.json').read_text())
        self.assertEqual(data['public_repositories'],101)
        self.assertEqual(data['primary_languages'],{})
    def test_public_events_only(self):
        self.run_with([self.repo()],[{'public':False,'created_at':'2099-01-01T00:00:00Z'},{'public':True,'created_at':'2026-01-01T00:00:00Z'}])
        self.assertEqual(json.loads((self.out/'activity.json').read_text())['latest_returned_public_event'],'2026-01-01T00:00:00Z')
if __name__=='__main__':unittest.main()
