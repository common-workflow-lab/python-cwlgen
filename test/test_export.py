import unittest


class TestExport(unittest.TestCase):

    def test_workflow_export(self):
        import cwlgen
        w = cwlgen.Workflow("identifier")
        w.export()

    def test_commandlinetool_export(self):
        import cwlgen

        c = cwlgen.CommandLineTool("identifier", "echo")
        c.export()
