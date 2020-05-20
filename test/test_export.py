import unittest


class TestExport(unittest.TestCase):

    def test_workflow_export(self):
        import cwlgen
        w = cwlgen.Workflow("identifier")
        expected = """\
class: Workflow
cwlVersion: v1.0
id: identifier
inputs: {}
outputs: {}
steps: {}
"""
        self.assertEqual(expected, w.export_string())

    def test_commandlinetool_export(self):
        import cwlgen

        c = cwlgen.CommandLineTool("identifier", "echo")
        expected = """\
baseCommand: echo
class: CommandLineTool
cwlVersion: v1.0
id: identifier
inputs: {}
outputs: {}
"""
        self.assertEqual(expected, c.export_string())
