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


# Logging setup

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

SCATTER_METHODS = ["dotproduct", "nested_crossproduct", "flat_crossproduct"]
LINK_MERGE_METHODS = ["merge_nested", "merge_flattened"]


#  Function(s)  ------------------------------

def parse_scatter_method(scatter_method, required=False):
    if scatter_method is None and not required:
        return None
    elif scatter_method not in SCATTER_METHODS:
        if required:
            raise Exception("The scatter method '{method}' is not a valid ScatterMethod and requires one of: {expected}"
                            .format(method=scatter_method, expected=" ,".join(SCATTER_METHODS)))
        elif scatter_method is not None:
            _LOGGER.info("The scatter method '{method}' is not a valid ScatterMethod, expected one of: {expected}"
                         .format(method=scatter_method, expected=" ,".join(SCATTER_METHODS)))
            return None
    return scatter_method


def parse_link_merge_method(link_merge, required=False):
    if link_merge is None and not required:
        return None
    elif link_merge not in LINK_MERGE_METHODS:
        if required:
            raise Exception("The link merge method '{method}' is not a valid LinkMergeMethod and requires one of:"
                            " {expected}. ".format(method=link_merge, expected=" ,".join(LINK_MERGE_METHODS)))
        elif link_merge is not None:
            _LOGGER.info("The link merge method '{method}' is not a valid LinkMergeMethod, expected one of:"
                            " {expected}. This value will be null which CWL defaults to 'merge_nested'"
                            .format(method=link_merge, expected=" ,".join(LINK_MERGE_METHODS)))
            return None
    return link_merge


#  Class(es)  ------------------------------

class Workflow(object):
    """
    A workflow describes a set of steps and the dependencies between those steps.
    When a step produces output that will be consumed by a second step,
    the first step is a dependency of the second step.

    Documentation: https://www.commonwl.org/v1.0/Workflow.html#Workflow
    """
    __CLASS__ = 'Workflow'

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
        self.requirements = []
        self.hints = None
        self._path = None

    def get_dict(self):
        cwl_workflow = {k: v for k, v in vars(self).items() if v is not None and type(v) is str}

        cwl_workflow['class'] = self.__CLASS__
        cwl_workflow['cwlVersion'] = self.cwlVersion

        cwl_workflow['inputs'] = {}
        cwl_workflow['outputs'] = {}

        # steps, inputs, outputs are required properties, so it should fail if we can't place it
        cwl_workflow['steps'] = {step.id: step.get_dict() for step in self.steps}
        cwl_workflow['inputs'] = {i.id: i.get_dict() for i in self.inputs}
        cwl_workflow['outputs'] = {o.id: o.get_dict() for o in self.outputs}

        if self.requirements:
            cwl_workflow['requirements'] = {r.get_class(): r.get_dict() for r in self.requirements}

        if self.hints:
            # can be array<Any> | dict<class, Any>
            cwl_workflow['hints'] = self.hints

        return cwl_workflow

    def export(self, outfile=None):
        """
        Export the workflow in CWL either on STDOUT or in outfile.
        """
        # First add representer (see .utils.py) for multiline writting
        ruamel.yaml.add_representer(literal, literal_presenter)

        cwl_workflow = self.get_dict()

        # Write CWL file in YAML
        if outfile is None:
            six.print_(CWL_SHEBANG, "\n", sep='')
            six.print_(ruamel.yaml.dump(cwl_workflow))
        else:
            out_write = open(outfile, 'w')
            out_write.write(CWL_SHEBANG + '\n\n')
            out_write.write(ruamel.yaml.dump(cwl_workflow))
            out_write.close()

    # def add(self, step_id, tool, params):
    #     return StepRun(self, step_id, tool, params)


class InputParameter(Parameter):
    """
    Documentation: https://www.commonwl.org/v1.0/Workflow.html#InputParameter
    """
    def __init__(self, param_id, label=None, secondary_files=None, param_format=None,
                 streamable=False, doc=None, input_binding=None, default=None, param_type=None):
        """
        :param param_id: unique identifier for this parameter
        :type param_id: STRING
        :param label: short, human-readable label
        :type label: STRING
        :param secondary_files: If type is a file, describes files that must be
                                included alongside the primary file(s)
        :type secondary_files: STRING
        :param param_format: If type is a file, uri to ontology of the format or exact format
        :type param_format: STRING
        :param streamable: If type is a file, true indicates that the file is read or written
                           sequentially without seeking
        :type streamable: BOOLEAN
        :param doc: documentation
        :type doc: STRING
        :param param_type: type of data assigned to the parameter
        :type param_type: STRING corresponding to CWLType
        :param input_binding:
        :type input_binding: CommandLineBinding

        """
        Parameter.__init__(self, param_id=param_id, label=label,
                           secondary_files=secondary_files, param_format=param_format,
                           streamable=streamable, doc=doc, param_type=param_type, requires_type=False)
        self.inputBinding = input_binding
        self.default = default

    def get_dict(self):
        input_dict = Parameter.get_dict(self)

        if self.inputBinding:
            # CommandLineBinding
            input_dict["inputBinding"] = self.inputBinding.get_dict()

        if self.default:
            input_dict["default"] = self.default

        return input_dict


class WorkflowStep(Serializable):
    """
    A workflow step is an executable element of a workflow. It specifies the underlying process implementation
    (such as CommandLineTool or another Workflow) in the run field and connects the input and output parameters
    of the underlying process to workflow parameters.

    Documentation: https://www.commonwl.org/v1.0/Workflow.html#WorkflowStep
    """
    def __init__(self, step_id, run, label=None, doc=None, scatter=None, scatter_method=None):
        """
        :param step_id: The unique identifier for this workflow step.
        :type step_id: STRING
        :param run: Specifies the process to run.
        :type run: STRING | CommandLineTool | ExpressionTool | Workflow
        :param label: A short, human-readable label of this process object.
        :type label: STRING
        :param doc: A long, human-readable description of this process object.
        :type doc: STRING | list[STRING]
        :param scatter: Field to scatter on, see: https://www.commonwl.org/v1.0/Workflow.html#WorkflowStep
        :type scatter: STRING | list[STRING]
        :param scatter_method: Required if scatter is an array of more than one element.
        :type scatter_method: STRING | list[STRING] in [dotproduct, nested_crossproduct, flat_crossproduct]
        """
        self.id = step_id
        self.run = run
        self.label = label
        self.doc = doc
        self.scatter = scatter
        self.scatterMethod = parse_scatter_method(scatter_method)

        # in is a reserved keywork
        self.inputs = []
        self.out = []
        self.requirements = []
        self.hints = []

        self.ignore_attributes = ["id", "inputs"]

    def get_dict(self):
        d = super(WorkflowStep, self).get_dict()
        d['in'] = {i.id: i.get_dict() for i in self.inputs}
        return d


class WorkflowStepInput(object):
    """
    The input of a workflow step connects an upstream parameter (from the workflow inputs, or the outputs of
    other workflows steps) with the input parameters of the underlying step.

    Documentation: https://www.commonwl.org/v1.0/Workflow.html#WorkflowStepInput
    """
    def __init__(self, input_id, source=None, link_merge=None, default=None, value_from=None):
        """
        :param input_id: A unique identifier for this workflow input parameter.
        :type input_id: STRING
        :param source: Specifies one or more workflow parameters that will provide input to the underlying step parameter.
        :type source: STRING | list[STRING]
        :param link_merge: The method to use to merge multiple inbound links into a single array.
                           If not specified, the default method is "merge_nested".
        :type link_merge: LinkMergeMethod
        :param default: The default value for this parameter to use if either there is no source field,
                        or the value produced by the source is null
        :type default: Any | DictRepresentible
        :param value_from: If valueFrom is a constant string value, use this as the value for this input parameter.
                           If valueFrom is a parameter reference or expression,
                           it must be evaluated to yield the actual value to be assiged to the input field.
        :type value_from: STRING
        """

        self.id = input_id
        self.source = source
        self.linkMerge = parse_link_merge_method(link_merge)
        self.default = default
        self.valueFrom = value_from

    def get_dict(self):
        """
        Transform the object to a [DICT] to write CWL.
        :return: dictionary of the object
        :rtype: DICT
        """
        dict_param = {
            'id': self.id
        }

        if self.source:
            dict_param['source'] = self.source

        if self.linkMerge:
            dict_param['linkMerge'] = self.linkMerge

        if self.default:
            dict_param['default'] = self.default

        if self.valueFrom:
            dict_param['valueFrom'] = self.valueFrom

        return dict_param


class WorkflowStepOutput(object):
    """
    Associate an output parameter of the underlying process with a workflow parameter.
    The workflow parameter (given in the id field) be may be used as a source to connect with
    input parameters of other workflow steps, or with an output parameter of the process.

    Documentation: https://www.commonwl.org/v1.0/Workflow.html#WorkflowStepOutput
    """
    def __init__(self, output_id):
        """
        :param output_id: A unique identifier for this workflow output parameter. This is the identifier to use in
        the source field of WorkflowStepInput to connect the output value to downstream parameters.
        :type output_id: STRING
        """
        self.id = output_id

    def get_dict(self):
        return self.id


class WorkflowOutputParameter(Parameter):
    """
    Describe an output parameter of a workflow. The parameter must be connected to one or more parameters
    defined in the workflow that will provide the value of the output parameter.

    Documentation: https://www.commonwl.org/v1.0/Workflow.html#WorkflowOutputParameter
    """
    def __init__(self, param_id, output_source=None, label=None, secondary_files=None, param_format=None,
                 streamable=False, doc=None, param_type=None, output_binding=None, linkMerge=None):
        """
        Documentation: https://www.commonwl.org/v1.0/Workflow.html#WorkflowOutputParameter
        :param param_id: The unique identifier for this parameter object.
        :type param_id: STRING
        :param output_source: Specifies one or more workflow parameters that supply the value of to the output parameter
        :type output_source: STRING | list[STRING]
        :param label: A short, human-readable label of this object.
        :type label: STRING
        :param secondary_files: Provides a pattern or expression specifying files or directories that must be
                                included alongside the primary file.
        :type secondary_files: STRING \ list[STRING]
        :param param_format: This is the file format that will be assigned to the output paramete
        :type param_format: STRING
        :param streamable: A value of true indicates that the file is read or written sequentially without seeking
        :type streamable: BOOLEAN
        :param doc: A documentation string for this type, or an array of strings which should be concatenated.
        :type doc: STRING | list[STRING]
        :param param_type: Specify valid types of data that may be assigned to this parameter.
        :type param_type: CWLType | OutputRecordSchema | OutputEnumSchema | OutputArraySchema | string | Array<type>
        :param output_binding: Describes how to handle the outputs of a process.
        :type output_binding: CommandOutputBinding
        :param linkMerge:
        :type linkMerge: STRING
        """
        Parameter.__init__(self, param_id=param_id, label=label,
                           secondary_files=secondary_files, param_format=param_format,
                           streamable=streamable, doc=doc, param_type=param_type, requires_type=False)
        self.outputSource = output_source
        self.outputBinding = output_binding     # CommandOutputBinding
        self.linkMerge = linkMerge

    def get_dict(self):
        output_dict = Parameter.get_dict(self)

        if self.outputSource:
            output_dict["outputSource"] = self.outputSource
        if self.outputBinding:
            output_dict["outputBinding"] = self.outputBinding.get_dict()
        if self.format:
            output_dict["format"] = self.format
        if self.linkMerge:
            output_dict["linkMerge"] = self.linkMerge

        return output_dict


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
