#!/usr/bin/env python

'''
Unit tests for cwlgen library
'''

#  Import  ------------------------------

# General libraries
import os
import filecmp
import unittest
from tempfile import NamedTemporaryFile

# External libraries
import cwlgen

#  Class(es)  ------------------------------

class TWorkflow:
# class TestWorkflow(unittest.TestCase):

    def capture_tempfile(self, func):
        with NamedTemporaryFile() as f:
            func(f.name)
            return f.read()

    def test_generates_workflow_two_steps(self):

        w = cwlgen.Workflow("test_generates_workflow_two_steps")
        tool = cwlgen.parse_cwl("test/import_cwl.cwl")

        f = cwlgen.File("input_file")

        o1 = w.add('step-a', tool, {"INPUT1" : f})
        o2 = w.add('step-b', tool, {"INPUT1" : o1['OUTPUT1']})
        o2['OUTPUT1'].store()
        generated = self.capture_tempfile(w.export)
        expected = b"""#!/usr/bin/env cwl-runner

class: Workflow
cwlVersion: v1.0
inputs:
  INPUT1: {id: INPUT1, type: File}
outputs:
  step-b_OUTPUT1: {id: step-b_OUTPUT1, outputSource: step-b/OUTPUT1, type: File}
steps:
  step-a:
    id: step-a
    in: {INPUT1: INPUT1}
    out: [OUTPUT1]
    run: test/import_cwl.cwl
  step-b:
    id: step-b
    in: {INPUT1: step-a/OUTPUT1}
    out: [OUTPUT1]
    run: test/import_cwl.cwl
"""
        self.assertEqual(expected, generated)

    def test_generates_workflow_int_inputs(self):

        w = cwlgen.Workflow("test_generates_workflow_int_inputs")
        tool = cwlgen.parse_cwl("test/int_tool.cwl")

        i = cwlgen.workflow.InputParameter('INTEGER', param_type='int')
        o1 = w.add('step', tool, {"INTEGER": i})
        o1['OUTPUT1'].store()

        expected = b"""#!/usr/bin/env cwl-runner

class: Workflow
cwlVersion: v1.0
inputs:
  INTEGER: {id: INTEGER, type: int}
outputs:
  step_OUTPUT1: {id: step_OUTPUT1, outputSource: step/OUTPUT1, type: File}
steps:
  step:
    id: step
    in: {INTEGER: INTEGER}
    out: [OUTPUT1]
    run: test/int_tool.cwl
"""
        generated = self.capture_tempfile(w.export)
        self.assertEqual(expected, generated)

    def test_add_requirements(self):
        w = cwlgen.Workflow("test_add_requirements")
        req = cwlgen.InlineJavascriptReq()
        w.requirements.append(req)
        generated = self.capture_tempfile(w.export)
        expected = b"""#!/usr/bin/env cwl-runner

class: Workflow
cwlVersion: v1.0
inputs: {}
outputs: {}
requirements:
  InlineJavascriptRequirement: {}
"""
        self.assertEqual(expected, generated)

