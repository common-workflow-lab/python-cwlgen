import unittest
from cwlgen.elements import parse_param_type, NON_NULL_CWL_TYPE, CWL_TYPE, DEF_TYPE, CommandInputArraySchema
import logging


class TestParamTyping(unittest.TestCase):

    def test_types(self):
        for cwl_type in NON_NULL_CWL_TYPE:
            self.assertEqual(parse_param_type(cwl_type), cwl_type)

    def test_incorrect_type(self):
        invalid_type = "invalid"
        should_be_def_type = parse_param_type(invalid_type)
        self.assertNotEqual(should_be_def_type, invalid_type)
        self.assertEqual(should_be_def_type, DEF_TYPE)

    def test_optional_string(self):
        for cwl_type in NON_NULL_CWL_TYPE:
            optional_type = cwl_type + "?"
            self.assertEqual(parse_param_type(optional_type), optional_type)

    def test_typed_array(self):
        array_string_type = "string[]"
        q = parse_param_type(array_string_type)
        self.assertIsInstance(q, CommandInputArraySchema)
        self.assertEqual(q.items, "string")

    def test_incorrectly_typed_array(self):
        array_string_type = "invalid[]"
        q = parse_param_type(array_string_type)
        self.assertIsInstance(q, CommandInputArraySchema)
        self.assertNotEqual(q.items, "invalid")
        self.assertEqual(q.items, DEF_TYPE)

    def test_optionally_typed_array(self):
        array_string_type = "string?[]"
        q = parse_param_type(array_string_type)
        self.assertIsInstance(q, CommandInputArraySchema)
        self.assertEqual(q.items, "string?")

    def test_optional_typed_array(self):
        optional_array_string_type = "string[]?"
        q = parse_param_type(optional_array_string_type)
        self.assertIsInstance(q, list)
        self.assertEqual(len(q), 2)
        null_idx = q.index(DEF_TYPE)
        array_type = q[1 - null_idx]
        self.assertIsInstance(array_type, CommandInputArraySchema)
        self.assertEqual(array_type.items, "string")

    def test_command_input_array_schema(self):
        ar = CommandInputArraySchema(items="string")
        self.assertIsInstance(ar, CommandInputArraySchema)
        self.assertEqual(parse_param_type(ar), ar)
        self.assertEqual(ar.items, "string")

    def test_optional_type_input_array_schema(self):
        ar = CommandInputArraySchema(items="string?")
        self.assertIsInstance(ar, CommandInputArraySchema)
        self.assertEqual(parse_param_type(ar), ar)
        self.assertEqual(ar.items, "string?")
