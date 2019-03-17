import unittest
import cwlgen


class TestAddRequirements(unittest.TestCase):

    def test_inlinejs(self):
        w = cwlgen.Workflow()
        req = cwlgen.InlineJavascriptReq(["expression"])
        w.requirements.append(req)
        d = w.get_dict()
        self.assertIn("requirements", d)
        dr = d["requirements"]
        self.assertIn(req.get_class(), dr)
        drr = dr[req.get_class()]
        self.assertIn("expressionLib", drr)
        self.assertEqual(drr["expressionLib"], ["expression"])

    def test_commandtool(self):
        c = cwlgen.CommandLineTool("reqs")
        docker = cwlgen.DockerRequirement(docker_pull="ubuntu:latest")
        c.requirements.append(docker)

        d = c.get_dict()
        self.assertIn("requirements", d)
        self.assertIn(docker.get_class(), d["requirements"])


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
        self.assertDictEqual(tool, {})


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
        self.assertDictEqual(dr.get_dict(), {})


class TestSubworkflowFeatureRequirement(unittest.TestCase):

    def setUp(self):
        self.req = cwlgen.SubworkflowFeatureRequirement()

    def test_init(self):
        self.assertEqual(self.req.get_class(), 'SubworkflowFeatureRequirement')

    def test_add(self):
        tool = self.req.get_dict()
        self.assertDictEqual(tool, {})


class TestSoftwareRequirement(unittest.TestCase):

    def setUp(self):
        self.r = cwlgen.SoftwareRequirement()
        self.r.packages.append(cwlgen.SoftwareRequirement.SoftwarePackage("package", "version", None))

    def test_properties(self):
        self.assertEqual(self.r.get_class(), "SoftwareRequirement")
        self.assertEqual(len(self.r.packages), 1)
        p = self.r.packages[0]
        self.assertEqual(p.package, "package")
        self.assertEqual(p.version, "version")
        self.assertIsNone(p.specs)

    def test_serialization(self):
        d = self.r.get_dict()
        self.assertIn("packages", d)
        pks = d["packages"]
        self.assertEqual(len(pks), 1)
        p = pks[0]
        self.assertEqual(p.get("package"), "package")
        self.assertEqual(p.get("version"), "version")
        self.assertNotIn("specs", p)


class TestInitialWorkDirRequirement(unittest.TestCase):

    def setUp(self):
        self.i1 = cwlgen.InitialWorkDirRequirement("listing1")
        self.i2 = cwlgen.InitialWorkDirRequirement([
            cwlgen.InitialWorkDirRequirement.Dirent("entry", "entryname")
        ])

    def test_properties_i1(self):
        self.assertEqual(self.i1.get_class(), "InitialWorkDirRequirement")
        self.assertEqual(self.i1.listing, "listing1")

    def test_properties_i2(self):
        self.assertEqual(len(self.i2.listing), 1)
        l = self.i2.listing[0]
        self.assertEqual(l.entry, "entry")
        self.assertEqual(l.entryname, "entryname")
        self.assertIsNone(l.writable)

    def test_serialization_i1(self):
        d = self.i1.get_dict()
        self.assertIn("listing", d)
        self.assertIsInstance(d["listing"], str)
        self.assertEqual(d["listing"], "listing1")

    def test_serialization_i2(self):
        d = self.i2.get_dict()
        self.assertIn("listing", d)
        listing = d.get("listing")
        self.assertIsInstance(listing, list)
        self.assertEqual(len(listing), 1)
        l = listing[0]
        self.assertIn("entry", l)
        self.assertIn("entryname", l)
        self.assertNotIn("writable", l)

        self.assertEqual(l["entry"], "entry")
        self.assertEqual(l["entryname"], "entryname")


class TestScatterFeatureRequirement(unittest.TestCase):

    def setUp(self):
        self.req = cwlgen.ScatterFeatureRequirement()

    def test_init(self):
        self.assertEqual(self.req.get_class(), 'ScatterFeatureRequirement')

    def test_add(self):
        tool = self.req.get_dict()
        self.assertDictEqual(tool, {})


class TestStepInputExpressionRequirement(unittest.TestCase):

    def setUp(self):
        self.req = cwlgen.StepInputExpressionRequirement()

    def test_init(self):
        self.assertEqual(self.req.get_class(), 'StepInputExpressionRequirement')

    def test_add(self):
        tool = self.req.get_dict()
        self.assertDictEqual(tool, {})


class TestEnvVarRequirement(unittest.TestCase):

    def setUp(self):
        self.e = cwlgen.EnvVarRequirement([
            cwlgen.EnvVarRequirement.EnvironmentDef("env_name", "env_value")
        ])

    def test_properties(self):
        self.assertEqual(self.e.get_class(), "EnvVarRequirement")
        self.assertIsInstance(self.e.envDef, list)
        self.assertEqual(len(self.e.envDef), 1)
        e = self.e.envDef[0]
        self.assertEqual(e.envName, "env_name")
        self.assertEqual(e.envValue, "env_value")

    def test_serialization(self):
        d = self.e.get_dict()
        self.assertIn("envDef", d)
        ed = d["envDef"]
        self.assertIsInstance(ed, list)
        self.assertEqual(len(ed), 1)
        e = ed[0]
        self.assertEqual(e.get("envName"), "env_name")
        self.assertEqual(e.get("envValue"), "env_value")


class TestShellCommandRequirement(unittest.TestCase):

    def setUp(self):
        self.req = cwlgen.ShellCommandRequirement()

    def test_init(self):
        self.assertEqual(self.req.get_class(), 'ShellCommandRequirement')

    def test_add(self):
        tool = self.req.get_dict()
        self.assertDictEqual(tool, {})


class TestResourceRequirement(unittest.TestCase):

    def setUp(self):
        self.req = cwlgen.ResourceRequirement(
            cores_min=1, cores_max=3,
            ram_min=2, ram_max=4,
            tmpdir_min="tmp/min", tmpdir_max="tmp/max",
            outdir_min="out/min", outdir_max="out/max"
        )
        self.empty = cwlgen.ResourceRequirement()

    def test_init(self):
        self.assertEqual(self.req.get_class(), 'ResourceRequirement')

        self.assertEqual(1, self.req.coresMin)
        self.assertEqual(3, self.req.coresMax)

        self.assertEqual(2, self.req.ramMin)
        self.assertEqual(4, self.req.ramMax)

        self.assertEqual("tmp/min", self.req.tmpdirMin)
        self.assertEqual("tmp/max", self.req.tmpdirMax)
        self.assertEqual("out/min", self.req.outdirMin)
        self.assertEqual("out/max", self.req.outdirMax)

    def test_empty(self):
        self.assertDictEqual(self.empty.get_dict(), {})

    def test_add(self):
        r = self.req.get_dict()
        self.assertEqual(r.get("coresMin"), 1)
        self.assertEqual(r.get("coresMax"), 3)

        self.assertEqual(r.get("ramMin"), 2)
        self.assertEqual(r.get("ramMax"), 4)

        self.assertEqual(r.get("tmpdirMin"), "tmp/min")
        self.assertEqual(r.get("tmpdirMax"), "tmp/max")
        self.assertEqual(r.get("outdirMin"), "out/min")
        self.assertEqual(r.get("outdirMax"), "out/max")

