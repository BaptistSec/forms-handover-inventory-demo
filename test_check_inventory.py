import contextlib
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from check_inventory import check, main, HEADERS, REQUIRED

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'inventory.csv'
        self.rows=[dict(zip(HEADERS,[c,'REF','owner','target','confirmed','EVIDENCE'])) for c in sorted(REQUIRED)]
    def tearDown(self):self.tmp.cleanup()
    def write(self):
        with self.path.open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,HEADERS);w.writeheader();w.writerows(self.rows)
        return self.path
    def test_complete_not_platform_verified(self):
        r=check(self.write());self.assertEqual(r['record_check'],'complete_on_paper');self.assertFalse(r['platform_verified'])
    def test_missing_component(self):
        self.rows.pop();self.assertTrue(check(self.write())['issues'])
    def test_pending(self):
        self.rows[0]['status']='pending';self.assertTrue(check(self.write())['issues'])
    def test_blocked(self):
        self.rows[0]['status']='blocked';self.assertTrue(check(self.write())['issues'])
    def test_confirmed_no_evidence(self):
        self.rows[0]['evidence']='';self.assertTrue(check(self.write())['issues'])
    def test_no_owner(self):
        self.rows[0]['target_owner']='';self.assertTrue(check(self.write())['issues'])
    def test_not_used_reason(self):
        self.rows[0]['status']='not_used';self.rows[0]['evidence']='';self.assertTrue(check(self.write())['issues'])
    def test_form_required(self):
        next(x for x in self.rows if x['component']=='form')['status']='not_used';self.assertTrue(check(self.write())['issues'])
    def test_duplicate(self):
        self.rows.append(self.rows[0]);self.write()
        with self.assertRaises(ValueError):check(self.path)
    def test_unknown(self):
        self.rows[0]['component']='mystery';self.write()
        with self.assertRaises(ValueError):check(self.path)
    def test_invalid_status(self):
        self.rows[0]['status']='done';self.write()
        with self.assertRaises(ValueError):check(self.path)
    def test_headers(self):
        self.path.write_text('component,status\nform,confirmed\n')
        with self.assertRaises(ValueError):check(self.path)
    def test_unchanged(self):
        self.write();before=self.path.read_bytes();check(self.path);self.assertEqual(before,self.path.read_bytes())
    def test_cli_status(self):
        self.write()
        with contextlib.redirect_stdout(io.StringIO()) as o:self.assertEqual(main([str(self.path)]),0)
        self.assertFalse(json.loads(o.getvalue())['platform_verified'])
        self.rows[0]['status']='pending';self.write()
        with contextlib.redirect_stdout(io.StringIO()):self.assertEqual(main([str(self.path)]),1)
        self.path.write_text('wrong\n')
        with contextlib.redirect_stderr(io.StringIO()):self.assertEqual(main([str(self.path)]),2)
if __name__=='__main__':unittest.main()
