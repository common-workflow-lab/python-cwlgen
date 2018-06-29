import ruamel.yaml
import six

from .elements import CWL_SHEBANG, Parameter
from .utils import literal, literal_presenter


class Workflow(object):
    """
    Contain all informations to describe a CWL workflow.
    """
    __CLASS__ = 'Workflow'

    def __init__(self):
        self.steps = []
        self.inputs = []
        self.outputs = []
        self._path = None


    def export(self, outfile=None):
        """
        Export the workflow in CWL either on STDOUT or in outfile.
        """
        # First add representer (see .utils.py) for multiline writting
        ruamel.yaml.add_representer(literal, literal_presenter)
        cwl_workflow = {k: v for k, v in vars(self).items() if v is not None and
                        type(v) is str}
        cwl_workflow['class'] = self.__CLASS__
        cwl_workflow['cwlVersion'] = 'v1.0'

        cwl_workflow['inputs'] = {}
        cwl_workflow['outputs'] = {}

        if self.steps:
            cwl_workflow['steps'] = {}
            for step in self.steps:
                cwl_workflow['steps'][step.id] = step.get_dict()

        if self.inputs:
            cwl_workflow['inputs'] = {}
            for i in self.inputs:
                cwl_workflow['inputs'][i.id] = i.get_dict()

        if self.outputs:
            cwl_workflow['outputs'] = {}
            for out in self.outputs:
                cwl_workflow['outputs'][out.id] = out.get_dict()

        # Write CWL file in YAML
        if outfile is None:
            six.print_(CWL_SHEBANG, "\n", sep='')
            six.print_(ruamel.yaml.dump(cwl_workflow))
        else:
            out_write = open(outfile, 'w')
            out_write.write(CWL_SHEBANG + '\n\n')
            out_write.write(ruamel.yaml.dump(cwl_workflow))
            out_write.close()

    def add(self, step_id, tool, params):
        return StepRun(self, step_id, tool, params)


class InputParameter(Parameter):
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
        """
        Parameter.__init__(self, param_id=param_id, label=label,
                           secondary_files=secondary_files, param_format=param_format,
                           streamable=streamable, doc=doc, param_type=param_type)


class WorkflowStep(object):
    def __init__(self, id, inputs=None, outputs=None, run=None):
        """
        :param id: ID of the step
        :type id: STRING
        :param inputs:
        :type inputs:
        :param outputs:
        :type outputs:
        :param run:
        :type run:
        """
        self.id = id
        if inputs:
            self.inputs = inputs
        else:
            self.inputs = []
        if outputs:
            self.outputs = outputs
        else:
            self.outputs = []
        self.run = run

    def get_dict(self):
        '''
        Transform the object to a [DICT] to write CWL.

        :return: dictionnary of the object
        :rtype: DICT
        '''
        # {k: v for k, v in vars(self).items() if v is not None and v is not False}
        dict_param = {'id': self.id, "run": self.run}

        if self.inputs:
            dict_param['in'] = {}
            for i in self.inputs:
                if i.src:
                    dict_param['in'][i.id] = i.src
                elif i.default:
                    dict_param['in'][i.id] = {"default": i.default}

        if self.outputs:
            dict_param['out'] = []
            for i in self.outputs:
                if isinstance(i, WorkflowStepOutput):
                    dict_param['out'].append(i.id)
                else:
                    dict_param['out'].append(i)

        return dict_param


class WorkflowStepInput(object):
    def __init__(self, id, src=None, default=None):
        """
        :param id: ID of the step input
        :type id: STRING
        :param src:
        :type src:
        :param default:
        :type default:
        """
        self.id = id
        self.src = src
        self.default = default

    def get_dict(self):
        """
        Transform the object to a [DICT] to write CWL.

        :return: dictionnary of the object
        :rtype: DICT
        """
        dict_param = {}  # {k: v for k, v in vars(self).items() if v is not None and v is not False}
        if self.src:
            dict_param["src"] = self.src
        if self.default:
            dict_param["default"] = self.default
        return dict_param


class WorkflowStepOutput(object):
    def __init__(self, id):
        """
        :param id:
        :type id:
        """
        self.id = id


class WorkflowOutputParameter(Parameter):
    def __init__(self, param_id, outputSource, label=None, secondary_files=None, param_format=None,
                 streamable=False, doc=None, param_type=None):
        Parameter.__init__(self, param_id=param_id, label=label,
                           secondary_files=secondary_files, param_format=param_format,
                           streamable=streamable, doc=doc, param_type=param_type)
        self.outputSource = outputSource

############################
# Workflow construction classes


class File:
    """
    An abstract file reference used for generating workflows
    """
    def __init__(self, path):
        self.path = path




class Variable:
    """
    An output variable from a workflow step
    """
    def __init__(self, workflow, step, name):
        self.step = step
        self.name = name
        self.workflow = workflow

    def path(self):
        return "%s/%s" % (self.step, self.name)

    def store(self):
        self.workflow.outputs.append(
            WorkflowOutputParameter(self.path().replace("/", "_"),
                                    outputSource=self.path(),
                                    param_type="File"))
        return




class StepRun:
    """
    Result of adding a step into a workflow
    """
    def __init__(self, workflow, id, tool, params):
        self.tool = tool
        self.workflow = workflow
        self.id = id

        step = WorkflowStep(id=id, run=tool._path)
        workflow.steps.append(step)

        for i, j in params.items():
            if isinstance(j, six.string_types):
                step.inputs.append(WorkflowStepInput(i, default=j))
            elif isinstance(j, Variable):
                step.inputs.append(WorkflowStepInput(i, src=j.path()))
            elif isinstance(j, InputParameter):
                self.workflow.inputs.append(j),
                step.inputs.append(WorkflowStepInput(j.id, src=j.id))
            elif isinstance(j, File):
                # This is just used as a stub, the 'path' inside the file doesn't do anything
                self.workflow.inputs.append(InputParameter(i, param_type="File"))
                step.inputs.append(WorkflowStepInput(i, src=i))
        for o in tool.outputs:
            step.outputs.append(o.id)

    def store_all(self):
        for i in self.tool.outputs:
            Variable(self.workflow, self.id, i.id).store()

    def __getitem__(self, key):
        for i in self.tool.outputs:
            if i.id == key:
                return Variable(self.workflow, self.id, key)
        raise KeyError
