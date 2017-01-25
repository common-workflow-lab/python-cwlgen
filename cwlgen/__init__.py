#!/usr/bin/env python

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.6.0
## Creation : 12-30-2016

'''
Library to handle the manipulation and generation of CWL tool
'''

###########  Import  ###########

# General libraries
import os
import argparse
import sys

# External libraries
import ruamel.yaml
import six

# Class and Objects

###########  Constant(s)  ###########

CWL_SHEBANG = "#!/usr/bin/env cwl-runner"
DEF_CWL_VERSION = 'v1.0'
CWL_TYPE = ['null', 'boolean', 'int', 'long', 'float', 'double', 'string', 'File', 'Directory']

###########  Function(s)  ###########

###########  Class(es)  ###########

class CommandLineTool(object):
    '''
    Contain all informations to describe a CWL command line tool.
    '''

    def __init__(self, tool_id=None, base_command=None, label=None, doc=None,\
                 cwl_version=DEF_CWL_VERSION, stdin=None, stderr=None, stdout=None):
        '''
        :param tool_id: unique identifier for this tool.
        :type tool_id: STRING
        :param base_command: command line for the tool.
        :type base_command: STRING
        :param label: label of this tool.
        :type label: STRING
        :param doc: documentation for the tool, usually longer than the label.
        :type doc: STRING
        :param cwl_version: version of the CWL tool.
        :type cwl_version: STRING
        :param stdin: path to a file whose contents must be piped into stdin.
        :type stdin: STRING
        :param stderr: capture stderr into the given file.
        :type stderr: STRING
        :param stdout: capture stdout into the given file.
        :type stdout: STRING
        
        Inputs (:class:`cwlgen.CommandInputParameter` objects),
        outputs (:class:`cwlgen.CommandOutputParameter` objects),
        arguments (:class:`cwlgen.CommandLineBinding` objects) 
        and requirements (:class:`cwlgen.Requirement` objects)
        are stored in lists which are initialized empty.
        '''
        self.tool_id = tool_id
        self.base_command = base_command
        self.label = label
        self.doc = doc
        self.cwl_version = cwl_version
        self.stdin = stdin
        self.stderr = stderr
        self.stdout = stdout
        self.inputs = [] # List of [CommandInputParameter] objects
        self.outputs = []    # List of [CommandOutputParameter] objects
        self.arguments = [] # List of [CommandLineBinding] objects
        self.requirements = [] # List of Several object inhereting from [Requirement]
        self.hints = []
        self.success_codes = []
        self.temporary_fail_codes = []
        self.permanent_fail_codes = []

    def export(self, outfile=None):
        '''
        Export the tool in CWL either on STDOUT or in outfile
        '''
        cwl_tool = {}
        cwl_tool['cwlVersion'] = self.cwl_version
        cwl_tool['id'] = self.tool_id
        cwl_tool['label'] = self.label
        cwl_tool['baseCommand'] = self.base_command
        cwl_tool['class'] = 'CommandLineTool'
        if self.doc is not None:
            cwl_tool['doc'] = self.doc
        # Add Inputs
        if self.inputs:
            cwl_tool['inputs'] = {}
            for in_param in self.inputs:
                cwl_tool['inputs'][in_param.id] = in_param.get_dict()

        # Add Outputs
        if self.outputs:
            cwl_tool['outputs'] = {}
            for out_param in self.outputs:
                cwl_tool['outputs'][out_param.id] = out_param.get_dict()

        # Write CWL file in YAML
        if outfile is None:
            six.print_(CWL_SHEBANG, "\n", sep='')
            six.print_(ruamel.yaml.dump(cwl_tool, Dumper=ruamel.yaml.RoundTripDumper))
        else:
            out_write = open(outfile, 'w')
            out_write.write(CWL_SHEBANG + '\n\n')
            out_write.write(ruamel.yaml.dump(cwl_tool, Dumper=ruamel.yaml.RoundTripDumper))
            out_write.close()


class Parameter(object):
    '''
    A parameter (common field of Input and Output) for a CommandLineTool
    '''

    def __init__(self, param_id, label=None, secondary_files=None, param_format=None,\
                 streamable=False, doc=None, param_type=None):
        '''
        param_id: unique identifier for this parameter [STRING]
        label: short, human-readable label [STRING]
        secondary_files: If type is a file, describes files that must be included alongside
                         the primary file(s) [STRING]
        param_format: If type is a file, uri to ontology of the format or exact format [STRING]
        streamable: If type is a file, true indicates that the file is read or written
                    sequentially without seeking [BOOLEAN]
        doc: documentation [STRING]
        param_type: type of data assigned to the parameter [STRING] corresponding to CWLType
        '''
        if not param_type in CWL_TYPE:
            print("The type is incorrect for the parameter")
            return 1
        self.id = param_id
        self.label = label
        self.secondary_files = secondary_files
        self.format = param_format
        self.streamable = streamable
        self.doc = doc
        self.type = param_type

    def get_dict(self):
        '''
        Transform the object to a [DICT] to write CWL

        :return: dictionnary of the object
        :rtype: DICT
        '''
        dict_param = {}
        if self.type:
            dict_param['type'] = self.type
        if self.doc:
            dict_param['doc'] = self.doc
        if self.label:
            dict_param['label'] = self.label
        if self.type == 'File':
            if self.format:
                dict_param['format'] = self.format
            if self.secondary_files:
                dict_param['secondaryFiles'] = self.secondary_files
            if self.streamable:
                dict_param['streamable'] = self.streamable
        return dict_param


class CommandInputParameter(Parameter):
    '''
    An input parameter for a :class:`cwlgen.CommandLineTool`.
    '''

    def __init__(self, param_id, label=None, secondary_files=None, param_format=None,\
                 streamable=False, doc=None, input_binding=None, default=None, param_type=None):
        '''
        :param param_id: unique identifier for this parameter.
        :type param_id: STRING
        :param label: short, human-readable label.
        :type label: STRING
        :param secondary_files: If type is a file, describes files that must be
                                included alongside the primary file(s).
        :type secondary_files: STRING
        :param param_format: If type is a file, uri to ontology of the format or exact format.
        :type param_format: STRING
        :param streamable: If type is a file, true indicates that the file is read or written
                           sequentially without seeking.
        :type streamable: BOOLEAN
        :param doc: documentation.
        :type doc: STRING
        :param input_binding: describes how to handle the input.
        :type input_binding: :class:`cwlgen.CommandLineBinding` object
        :param default: default value.
        :type default: STRING
        :param param_type: type of data assigned to the parameter corresponding to CWLType.
        :type param_type: STRING
        '''
        Parameter.__init__(self, param_id=param_id, label=label, \
                           secondary_files=secondary_files, param_format=param_format,\
                           streamable=streamable, doc=doc, param_type=param_type)
        self.input_binding = input_binding
        self.default = default

    def get_dict(self):
        '''
        Transform the object to a [DICT] to write CWL.

        :return: dictionnary of the object
        :rtype: DICT
        '''
        dict_in = Parameter.get_dict(self)
        if self.default:
            dict_in['default'] = self.default
        if self.input_binding:
            dict_in['inputBinding'] = self.input_binding.get_dict()
        return dict_in


class CommandOutputParameter(Parameter):
    '''
    An output parameter for a :class:`cwlgen.CommandLineTool`.
    '''

    def __init__(self, param_id, label=None, secondary_files=None, param_format=None,\
                 streamable=False, doc=None, output_binding=None, param_type=None):
        '''
        :param param_id: unique identifier for this parameter.
        :type param_id: STRING
        :param label: short, human-readable label.
        :type label: STRING
        :param secondary_files: If type is a file, describes files that must be
                                included alongside the primary file(s).
        :type secondary_files: STRING
        :param param_format: If type is a file, uri to ontology of the format or exact format.
        :type param_format: STRING
        :param streamable: If type is a file, true indicates that the file is read or written
                           sequentially without seeking.
        :type streamable: BOOLEAN
        :param doc: documentation.
        :type doc: STRING
        :param output_binding: describes how to handle the output.
        :type output_binding: :class:`cwlgen.CommandOutputBinding` object
        :param param_type: type of data assigned to the parameter corresponding to CWLType.
        :type param_type: STRING
        '''
        Parameter.__init__(self, param_id, label, secondary_files, param_format, streamable,\
                           doc, param_type)
        self.output_binding = output_binding

    def get_dict(self):
        '''
        Transform the object to a [DICT] to write CWL.

        :return: dictionnary of the object
        :rtype: DICT
        '''
        dict_out = Parameter.get_dict(self)
        if self.output_binding:
            dict_out['outputBinding'] = self.output_binding.get_dict()
        return dict_out


class CommandLineBinding(object):
    '''
    Describes how the handle an input or an argument.
    '''

    def __init__(self, load_contents=False, position=None, prefix=None, separate=False,\
                 item_separator=None, value_from=None, shell_quote=False):
        '''
        :param load_contents:
        :type load_contents: BOOLEAN
        :param position:
        :type positio: INT
        :param prefix:
        :type prefix: STRING
        :param separate:
        :type separate: BOOLEAN
        :param item_separator:
        :type item_separator: STRING
        :param value_from:
        :type value_from: STRING
        :param shell_quote:
        :type shell_quote: BOOLEAN
        '''
        self.load_contents = load_contents
        self.position = position
        self.prefix = prefix
        self.separate = separate
        self.item_separator = item_separator
        self.value_from = value_from
        self.shell_quote = shell_quote

    def get_dict(self):
        '''
        Transform the object to a [DICT] to write CWL.

        :return: dictionnary of the object
        :rtype: DICT
        '''
        dict_binding = {}
        if self.load_contents:
            # Does not take care if type: File for the moment
            dict_binding['loadContents'] = self.load_contents
        if self.position:
            dict_binding['position'] = self.position
        if self.prefix:
            dict_binding['prefix'] = self.prefix
        if self.separate:
            dict_binding['separate'] = self.separate
        if self.item_separator:
            dict_binding['itemSeparator'] = self.item_separator
        if self.value_from:
            dict_binding['valueFrom'] = self.value_from
        if self.shell_quote:
            dict_binding['shellQuote'] = self.shell_quote
        return dict_binding


class CommandOutputBinding(object):
    '''
    Describes how to generate an output parameter based on the files produced.
    '''

    def __init__(self, glob=False, load_contents=False, output_eval=None):
        '''
        :param glob: Find corresponding file(s).
        :type glob: STRING
        :param load_contents: For each file matched, read up to the 1st 64 KiB of text and
                              place it in the contents field.
        :type load_contents: BOOLEAN
        :param output_eval: Evaluate an expression to generate the output value.
        :type output_eval: STRING
        '''
        self.glob = glob
        self.load_contents = load_contents
        self.output_eval = output_eval

    def get_dict(self):
        '''
        Transform the object to a [DICT] to write CWL.

        :return: dictionnary of the object
        :rtype: DICT
        '''
        dict_binding = {}
        if self.glob:
            dict_binding['glob'] = self.glob
            if self.load_contents:
                dict_binding['loadContents'] = self.load_contents
        if self.output_eval:
            dict_binding['outputEval'] = self.output_eval
        return dict_binding


class Requirement(object):
    '''
    Requirement that must be met in order to execute the process.
    '''

    def __init__(self, req_class):
        '''
        :param req_class: requirement class.
        :type req_class: STRING
        '''
        self.req_class = req_class


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
        self.expression_lib = expression_lib


class DockerRequirement(Requirement):
    '''
    Workflow component should be run in a Docker container.
    This class specifies how to fetch or build the image.
    '''

    def __init__(self, docker_pull=None, docker_load=None, docker_file=None,\
                 docker_import=None, docker_image_id=None, docker_output_dir=None):
        '''
        :param docker_pull: image to retrive with docker pull.
        :type docker_pull: STRING
        :param docker_load: HTTP URL from which to download Docker image.
        :type docker_load: STRING
        :param docker_file: supply the contents of a Dockerfile.
        :type docker_file: STRING
        :param docker_import: HTTP URL to download and gunzip a Docker images.
        :type docker_import: STRING
        :param docker_image_id: Image id for docker run.
        :type docker_image_id: STRING
        :param docker_output_dir: designated output dir inside the Docker container.
        :type docker_output_dir: STRING
        '''
        Requirement.__init__(self, 'DockerRequirement')
        self.docker_pull = docker_pull
        self.docker_load = docker_load
        self.docker_file = docker_file
        self.docker_import = docker_import
        self.docker_image_id = docker_image_id
        self.docker_output_dir = docker_output_dir
