#!/usr/bin/env python

'''
Unit tests for import feature of cwlgen library
'''

#  Import  ------------------------------

import unittest
# General libraries
from os import path

import ruamel.yaml as ryaml

# External libraries
from cwlgen.import_cwl import parse_cwl_dict

#  Class(es)  ------------------------------

# Use this to ensure location to import_workflow is correct when directly running the file.
test_dir = path.dirname(path.abspath(__file__))


class TestImport(unittest.TestCase):

    # def setUp(self):
    #     ctp = CWLToolParser()
    #     self.wf = ctp.import_cwl(test_dir + '/import_cwl.cwl')

    @classmethod
    def setUpClass(cls):
        cls.path = test_dir + '/import_workflow.cwl'
        with open(cls.path) as mf:
            cls.wf_dict = ryaml.load(mf, Loader=ryaml.Loader)
        cls.wf = parse_cwl_dict(cls.wf_dict)


class TestImportCWL(TestImport):

    # def test_export_loaded(self):
        # self.maxDiff = None
        # print(self.wf_dict)
        # print(self.wf.get_dict())
        # self.assertDictEqual(self.wf_dict, self.wf.get_dict())

    def test_load_id(self):
        self.assertEqual(self.wf.id, '1stWorkflow')

    def test_load_class(self):
        self.assertEqual(self.wf.cwlVersion, 'v1.0')

    def test_load_doc(self):
        self.assertEqual(self.wf.doc, 'This is a documentation string')


class TestInputsParser(TestImport):

    def test_init_input(self):
        self.assertEqual(self.wf.inputs[0].id, 'tarball')

    def test_load_label(self):
        self.assertEqual(self.wf.inputs[0].label, 'label_in')

    def test_load_secondaryFiles(self):
        self.assertEqual(self.wf.inputs[0].secondaryFiles, 'sec_file_in')

    def test_load_format(self):
        self.assertEqual(self.wf.inputs[0].format, 'format_1930')

    def test_load_streamable(self):
        self.assertTrue(self.wf.inputs[0].streamable)

    def test_load_doc(self):
        self.assertEqual(self.wf.inputs[0].doc, 'documentation_in')

    def test_load_default(self):
        self.assertEqual(self.wf.inputs[0].default, 'def_in')

    def test_load_type(self):
        self.assertEqual(self.wf.inputs[0].type, 'File')


class TestOutputsParser(TestImport):

    def test_init_input(self):
        self.assertEqual(self.wf.outputs[0].id, 'compiled_class')

    def test_load_label(self):
        self.assertEqual(self.wf.outputs[0].outputSource, 'compile/classfile')

    def test_load_secondaryFiles(self):
        self.assertEqual(self.wf.outputs[0].type, 'File')


class TestStepParser(TestImport):

    def test_load_id(self):
        self.assertEqual(self.wf.steps[0].id, 'compile')

    def test_load_out(self):
        self.assertListEqual(self.wf.steps[0].out, ['classfile'])


class TestStepInputParser(TestImport):

    def test_load_id(self):
        self.assertEqual(self.wf.steps[0].inputs[0].id, "src")

    def test_load_source(self):
        self.assertEqual(self.wf.steps[0].inputs[0].source, "untar/extracted_file")

