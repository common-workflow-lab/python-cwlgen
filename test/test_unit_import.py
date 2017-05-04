#!/usr/bin/env python

'''
Unit tests for import feature of cwlgen library
'''

#  Import  ------------------------------ 

# General libraries
import os
import filecmp
import unittest

# External libraries
from cwlgen.import_cwl import CWLToolParser

#  Class(es)  ------------------------------ 

class TestImport(unittest.TestCase):

    def setUp(self):
        ctp = CWLToolParser()
        self.tool = ctp.import_cwl('test/import_cwl.cwl')


class TestImportCWL(TestImport):

    def test_load_id(self):
        self.assertEqual(self.tool.tool_id, 'tool_id')

    def test_load_baseCommand(self):
        self.assertEqual(self.tool.base_command, 'share')

    def test_load_label(self):
        self.assertEqual(self.tool.label, 'a_label')

    def test_load_doc(self):
        self.assertEqual(self.tool.doc, 'super_doc')

    def test_load_cwlVersion(self):
        self.assertEqual(self.tool.cwl_version, 'v1.0')

    def test_load_stdin(self):
        self.assertEqual(self.tool.stdin, 'in')

    def test_load_stderr(self):
        self.assertEqual(self.tool.stderr, 'err')

    def test_load_stdout(self):
        self.assertEqual(self.tool.stdout, 'out')
