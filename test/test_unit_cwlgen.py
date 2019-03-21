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

    def setUp(self):
        self.cwl = cwlgen.CommandLineTool(tool_id='an_id', label='a description ' + \
                                                                 'with spaces.', base_command='a_command')

        self.array_basecommand = cwlgen.CommandLineTool(tool_id="base-command-array", base_command=["base", "command"])

    def test_init(self):
        self.assertEqual(self.cwl.id, 'an_id')
        self.assertEqual(self.cwl.label, 'a description with spaces.')
        self.assertEqual(self.cwl.baseCommand, 'a_command')
        self.assertListEqual(self.cwl.inputs, [])
        self.assertListEqual(self.cwl.outputs, [])
        self.assertIsNone(self.cwl.doc)

    def test_array_basecommand(self):
        dict_test = self.array_basecommand.get_dict()
        self.assertIn('baseCommand', dict_test)

    def test_codes(self):
        code_tool = cwlgen.CommandLineTool()
        code_tool.permanentFailCodes.extend([400, 401, 500])
        code_tool.temporaryFailCodes.append(408)
        code_tool.successCodes = []  # empty (falsy)

        dict_test = code_tool.get_dict()
        self.assertIn('permanentFailCodes', dict_test)
        self.assertEqual(len(dict_test['permanentFailCodes']), 3)
        self.assertIn('temporaryFailCodes', dict_test)
        self.assertEqual(len(dict_test['temporaryFailCodes']), 1)
        self.assertNotIn('successCodes', dict_test)

    """
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
        an_input = cwlgen.CommandInputParameter('an_in_id', param_type='File')
        self.cwl.inputs.append(an_input)
        an_output = cwlgen.CommandOutputParameter('an_out_id', param_type='File')
        self.cwl.outputs.append(an_output)
        self.cwl.export(tmp_file)
        try:
            self.assertTrue(filecmp.cmp(expected_file, tmp_file))
        finally:
            os.remove(tmp_file)
    """


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        self.workflow = cwlgen.Workflow("test-workflow", label="testing-workflow", doc="A method for testing "
                                                                                       "the features of a workflow.")
        self.workflow.inputs.append(cwlgen.InputParameter("inputParam1", "input-parameter"))
        self.workflow.steps.append(cwlgen.WorkflowStep("step1", run="mytool.cwl"))
        self.workflow.outputs.append(cwlgen.WorkflowOutputParameter("outputFile", output_source="step/output"))

    def test_init(self):
        self.assertEqual(self.workflow.id, "test-workflow")
        self.assertEqual(self.workflow.label, "testing-workflow")
        self.assertEqual(self.workflow.doc, "A method for testing the features of a workflow.")

    def test_added_inputs(self):
        self.assertEqual(len(self.workflow.inputs), 1)
        self.assertEqual(self.workflow.inputs[0].id, "inputParam1")

    def test_added_outputs(self):
        self.assertEqual(len(self.workflow.outputs), 1)
        self.assertEqual(self.workflow.outputs[0].id, "outputFile")

    def test_added_steps(self):
        self.assertEqual(len(self.workflow.steps), 1)
        step = self.workflow.steps[0]
        self.assertEqual(step.id, "step1")
        self.assertEqual(step.run, "mytool.cwl")

    def test_serialization(self):
        d = self.workflow.get_dict()
        self.assertIsInstance(d, dict)


class TestWorkflowStepInput(unittest.TestCase):
    def test_optional_source(self):
        wsi = cwlgen.WorkflowStepInput("test", None).get_dict()
        self.assertNotIn("source", wsi)

    def test_required_source(self):
        source = "step_id/source"
        wsi = cwlgen.WorkflowStepInput("required-input", source=source).get_dict()
        self.assertIn("source", wsi)
        self.assertEqual(wsi["source"], source)


class TestSubworkflow(unittest.TestCase):
    def setUp(self):
        self.subworkflow = cwlgen.Workflow("subworkflow", doc="This is the subworkflow")
        self.workflow = cwlgen.Workflow("workflow", doc="this will embed this subworkflow")

        self.workflow.steps.append(cwlgen.WorkflowStep("subworkflow-step", run=self.subworkflow))

    def test_subworkflow(self):
        sw = self.workflow.steps[0].run
        self.assertIsInstance(sw, cwlgen.Workflow)
        self.assertEqual(sw.id, self.subworkflow.id)

    def test_serialization(self):
        d = self.workflow.get_dict()
        self.assertIn("steps", d)
        steps = d["steps"]  # this should be a dictionary, so we look at 'key in dict'
        step_id = self.workflow.steps[0].id
        self.assertIn(step_id, steps)
        sw_step = steps[step_id]
        self.assertIsInstance(sw_step, dict)
        self.assertIn("run", sw_step)
        sw = sw_step["run"]
        self.assertIn("class", sw)
        sw_class = sw["class"]
        self.assertEqual(sw_class, "Workflow")


class TestParameter(unittest.TestCase):

    def setUp(self):
        self.param = cwlgen.Parameter('an_id', param_type='File', label='a_label', \
                                      doc='a_doc', param_format='a_format', \
                                      streamable=True, secondary_files='sec_files')
        self.nonfile_param = cwlgen.Parameter('non-file', param_type="string", label="a string",
                                              streamable=True, secondary_files=[".txt"], doc="documentation here")

        self.array_param = cwlgen.Parameter('an array', param_type='string[]', label="an array of strings")

    def test_init(self):
        self.assertEqual(self.param.id, 'an_id')
        self.assertEqual(self.param.type, 'File')
        self.assertEqual(self.param.doc, 'a_doc')
        self.assertEqual(self.param.format, 'a_format')
        self.assertEqual(self.param.label, 'a_label')
        self.assertEqual(self.param.secondaryFiles, 'sec_files')
        self.assertTrue(self.param.streamable)

    def test_get_dict(self):
        dict_test = self.param.get_dict()
        self.assertEqual(dict_test['type'], 'File')
        self.assertEqual(dict_test['doc'], 'a_doc')
        self.assertEqual(dict_test['format'], 'a_format')
        self.assertEqual(dict_test['label'], 'a_label')
        self.assertEqual(dict_test['secondaryFiles'], 'sec_files')
        self.assertTrue(dict_test['streamable'])

    # def test_nonfile_get_dict(self):
    #     dict_test = self.nonfile_param.get_dict()
    #     self.assertEqual(dict_test['type'], 'string')
    #     self.assertEqual(dict_test['doc'], self.nonfile_param.doc)
    #     self.assertNotIn('secondaryFiles', dict_test)
    #     self.assertNotIn('streamable', dict_test)
    #     self.assertNotIn('format', dict_test)

    def test_array(self):
        dict_test = self.array_param.get_dict()
        td = dict_test['type']
        self.assertIsInstance(td, dict)
        self.assertEqual(td['type'], 'array')
        self.assertEqual(td['items'], self.array_param.type.items)


class TestCommandInputParameter(unittest.TestCase):

    def setUp(self):
        self.frst_inp = cwlgen.CommandInputParameter('frst_id', param_type='File', \
                                                     label='a_label', \
                                                     default='def_value')
        binding = cwlgen.CommandLineBinding(position=2, prefix='--prefix')
        self.scnd_inp = cwlgen.CommandInputParameter('scnd_id', param_type='File', \
                                                     input_binding=binding)

    def test_init(self):
        # Test first input
        self.assertEqual(self.frst_inp.id, 'frst_id')
        self.assertEqual(self.frst_inp.type, 'File')
        self.assertEqual(self.frst_inp.label, 'a_label')
        self.assertEqual(self.frst_inp.default, 'def_value')
        # Test second input
        self.assertEqual(self.scnd_inp.id, 'scnd_id')
        self.assertEqual(self.scnd_inp.type, 'File')
        self.assertEqual(self.scnd_inp.inputBinding.position, 2)
        self.assertEqual(self.scnd_inp.inputBinding.prefix, '--prefix')

    def test_get_dict(self):
        # Test first input
        dict_frst = self.frst_inp.get_dict()
        self.assertEqual(dict_frst['type'], 'File')
        self.assertEqual(dict_frst['default'], 'def_value')
        self.assertEqual(dict_frst['label'], 'a_label')
        # Test second input
        dict_scnd = self.scnd_inp.get_dict()
        self.assertEqual(dict_scnd['type'], 'File')
        self.assertEqual(dict_scnd['inputBinding']['prefix'], '--prefix')
        self.assertEqual(dict_scnd['inputBinding']['position'], 2)

    def test_default(self):
        df = "DefaultParam"
        t = cwlgen.CommandInputParameter("has-default", default=df)
        d = t.get_dict()
        self.assertIn("default", d)
        self.assertEqual(t.default, d["default"])


class TestStep(unittest.TestCase):

    def test_ignore_id(self):
        step = cwlgen.WorkflowStep("identifier", "run")
        d = step.get_dict()
        self.assertNotIn("id", d)
        self.assertNotIn("ignore_attributes", d)

    def test_include_id(self):
        step = cwlgen.WorkflowStep("identifier", "run")
        step.ignore_attributes = None
        d = step.get_dict()
        self.assertIn("id", d)
        self.assertNotIn("ignore_attributes", d)


class TestCommandOutputParameter(unittest.TestCase):

    def setUp(self):
        self.outp = cwlgen.CommandOutputParameter('an_out_id', param_type='File')

    def test_init(self):
        self.assertEqual(self.outp.id, 'an_out_id')
        self.assertEqual(self.outp.type, 'File')

    def test_get_dict(self):
        dict_test = self.outp.get_dict()
        self.assertEqual(dict_test['type'], 'File')

    def test_empty_outputbinding(self):
        s = cwlgen.CommandOutputParameter("empty", output_binding=cwlgen.CommandOutputBinding()).get_dict()
        self.assertNotIn('outputBinding', s)
        self.assertEqual(s, {'id': 'empty'})

    def test_nonempty_outputbinding(self):
        s = cwlgen.CommandOutputParameter(
            "nonempty",
            output_binding=cwlgen.CommandOutputBinding(glob="$(inputs.test)")).get_dict()
        self.assertEqual(s, {'id': 'nonempty', 'outputBinding': {'glob': '$(inputs.test)'}})


class TestCommandLineBinding(unittest.TestCase):

    def setUp(self):
        self.line_binding = cwlgen.CommandLineBinding(load_contents=True, position=1, prefix='--prefix', separate=True,
                                                      item_separator='-', shell_quote=True, value_from='text.txt')
        self.false_line_binding = cwlgen.CommandLineBinding(load_contents=False, position=0, prefix='', separate=False,
                                                            item_separator='', shell_quote=False, value_from="")

    def test_init(self):
        self.assertTrue(self.line_binding.loadContents)
        self.assertEqual(self.line_binding.position, 1)
        self.assertEqual(self.line_binding.prefix, '--prefix')
        self.assertTrue(self.line_binding.separate)
        self.assertEqual(self.line_binding.itemSeparator, '-')
        self.assertTrue(self.line_binding.shellQuote)
        self.assertEqual(self.line_binding.valueFrom, 'text.txt')

    def test_get_dict(self):
        dict_test = self.line_binding.get_dict()
        self.assertEqual(dict_test['position'], 1)
        self.assertEqual(dict_test['prefix'], '--prefix')
        self.assertTrue(dict_test['separate'])
        self.assertEqual(dict_test['itemSeparator'], '-')
        self.assertTrue(dict_test['shellQuote'])
        self.assertEqual(dict_test['valueFrom'], 'text.txt')

    def test_false_dict(self):
        d = self.false_line_binding.get_dict()
        self.assertIn("loadContents", d)
        self.assertIn("position", d)
        self.assertIn("prefix", d)
        self.assertIn("separate", d)
        self.assertIn("itemSeparator", d)
        self.assertIn("shellQuote", d)
        self.assertIn("valueFrom", d)


class TestCommandOutputBinding(unittest.TestCase):

    def setUp(self):
        self.out_binding = cwlgen.CommandOutputBinding(glob='file.txt', load_contents=True, \
                                                       output_eval='eval')

    def test_init(self):
        self.assertEqual(self.out_binding.glob, 'file.txt')
        self.assertTrue(self.out_binding.loadContents)
        self.assertEqual(self.out_binding.outputEval, 'eval')

    def test_get_dict(self):
        dict_test = self.out_binding.get_dict()
        self.assertEqual(dict_test['glob'], 'file.txt')
        self.assertTrue(dict_test['loadContents'])
        self.assertEqual(dict_test['outputEval'], 'eval')

###########  Main  ###########

# if __name__ == "__main__":
#     unittest.main()
