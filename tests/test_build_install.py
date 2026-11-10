# Copyright (C) 2026 Maxim Lyadvinsky
# SPDX-License-Identifier: GPL-3.0-or-later
"""Test the actual prebuilt artifact, deterministic build and install lifecycle."""
from pathlib import Path
import base64
import gzip
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/'nic-doctor.sh'
MARKER = b'\n__NIC_DOCTOR_EMBEDDED_PAYLOAD__\n'


class PackagingTests(unittest.TestCase):
    def test_single_file_cli_no_install(self):
        for args, needle in (([], 'usage: nic-doctor'),
                             (['--help'], 'usage: nic-doctor'),
                             (['help','topology'], '--view'),
                             (['--version'], '1.1.1'),
                             (['topology'], 'HARDWARE TREE')):
            p=subprocess.run([str(SCRIPT), *args],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertIn(needle,p.stdout)

    def test_copyright_attribution(self):
        version=subprocess.run([str(SCRIPT),'--version'],capture_output=True,text=True)
        self.assertEqual(version.returncode,0,version.stderr)
        self.assertIn('Copyright (C) 2026 Maxim Lyadvinsky',version.stdout)
        self.assertIn('License: GPL-3.0-or-later',version.stdout)
        self.assertIn('Copyright (C) 2026 Maxim Lyadvinsky',SCRIPT.read_text().split('set -eu',1)[0])
        self.assertIn('GNU GENERAL PUBLIC LICENSE',(ROOT/'LICENSE').read_text())
        self.assertIn('Version 3, 29 June 2007',(ROOT/'LICENSE').read_text())
        self.assertIn('END OF TERMS AND CONDITIONS',SCRIPT.read_text())
        self.assertIn('SPDX-License-Identifier: GPL-3.0-or-later',SCRIPT.read_text().split('set -eu',1)[0])
        for name in ('common.py','discovery.py','topology.py','tuning.py','analysis.py','cli.py'):
            self.assertIn('Copyright (C) 2026 Maxim Lyadvinsky','\n'.join((ROOT/'src'/name).read_text().splitlines()[:8]))

    def test_build_reproducible_and_sources_match_embedded(self):
        before=SCRIPT.read_bytes()
        self.assertEqual(before.count(MARKER),1)
        encoded=b''.join(before.split(MARKER)[1].split())
        actual=gzip.decompress(base64.b64decode(encoded,validate=True))
        names=['common.py','discovery.py','topology.py','tuning.py','analysis.py','cli.py']
        expected=b'\n'.join((ROOT/'src'/f).read_bytes().rstrip(b'\n')+b'\n' for f in names)
        self.assertEqual(actual,expected)
        self.assertEqual(subprocess.run([str(ROOT/'build.sh')],capture_output=True,text=True).returncode,0)
        self.assertEqual(SCRIPT.read_bytes(),before,'build is not deterministic')

    @unittest.skipUnless(os.geteuid()==0, 'install/remove test requires root')
    def test_install_upgrade_remove_one_file(self):
        with tempfile.TemporaryDirectory() as directory:
            prefix=Path(directory)
            cmd=[str(SCRIPT),'install','--prefix',str(prefix)]
            install=subprocess.run(cmd,text=True,capture_output=True)
            self.assertEqual(install.returncode,0,install.stderr)
            exe=prefix/'bin/nic-doctor'
            self.assertTrue(exe.exists())
            self.assertEqual(exe.read_bytes(),SCRIPT.read_bytes())
            with subprocess.Popen([str(exe),'--version'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) as proc:
                stdout,stderr=proc.communicate(timeout=10)
                self.assertEqual(proc.returncode,0,stderr)
                self.assertIn('1.1.1',stdout)
            install2=subprocess.run(cmd,text=True,capture_output=True)
            self.assertEqual(install2.returncode,0,install2.stderr)
            remove=subprocess.run([str(exe),'remove'],text=True,capture_output=True)
            self.assertEqual(remove.returncode,0,remove.stderr)
            self.assertFalse(exe.exists())
            self.assertFalse((prefix/'lib/nic-doctor/install.json').exists())
            self.assertTrue(SCRIPT.exists())

    @unittest.skipUnless(os.geteuid()==0, 'upgrade test requires root')
    def test_legacy_manifest_upgrade_in_place(self):
        with tempfile.TemporaryDirectory() as directory:
            prefix = Path(directory)
            exe = prefix/'bin/nic-doctor'
            manifest = prefix/'lib/nic-doctor/install.json'
            exe.parent.mkdir(parents=True)
            manifest.parent.mkdir(parents=True)
            old = b'#!/usr/bin/env python3\n# NIC_DOCTOR_RELEASE v1.0.3\nprint("legacy")\n'
            exe.write_bytes(old)
            exe.chmod(0o755)
            manifest.write_text(json.dumps({
                'marker':'NIC_DOCTOR_RELEASE', 'version':'1.0.3',
                'binary':str(exe), 'sha256':hashlib.sha256(old).hexdigest()
            }))
            result=subprocess.run([str(SCRIPT),'install','--prefix',str(prefix)],text=True,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(exe.read_bytes(),SCRIPT.read_bytes())
            version=subprocess.run([str(exe),'--version'],text=True,capture_output=True)
            self.assertEqual(version.returncode,0,version.stderr)
            self.assertIn('1.1.1',version.stdout)
            removed=subprocess.run([str(exe),'remove'],text=True,capture_output=True)
            self.assertEqual(removed.returncode,0,removed.stderr)

    @unittest.skipUnless(os.geteuid()==0, 'root required to verify refusal')
    def test_does_not_overwrite_unrelated_nic_doctor(self):
        with tempfile.TemporaryDirectory() as directory:
            prefix=Path(directory)
            exe=prefix/'bin/nic-doctor'
            exe.parent.mkdir()
            exe.write_text('unrelated')
            result=subprocess.run([str(SCRIPT),'install','--prefix',str(prefix)],text=True,capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(exe.read_text(),'unrelated')


if __name__=='__main__':
    unittest.main()
