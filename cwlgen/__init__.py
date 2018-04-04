'''
Library to handle the manipulation and generation of CWL tool
'''

#  Import  ------------------------------

# General libraries
import os
import argparse
import sys
import logging

# External libraries
import ruamel.yaml
import six
from .version import __version__

from .utils import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

#  Constant(s)  ------------------------------

CWL_SHEBANG = "#!/usr/bin/env cwl-runner"
CWL_VERSIONS = ['draft-2', 'draft-3.dev1', 'draft-3.dev2', 'draft-3.dev3',
                'draft-3.dev4', 'draft-3.dev5', 'draft-3', 'draft-4.dev1',
                'draft-4.dev2', 'draft-4.dev3', 'v1.0.dev4', 'v1.0', None]
DEF_VERSION = 'v1.0'
CWL_TYPE = ['null', 'boolean', 'int', 'long', 'float', 'double', 'string', 'File',
            'Directory', None]

#  Function(s)  ------------------------------

#  Class(es)  ------------------------------


class CommandLineTool(object):
    '''
    Contain all informations to describe a CWL command line tool.
    '''

    __CLASS__ = 'CommandLineTool'

    def __init__(self, tool_id=None, base_command=None, label=None, doc=None,
                 cwl_version=None, stdin=None, stderr=None, stdout=None):
        '''
        :param tool_id: unique identifier for this tool
        :type tool_id: STRING
        :param base_command: command line for the tool
        :type base_command: STRING
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
            LOGGER.warning("CWL version is not recognized as a valid version.")
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
        self.namespaces = Namespaces()

    def export(self, outfile=None):
        """
        Export the tool in CWL either on STDOUT or in outfile.
        """
        # First add representer (see .utils.py) for multiline writting
        ruamel.yaml.add_representer(literal, literal_presenter)
        cwl_tool = {k: v for k, v in vars(self).items() if v is not None and\
                                                           type(v) is str}
        cwl_tool['class'] = self.__CLASS__
        # Treat doc for multiline writting
        if self.doc:
            cwl_tool['doc'] = literal(self.doc)

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

        # If metadata are present in the description
        if getattr(self, 'metadata', None):
            for key, value in self.metadata.__dict__.items():
                cwl_tool["s:" + key] = value
            # - Add Namespaces
            cwl_tool[self.namespaces.name] = {}
            for k, v in self.namespaces.__dict__.items():
                if '$' not in v:
                    cwl_tool[self.namespaces.name][k] = v

        # Add requirements.
        requirements = {}
        for requirement in self.requirements:
            requirement.add(requirements)

        if requirements:
            cwl_tool['requirements'] = requirements

        # Write CWL file in YAML
        if outfile is None:
            six.print_(CWL_SHEBANG, "\n", sep='')
            six.print_(ruamel.yaml.dump(cwl_tool))
        else:
            out_write = open(outfile, 'w')
            out_write.write(CWL_SHEBANG + '\n\n')
            out_write.write(ruamel.yaml.dump(cwl_tool))
            out_write.close()


class Parameter(object):
    '''
    A parameter (common field of Input and Output) for a CommandLineTool
    '''

    def __init__(self, param_id, label=None, secondary_files=None, param_format=None,
                 streamable=False, doc=None, param_type=None):
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
        :param param_type: type of data assigned to the parameter
        :type param_type: STRING corresponding to CWLType
        '''
        if param_type not in CWL_TYPE:
            LOGGER.warning("The type is incorrect for the parameter.")
            param_type = None
        self.id = param_id
        self.label = label
        self.secondaryFiles = secondary_files
        self.format = param_format
        self.streamable = streamable
        self.doc = doc
        self.type = param_type

    def get_dict(self):
        '''
        Transform the object to a [DICT] to write CWL.

        :return: dictionnary of the object
        :rtype: DICT
        '''
        dict_param = {k: v for k, v in vars(self).items() if v is not None and v is not False}
        if dict_param['type'] != 'File':
            # Remove what is only for File
            for key in ['format', 'secondaryFiles', 'streamable']:
               try:
                   del(dict_param[key])
               except KeyError:
                   pass
        return dict_param


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


class CommandLineBinding(object):
    '''
    Describes how the handle an input or an argument.
    '''

    def __init__(self, load_contents=False, position=None, prefix=None, separate=True,
                 item_separator=None, value_from=None, shell_quote=True):
        '''
        :param load_contents: Read up to the fist 64 KiB of text from the file and
                              place it in the "contents" field of the file object
        :type load_contents: BOOLEAN
        :param position: The sorting key
        :type positio: INT
        :param prefix: Command line prefix to add before the value
        :type prefix: STRING
        :param separate:
        :type separate: BOOLEAN
        :param item_separator: Join the array elements into a single string separated by this item
        :type item_separator: STRING
        :param value_from: Use this as the value
        :type value_from: STRING
        :param shell_quote: Value is quoted on the command line
        :type shell_quote: BOOLEAN
        '''
        self.loadContents = load_contents
        self.position = position
        self.prefix = prefix
        self.separate = separate
        self.itemSeparator = item_separator
        self.valueFrom = value_from
        self.shellQuote = shell_quote

    def get_dict(self):
        '''
        Transform the object to a [DICT] to write CWL.

        :return: dictionnary of the object
        :rtype: DICT
        '''
        dict_binding = {k: v for k, v in vars(self).items() if v is not None}
        return dict_binding


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


class Requirement(object):
    '''
    Requirement that must be met in order to execute the process.
    '''

    def __init__(self, req_class):
        '''
        :param req_class: requirement class
        :type req_class: STRING
        '''
        self.req_class = req_class

    def add(self, tool):
        tool[self.req_class] = self._to_dict()

    def _to_dict(self):
        raise NotImplementedError("Requirement subclass {} not fully implemented".format(
            self.req_class))


class InlineJavascriptReq(Requirement):
    '''
    Workflow platform must support inline Javascript expressions.
    '''

    def __init__(self, expression_lib=None):
        '''
        :param expression_lib: List of Strings
        :type expression_lib: STRING
        '''
        Requirement.__init__(self, 'InlineJavascriptRequirement')
        self.expressionLib = expression_lib


class DockerRequirement(Requirement):
    '''
    Workflow component should be run in a Docker container.
    This class specifies how to fetch or build the image.
    '''

    def __init__(self, docker_pull=None, docker_load=None, docker_file=None,
                 docker_import=None, docker_image_id=None, docker_output_dir=None):
        '''
        :param docker_pull: image to retrive with docker pull
        :type docker_pull: STRING
        :param docker_load: HTTP URL from which to download Docker image
        :type docker_load: STRING
        :param docker_file: supply the contents of a Dockerfile
        :type docker_file: STRING
        :param docker_import: HTTP URL to download and gunzip a Docker images
        :type docker_import: STRING
        :param docker_image_id: Image id for docker run
        :type docker_image_id: STRING
        :param docker_output_dir: designated output dir inside the Docker container
        :type docker_output_dir: STRING
        '''
        Requirement.__init__(self, 'DockerRequirement')
        self.dockerPull = docker_pull
        self.dockerLoad = docker_load
        self.dockerFile = docker_file
        self.dockerImport = docker_import
        self.dockerImageId = docker_image_id
        self.dockerOutputDir = docker_output_dir

    def _to_dict(self):
        """
        Add this requirement to a dictionary description of a
        tool generated in an export method.

        """
        return {p:v for p,v in vars(self).items() if p.startswith('docker') and v is not None}




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
