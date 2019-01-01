'''
Library to handle the manipulation and generation of CWL tool
'''

#  Import  ------------------------------

# General libraries
import logging

# External libraries
import ruamel.yaml
import six
from .version import __version__

from .utils import literal, literal_presenter
from .elements import Parameter, CommandInputArraySchema, CWL_VERSIONS, DEF_VERSION, CWL_SHEBANG, CwlTypes
from .commandlinebinding import CommandLineBinding
from .workflow import Workflow, InputParameter, WorkflowOutputParameter, WorkflowStep, WorkflowStepInput, \
    WorkflowStepOutput
from .requirements import *
from .import_cwl import parse_cwl

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)


#  Function(s)  ------------------------------

#  Class(es)  ------------------------------


class CommandLineTool(object):
    '''
    Contain all informations to describe a CWL command line tool.
    '''

    __CLASS__ = 'CommandLineTool'

    def __init__(self, tool_id=None, base_command=None, label=None, doc=None,
                 cwl_version=None, stdin=None, stderr=None, stdout=None, path=None):
        '''
        :param tool_id: unique identifier for this tool
        :type tool_id: STRING
        :param base_command: command line for the tool
        :type base_command: STRING | list[STRING]
        :param label: label of this tool
        :type label: STRING
        :param doc: documentation for the tool, usually longer than the label
        :type doc: STRING
        :param cwl_version: version of the CWL tool
        :type cwl_version: STRING
        :param stdin: path to a file whose contents must be piped into stdin
        :type stdin: STRING
        :param stderr: capture stderr into the given file
        :type stderr: STRING
        :param stdout: capture stdout into the given file
        :type stdout: STRING

        inputs (:class:`cwlgen.CommandInputParameter` objects),
        outputs (:class:`cwlgen.CommandOutputParameter` objects),
        arguments (:class:`cwlgen.CommandLineBinding` objects),
        and requirements (:class:`cwlgen.Requirement` objects)
        are stored in lists which are initialized empty.
        '''
        if cwl_version not in CWL_VERSIONS:
            _LOGGER.warning("CWL version {} is not recognized as a valid version.".format(cwl_version))
            _LOGGER.warning("CWL version is set up to {}.".format(DEF_VERSION))
            cwl_version = DEF_VERSION
        self.cwlVersion = cwl_version
        self.id = tool_id
        self.label = label
        self.requirements = []  # List of Several object inhereting from [Requirement]
        self.hints = []
        self.inputs = []  # List of [CommandInputParameter] objects
        self.outputs = []  # List of [CommandOutputParameter] objects
        self.baseCommand = base_command
        self.arguments = []  # List of [CommandLineBinding] objects
        self.doc = doc
        self.stdin = stdin
        self.stderr = stderr
        self.stdout = stdout
        self.successCodes = []
        self.temporaryFailCodes = []
        self.permanentFailCodes = []
        self._path = path
        self.namespaces = Namespaces()

    def get_dict(self):
        cwl_tool = {k: v for k, v in vars(self).items() if v is not None and
                    type(v) is str}
        cwl_tool['class'] = self.__CLASS__
        # Treat doc for multiline writting
        if self.doc:
            cwl_tool['doc'] = literal(self.doc)

        if self.baseCommand:
            cwl_tool['baseCommand'] = self.baseCommand

        # Add Arguments
        cwl_tool['arguments'] = [in_arg.get_dict() for in_arg in self.arguments]

        # Add Inputs
        cwl_tool['inputs'] = {}
        for in_param in self.inputs:
            cwl_tool['inputs'][in_param.id] = in_param.get_dict()

        # Add Outputs
        cwl_tool['outputs'] = {}
        for out_param in self.outputs:
            cwl_tool['outputs'][out_param.id] = out_param.get_dict()

        if self.successCodes:
            cwl_tool['successCodes'] = self.successCodes
        if self.temporaryFailCodes:
            cwl_tool['temporaryFailCodes'] = self.temporaryFailCodes
        if self.permanentFailCodes:
            cwl_tool['permanentFailCodes'] = self.permanentFailCodes

        # If metadata are present in the description
        if getattr(self, 'metadata', None):
            for key, value in self.metadata.__dict__.items():
                cwl_tool["s:" + key] = value
            # - Add Namespaces
            cwl_tool[self.namespaces.name] = {}
            for k, v in self.namespaces.__dict__.items():
                if '$' not in v:
                    cwl_tool[self.namespaces.name][k] = v

        if self.requirements:
            cwl_tool['requirements'] = {r.req_class: r.get_dict() for r in self.requirements}

        return cwl_tool

    def export(self, outfile=None):
        """
        Export the tool in CWL either on STDOUT or in outfile.
        """
        # First add representer (see .utils.py) for multiline writting
        ruamel.yaml.add_representer(literal, literal_presenter)
        cwl_tool = self.get_dict()

        # Write CWL file in YAML
        if outfile is None:
            six.print_(CWL_SHEBANG, "\n", sep='')
            six.print_(ruamel.yaml.dump(cwl_tool))
        else:
            out_write = open(outfile, 'w')
            out_write.write(CWL_SHEBANG + '\n\n')
            out_write.write(ruamel.yaml.dump(cwl_tool))
            out_write.close()


class CommandInputParameter(Parameter):
    '''
    An input parameter for a :class:`cwlgen.CommandLineTool`.
    '''

    def __init__(self, param_id, label=None, secondary_files=None, param_format=None,
                 streamable=False, doc=None, input_binding=None, default=None, param_type=None):
        '''
        :param param_id: unique identifier for this parameter
        :type param_id: STRING
        :param label: short, human-readable label
        :type label: STRING
        :param secondary_files: If type is a file, describes files that must be
                                included alongside the primary file(s)
        :type secondary_files: STRING
        :param param_format: If type is a file, uri to ontology of the format or exact format.
        :type param_format: STRING
        :param streamable: If type is a file, true indicates that the file is read or written
                           sequentially without seeking
        :type streamable: BOOLEAN
        :param doc: documentation
        :type doc: STRING
        :param input_binding: describes how to handle the input
        :type input_binding: :class:`cwlgen.CommandLineBinding` object
        :param default: default value
        :type default: STRING
        :param param_type: type of data assigned to the parameter corresponding to CWLType
        :type param_type: STRING
        '''
        Parameter.__init__(self, param_id=param_id, label=label,
                           secondary_files=secondary_files, param_format=param_format,
                           streamable=streamable, doc=doc, param_type=param_type)
        self.inputBinding = input_binding
        self.default = default

    def get_dict(self):
        '''
        Transform the object to a [DICT] to write CWL.

        :return: dictionnary of the object
        :rtype: DICT
        '''
        dict_in = Parameter.get_dict(self)
        del dict_in['id']
        if self.inputBinding:
            dict_in['inputBinding'] = self.inputBinding.get_dict()
        return dict_in


class CommandOutputParameter(Parameter):
    '''
    An output parameter for a :class:`cwlgen.CommandLineTool`.
    '''

    def __init__(self, param_id, label=None, secondary_files=None, param_format=None,
                 streamable=False, doc=None, output_binding=None, param_type=None):
        '''
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
        :param output_binding: describes how to handle the output
        :type output_binding: :class:`cwlgen.CommandOutputBinding` object
        :param param_type: type of data assigned to the parameter corresponding to CWLType
        :type param_type: STRING
        '''
        Parameter.__init__(self, param_id, label, secondary_files, param_format, streamable,
                           doc, param_type)
        self.outputBinding = output_binding

    def get_dict(self):
        '''
        Transform the object to a [DICT] to write CWL.

        :return: dictionnary of the object
        :rtype: DICT
        '''
        dict_out = Parameter.get_dict(self)
        del dict_out['id']
        if self.outputBinding:
            dict_out['outputBinding'] = self.outputBinding.get_dict()
        return dict_out


class CommandOutputBinding(object):
    '''
    Describes how to generate an output parameter based on the files produced.
    '''

    def __init__(self, glob=False, load_contents=False, output_eval=None):
        '''
        :param glob: Find corresponding file(s)
        :type glob: STRING
        :param load_contents: For each file matched, read up to the 1st 64 KiB of text and
                              place it in the contents field
        :type load_contents: BOOLEAN
        :param output_eval: Evaluate an expression to generate the output value
        :type output_eval: STRING
        '''
        self.glob = glob
        self.loadContents = load_contents
        self.outputEval = output_eval

    def get_dict(self):
        '''
        Transform the object to a [DICT] to write CWL.

        :return: dictionnary of the object
        :rtype: DICT
        '''
        dict_binding = {k: v for k, v in vars(self).items() if v is not None and v is not False}
        return dict_binding


class Namespaces(object):
    """
    Define different namespace for the description.
    """

    def __init__(self):
        """
        """
        self.name = "$namespaces"
        self.s = "http://schema.org/"


class Metadata(object):
    """
    Represent metadata described by http://schema.org.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
