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

# Class and Objects

###########  Constant(s)  ###########

###########  Function(s)  ###########

###########  Class(es)  ###########

class CommandLineTool(object):
    '''
    Contain all informations to describe a CWL command line tool
    '''

    def __init__(self, tool_id, label, base_command, doc=None):
        '''
        tool_id: [STRING]
        tool_class: [STRING]
        label: [STRING]
        base_command: command line for the tool [STRING]
        '''
        self.tool_id = tool_id
        self.label = label
        self.doc = doc
        self.inputs = [] # List of Input objects
        self.outputs = []    # List of Output objects
        self.base_command = base_command

    def export(self, outfile=None):
        '''
        Export the tool in CWL
        '''
        cwl_tool = {}
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
                cwl_tool['inputs'][in_param.id] = in_param.getdict_cwl()

        # Add Outputs
        if self.outputs:
            cwl_tool['outputs'] = {}
            for out_param in self.outputs:
                cwl_tool['outputs'][out_param.id] = out_param.getdict_cwl()

        # Write CWL file in YAML
        if outfile is None:
            print(ruamel.yaml.dump(cwl_tool, Dumper=ruamel.yaml.RoundTripDumper))
        else:
            out_write = open(outfile, 'w')
            out_write.write(ruamel.yaml.dump(cwl_tool, Dumper=ruamel.yaml.RoundTripDumper))
            out_write.close()


class Parameter(object):
    '''
    Common fields for input and output parameters for a CommandLineTool
    '''

    def __init__(self, param_id, param_type, label=None, doc=None, param_format=None,\
                 streamable=False, secondary_files=None):
        '''
        param_id: unique identifier for this parameter [STRING]
        param_type: type of datai assigned to the parameter [STRING]
        label: short, human-readable label [STRING]
        doc: documentation [STRING]
        param_format: If type is a file, uri to ontology of the format or exact format [STRING]
        streamable: If type is a file, true indicates that the file is read or written
                    sequentially without seeking [BOOLEAN]
        secondary_files: If type is a file, describes files that must be included alongside
                         the primary file(s) [STRING]
        '''
        self.id = param_id
        self.type = param_type
        self.label = label
        self.doc = doc
        self.format = param_format
        self.streamable = streamable
        self.secondary_files = secondary_files

    def getdict_cwl(self):
        '''
        Transform the object to a [DICT] for CWL
        '''
        dict_cwl = {}
        dict_cwl['type'] = self.type
        if self.doc:
            dict_cwl['doc'] = self.doc
        if self.label:
            dict_cwl['label'] = self.label
        if self.type == 'File':
            if self.format:
                dict_cwl['format'] = self.format
            if self.streamable:
                dict_cwl['streamable'] = self.streamable
            if self.secondary_files:
                dict_cwl['secondaryFiles'] = self.secondary_files
        return dict_cwl

class Input(Parameter):
    '''
    An input parameter for a CommandLineTool
    '''

    def __init__(self, param_id, param_type, label=None, doc=None, param_format=None,\
                 streamable=False, secondary_files=None, position=None, prefix=None,\
                 separate=True, item_separator=None, value_from=None, shell_quote=False,\
                 load_contents=False):
        '''
        param_id: unique identifier for this parameter [STRING]
        param_type: type of datai assigned to the parameter [STRING]
        label: short, human-readable label [STRING]
        doc: documentation [STRING]
        param_format: If type is a file, uri to ontology of the format or exact format [STRING]
        streamable: If type is a file, true indicates that the file is read or written
                    sequentially without seeking [BOOLEAN]
        secondary_files: If type is a file, describes files that must be included alongside
                         the primary file(s) [STRING]
        position: sorting key [INT]
        prefix: command line prefix before the value [STRING]
        separate: if true, prefix and value are separated [BOOLEAN]
        item_separator: join elements into single string with the separator [STRING]
        value_from: [STRING]
        shell_quote: [BOOLEAN]
        load_contents: [BOOLEAN]
        '''
        Parameter.__init__(self, param_id, param_type, label, doc, param_format, streamable,\
                           secondary_files)
        self.position = position
        self.prefix = prefix
        self.separate = separate
        self.item_separator = item_separator
        self.value_from = value_from
        self.shell_quote = shell_quote
        self.load_contents = load_contents

    def getdict_cwl(self):
        '''
        Transform the object to a [DICT] for CWL
        '''
        dict_cwl = Parameter.getdict_cwl(self)
        dict_cwl['inputBinding'] = {}
        if self.position:
            dict_cwl['inputBinding']['position'] = self.position
        elif self.prefix:
            dict_cwl['inputBinding']['prefix'] = self.prefix
        if not dict_cwl['inputBinding']:
            del dict_cwl['inputBinding']
        return dict_cwl

class Output(Parameter):
    '''
    An output parameter for a CommandLineTool
    '''

    def __init__(self, param_id, param_type, label=None, doc=None, param_format=None,\
                 streamable=False, secondary_files=None, glob=None, output_eval=None,\
                 load_contents=False):
        '''
        param_id: unique identifier for this parameter [STRING]
        param_type: type of datai assigned to the parameter [STRING]
        label: short, human-readable label [STRING]
        doc: documentation [STRING]
        param_format: If type is a file, uri to ontology of the format or exact format [STRING]
        streamable: If type is a file, true indicates that the file is read or written
                    sequentially without seeking [BOOLEAN]
        secondary_files: If type is a file, describes files that must be included alongside
                         the primary file(s) [STRING]
        glob: Find files relative to output directory [STRING]
        output_eval: [STRING]
        load_contents: [BOOLEAN]
        '''
        Parameter.__init__(self, param_id, param_type, label, doc, param_format, streamable,\
                           secondary_files)
        self.glob = glob
        self.output_eval = output_eval
        self.load_contents = load_contents

    def getdict_cwl(self):
        '''
        Transform the object to a [DICT] for CWL
        '''
        dict_cwl = Parameter.getdict_cwl(self)
        if self.glob:
            dict_cwl['outputBinding'] = {}
            dict_cwl['outputBinding']['glob'] = self.glob
        return dict_cwl
