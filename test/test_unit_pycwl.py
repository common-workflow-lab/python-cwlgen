#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.6.0
## Creation : 01-02-2017

'''
Unit tests for pycwl library
'''

###########  Import  ###########

# General libraries
import os
import filecmp
import unittest

# External libraries
import pycwl

# Class and Objects

###########  Constant(s)  ###########

###########  Function(s)  ###########

###########  Class(es)  ###########

class TestCommandLineTool(unittest.TestCase):

    def setUp(self):
        self.cwl = pycwl.CommandLineTool('an_id', 'a description '+\
                                         'with spaces.', 'a_command')

    def test_init(self):
        self.assertEqual(self.cwl.tool_id, 'an_id')
        self.assertEqual(self.cwl.label, 'a description with spaces.')
        self.assertEqual(self.cwl.base_command, 'a_command')
        self.assertListEqual(self.cwl.inputs, [])
        self.assertListEqual(self.cwl.outputs, [])
        self.assertIsNone(self.cwl.doc)

    def test_export(self):
        tmp_file = 'test_export.tmp'
        expected_file = os.path.dirname(__file__) + '/test_export.cwl'
        self.cwl.export(tmp_file)
        try:
            self.assertTrue(filecmp.cmp(expected_file, tmp_file))
        finally:
            os.remove(tmp_file)

    def test_full_export(self):
        tmp_file = 'test_full_export.tmp'
        expected_file = os.path.dirname(__file__) + '/test_full_export.cwl'
        self.cwl.doc = "documentation"
        an_input = pycwl.Input('an_in_id', 'an_in_type')
        self.cwl.inputs.append(an_input)
        an_output = pycwl.Output('an_out_id', 'an_out_type')
        self.cwl.outputs.append(an_output)
        self.cwl.export(tmp_file)
        try:
            self.assertTrue(filecmp.cmp(expected_file, tmp_file))
        finally:
            os.remove(tmp_file)


class TestParameter(unittest.TestCase):

    def setUp(self):
        self.param = pycwl.Parameter('an_id', 'File', label='a_label',\
                                     doc='a_doc', param_format='a_format',\
                                     streamable=True, secondary_files='sec_files')

    def test_init(self):
        self.assertEqual(self.param.id, 'an_id')
        self.assertEqual(self.param.type, 'File')
        self.assertEqual(self.param.doc, 'a_doc')
        self.assertEqual(self.param.format, 'a_format')
        self.assertEqual(self.param.label, 'a_label')
        self.assertEqual(self.param.secondary_files, 'sec_files')
        self.assertTrue(self.param.streamable)

    def test_getdict_cwl(self):
        dict_test = self.param.getdict_cwl()
        self.assertEqual(dict_test['type'], 'File')
        self.assertEqual(dict_test['doc'], 'a_doc')
        self.assertEqual(dict_test['format'], 'a_format')
        self.assertEqual(dict_test['label'], 'a_label')
        self.assertEqual(dict_test['secondaryFiles'], 'sec_files')
        self.assertTrue(dict_test['streamable'])


class TestInput(unittest.TestCase):

    def setUp(self):
        self.frst_inp = pycwl.Input('frst_id', 'File', position=1)
        self.scnd_inp = pycwl.Input('scnd_id', 'File', prefix='--prefix')

    def test_init(self):
        # Test first input
        self.assertEqual(self.frst_inp.id, 'frst_id')
        self.assertEqual(self.frst_inp.type, 'File')
        self.assertEqual(self.frst_inp.position, 1)
        # Test second input
        self.assertEqual(self.scnd_inp.id, 'scnd_id')
        self.assertEqual(self.scnd_inp.type, 'File')
        self.assertEqual(self.scnd_inp.prefix, '--prefix')

    def test_getdict_cwl(self):
        # Test first input
        dict_frst = self.frst_inp.getdict_cwl()
        self.assertEqual(dict_frst['type'], 'File')
        self.assertEqual(dict_frst['inputBinding']['position'], 1)
        # Test second input
        dict_scnd = self.scnd_inp.getdict_cwl()
        self.assertEqual(dict_scnd['type'], 'File')
        self.assertEqual(dict_scnd['inputBinding']['prefix'], '--prefix')


class TestOutput(unittest.TestCase):

    def setUp(self):
        self.outp = pycwl.Output('an_out_id', 'File', glob='file.ext')

    def test_init(self):
        self.assertEqual(self.outp.id, 'an_out_id')
        self.assertEqual(self.outp.type, 'File')
        self.assertEqual(self.outp.glob, 'file.ext')

    def test_getdict_cwl(self):
        dict_test = self.outp.getdict_cwl()
        self.assertEqual(dict_test['type'], 'File')
        self.assertEqual(dict_test['outputBinding']['glob'], 'file.ext')


###########  Main  ###########

if __name__ == "__main__":
    unittest.main()
