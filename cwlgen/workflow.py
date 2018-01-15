

import ruamel.yaml
import six

from . import CWL_SHEBANG, Parameter
from .utils import *


class Workflow(object):
    '''
    Contain all informations to describe a CWL workflow.
    '''
    __CLASS__ = 'Workflow'

    def __init__(self):
        self.steps = []
        self.inputs = []
        self.outputs = []

    def export(self, outfile=None):
        """
        Export the workflow in CWL either on STDOUT or in outfile.
        """
        # First add representer (see .utils.py) for multiline writting
        ruamel.yaml.add_representer(literal, literal_presenter)
        cwl_workflow = {k: v for k, v in vars(self).items() if v is not None and\
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

class InputParameter(Parameter):
    def __init__(self, param_id, label=None, secondary_files=None, param_format=None,
                 streamable=False, doc=None, input_binding=None, default=None, param_type=None):
        Parameter.__init__(self, param_id=param_id, label=label,
                           secondary_files=secondary_files, param_format=param_format,
                           streamable=streamable, doc=doc, param_type=param_type)


class WorkflowStep(object):
    def __init__(self, id, inputs=None, outputs=None, run=None):
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
        dict_param = {'id' : self.id, "run" : self.run} #{k: v for k, v in vars(self).items() if v is not None and v is not False}

        if self.inputs:
            dict_param['in'] = {}
            for i in self.inputs:
                if i.src:
                    dict_param['in'][i.id] = i.src
                elif i.default:
                    dict_param['in'][i.id] = {"default" : i.default}

        if self.outputs:
            dict_param['out'] = []
            for i in self.outputs:
                dict_param['out'].append(i)

        return dict_param

class WorkflowStepInput(object):
    def __init__(self, id, src=None, default=None):
        self.id = id
        self.src = src
        self.default = default

    def get_dict(self):
        '''
        Transform the object to a [DICT] to write CWL.

        :return: dictionnary of the object
        :rtype: DICT
        '''
        dict_param = {} #{k: v for k, v in vars(self).items() if v is not None and v is not False}
        if self.src:
            dict_param["src"] = self.src
        if self.default:
            dict_param["default"] = self.default
        return dict_param

class WorkflowStepOutput(object):
    def __init__(self, id):
        self.id = id



class WorkflowOutputParameter(Parameter):
    def __init__(self, param_id, outputSource, label=None, secondary_files=None, param_format=None,
                 streamable=False, doc=None, param_type=None):
        Parameter.__init__(self, param_id=param_id, label=label,
                           secondary_files=secondary_files, param_format=param_format,
                           streamable=streamable, doc=doc, param_type=param_type)
        self.outputSource = outputSource
