#  Import  ------------------------------

# General libraries
import logging

# External libraries
import ruamel.yaml
import six

from .version import __version__

# Internal libraries

from .utils import literal, literal_presenter, Serializable
from .common import Parameter, CWL_SHEBANG
from .workflowdeps import InputParameter, WorkflowOutputParameter, WorkflowStep


# Logging setup

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)


#  Function(s)  ------------------------------


#  Class(es)  ------------------------------

class Workflow(Serializable):
    """
    A workflow describes a set of steps and the dependencies between those steps.
    When a step produces output that will be consumed by a second step,
    the first step is a dependency of the second step.

    Documentation: https://www.commonwl.org/v1.0/Workflow.html#Workflow
    """
    __CLASS__ = 'Workflow'
    ignore_fields_on_parse = ["class"]
    ignore_fields_on_convert = ["inputs", "outputs"]
    parse_types = {
        "inputs": [[InputParameter]],
        "outputs": [[WorkflowOutputParameter]],
        "steps": [[WorkflowStep]],
    }

    def __init__(self, workflow_id=None, label=None, doc=None, cwl_version='v1.0'):
        """
        :param workflow_id: The unique identifier for this process object.
        :type workflow_id: STRING
        :param label: A short, human-readable label of this process object.
        :type label: STRING
        :param doc: A long, human-readable description of this process object.
        :type doc: STRING
        :param cwl_version: CWL document version. Always required at the document root. Default: 'v1.0'
        :type cwl_version: CWLVersion
        """
        self.id = workflow_id
        self.label = label
        self.doc = doc
        self.cwlVersion = cwl_version

        self.inputs = []            # list[InputParameter]
        self.outputs = []           # list[WorkflowOutputParameter]
        self.steps = []             # list[WorkflowStep]
        self.requirements = []      # list[Requirement]
        self.hints = []             # list[Requirement]
        self._path = None

    def get_dict(self):
        cwl_workflow = super(Workflow, self).get_dict()

        cwl_workflow['class'] = self.__CLASS__

        cwl_workflow['inputs'] = {}
        cwl_workflow['outputs'] = {}

        # steps, inputs, outputs are required properties, so it should fail if we can't place it
        cwl_workflow['steps'] = {step.id: step.get_dict() for step in self.steps}
        cwl_workflow['inputs'] = {i.id: i.get_dict() for i in self.inputs}
        cwl_workflow['outputs'] = {o.id: o.get_dict() for o in self.outputs}

        if self.requirements:
            cwl_workflow['requirements'] = {r.get_class(): r.get_dict() for r in self.requirements}

        return cwl_workflow

    def export_string(self):
        ruamel.yaml.add_representer(literal, literal_presenter)
        cwl_tool = self.get_dict()
        return ruamel.yaml.dump(cwl_tool, default_flow_style=False)

    def export(self, outfile=None):
        """
        Export the workflow in CWL either on STDOUT or in outfile.
        """
        rep = self.export_string()

        # Write CWL file in YAML
        if outfile is None:
            six.print_(CWL_SHEBANG, "\n", sep='')
            six.print_(rep)
        else:
            out_write = open(outfile, 'w')
            out_write.write(CWL_SHEBANG + '\n\n')
            out_write.write(rep)
            out_write.close()



############################
# Workflow construction classes

# class File:
#     """
#     An abstract file reference used for generating workflows
#     """
#     def __init__(self, path):
#         self.path = path
#
#
# class Variable:
#     """
#     An output variable from a workflow step
#     """
#     def __init__(self, workflow, step, name):
#         self.step = step
#         self.name = name
#         self.workflow = workflow
#
#     def path(self):
#         return "%s/%s" % (self.step, self.name)
#
#     def store(self):
#         self.workflow.outputs.append(
#             WorkflowOutputParameter(self.path().replace("/", "_"),
#                                     outputSource=self.path(),
#                                     param_type="File"))
#         return


# class StepRun:
#     """
#     Result of adding a step into a workflow
#     """
#     def __init__(self, workflow, id, tool, params):
#         self.tool = tool
#         self.workflow = workflow
#         self.id = id
#
#         step = WorkflowStep(id=id, run=tool._path)
#         workflow.steps.append(step)
#
#         for i, j in params.items():
#             if isinstance(j, six.string_types):
#                 step.inputs.append(WorkflowStepInput(i, default=j))
#             elif isinstance(j, Variable):
#                 step.inputs.append(WorkflowStepInput(i, src=j.path()))
#             elif isinstance(j, InputParameter):
#                 self.workflow.inputs.append(j),
#                 step.inputs.append(WorkflowStepInput(j.id, src=j.id))
#             elif isinstance(j, File):
#                 # This is just used as a stub, the 'path' inside the file doesn't do anything
#                 self.workflow.inputs.append(InputParameter(i, param_type="File"))
#                 step.inputs.append(WorkflowStepInput(i, src=i))
#         for o in tool.outputs:
#             step.outputs.append(o.id)
#
#     def store_all(self):
#         for i in self.tool.outputs:
#             Variable(self.workflow, self.id, i.id).store()
#
#     def __getitem__(self, key):
#         for i in self.tool.outputs:
#             if i.id == key:
#                 return Variable(self.workflow, self.id, key)
#         raise KeyError
