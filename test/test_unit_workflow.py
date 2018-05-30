#!/usr/bin/env python

'''
Unit tests for cwlgen library
'''

#  Import  ------------------------------

# General libraries
import os
import filecmp
import unittest

# External libraries
import cwlgen

#  Class(es)  ------------------------------

class TestCommandLineTool(unittest.TestCase):


    def test_build(self):

        w = cwlgen.Workflow()
        tool = cwlgen.parse_cwl("test/import_cwl.cwl")

        f = cwlgen.File("input_file")

        o1 = w.add('step-a', tool, {"INPUT1" : f})
        o2 = w.add('step-b', tool, {"INPUT1" : o1['OUTPUT1']})
        o2['OUTPUT1'].store()
        w.export("test.cwl")
