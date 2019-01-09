import unittest

import cwlgen


class TestInlineJavascriptReq(unittest.TestCase):

    def setUp(self):
        self.js_req = cwlgen.InlineJavascriptReq(expression_lib=['expression'])
        self.js_req_nolib = cwlgen.InlineJavascriptReq()

    def test_init(self):
        self.assertEqual(self.js_req.get_class(), 'InlineJavascriptRequirement')
        self.assertEqual(self.js_req.expressionLib, ['expression'])
        self.assertEqual(self.js_req_nolib.get_class(), 'InlineJavascriptRequirement')
        self.assertIsNone(self.js_req_nolib.expressionLib)

    def test_export(self):
        tool = self.js_req.get_dict()
        self.assertEqual(tool, {'expressionLib': ['expression']})

    def test_export_without_lib(self):
        tool = self.js_req_nolib.get_dict()
        self.assertEqual(tool, {})


class TestDockerRequirement(unittest.TestCase):

    def setUp(self):
        self.dock_req = cwlgen.DockerRequirement(
            docker_pull='pull',
            docker_load='load',
            docker_file='file',
            docker_import='import',
            docker_image_id='id',
            docker_output_dir='dir'
        )

    def test_init(self):
        self.assertEqual(self.dock_req.get_class(), 'DockerRequirement')
        self.assertEqual(self.dock_req.dockerPull, 'pull')
        self.assertEqual(self.dock_req.dockerLoad, 'load')
        self.assertEqual(self.dock_req.dockerFile, 'file')
        self.assertEqual(self.dock_req.dockerImport, 'import')
        self.assertEqual(self.dock_req.dockerImageId, 'id')
        self.assertEqual(self.dock_req.dockerOutputDir, 'dir')

    def test_export(self):
        d = self.dock_req.get_dict()
        comparison = {
            'dockerFile': 'file',
            'dockerImageId': 'id',
            'dockerImport': 'import',
            'dockerLoad': 'load',
            'dockerOutputDir': 'dir',
            'dockerPull': 'pull'
        }
        self.assertEqual(d, comparison)

    def test_missing_export(self):
        dr = cwlgen.DockerRequirement()
        self.assertEqual(dr.get_dict(), {})


class TestSubworkflowFeatureRequirement(unittest.TestCase):

    def setUp(self):
        self.req = cwlgen.SubworkflowFeatureRequirement()

    def test_init(self):
        self.assertEqual(self.req.get_class(), 'SubworkflowFeatureRequirement')

    def test_add(self):
        tool = self.req.get_dict()
        self.assertEqual(tool, {})
