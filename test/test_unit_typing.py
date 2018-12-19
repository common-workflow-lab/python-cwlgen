import unittest
from cwlgen.elements import parse_param_type, NON_NULL_CWL_TYPE, CWL_TYPE, DEF_TYPE
import logging


class TestParamTyping(unittest.TestCase):

    def test_types(self):
        for cwl_type in NON_NULL_CWL_TYPE:
            self.assertEqual(parse_param_type(cwl_type), cwl_type)

    def test_incorrect_type(self):
        for cwl_type in NON_NULL_CWL_TYPE:
            should_be_def_type = parse_param_type(cwl_type.upper())
            self.assertNotEqual(should_be_def_type, cwl_type)
            self.assertEqual(should_be_def_type, DEF_TYPE)

    def test_optional_string(self):
        for cwl_type in NON_NULL_CWL_TYPE:
            optional_type = cwl_type + "?"
            self.assertEqual(parse_param_type(optional_type), optional_type)
