#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.5.2+
## Creation : 01-02-2017

'''
Descrition
'''

###########  Import  ###########

# General libraries
import os
import filecmp
import unittest

# External libraries

# Class and Objects
import pycwl

###########  Constant(s)  ###########

# Declare one ontology for all the test
EDAM = {'uri':'http://edamontology.org/topic_0091',
        'term':'bioinformatics'}

###########  Function(s)  ###########

###########  Class(es)  ###########

class TestCwl(unittest.TestCase):

    def setUp(self):
        self.cwl = pycwl.Cwl('an_id', 'a_class', 'a description '+\
                             'with spaces.', 'a_command')

    def test_init(self):
        self.assertEqual(self.cwl.tool_id, 'an_id')
        self.assertEqual(self.cwl.tool_class, 'a_class')
        self.assertEqual(self.cwl.label, 'a description with spaces.')
        self.assertEqual(self.cwl.base_command, 'a_command')
        self.assertListEqual(self.cwl.inputs, [])
        self.assertListEqual(self.cwl.outputs, [])
        self.assertIsNone(self.cwl.documentation)


###########  Main  ###########

if __name__ == "__main__":
    unittest.main()
