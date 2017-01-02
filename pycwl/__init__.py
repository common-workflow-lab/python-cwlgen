#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.5.2+
## Creation : 12-30-2016

'''
Descrition
'''

###########  Import  ###########

# General libraries
import os
import argparse
import sys

# External libraries
import yaml

# Class and Objects

###########  Constant(s)  ###########

###########  Function(s)  ###########

###########  Class(es)  ###########

class Cwl:

    def __init__(self, tool_id, tool_class, label, base_command):
        '''
        tool_id: [STRING]
        tool_class: [STRING]
        label: [STRING]
        base_command: command line for the tool [STRING]
        '''
        self.tool_id = tool_id
        self.tool_class = tool_class
        self.label = label
        self.inputs = [] # List of Input objects
        self.outputs = []    # List of Output objects
        self.documentation = None # Documentation object
        self.base_command = base_command

    def export(self, outfile=None):
        '''
        Export the tool in CWL
        '''
        cwl_tool = {}
        cwl_tool['id'] = self.tool_id
        cwl_tool['label'] = self.label
        cwl_tool['baseCommand'] = self.base_command
        cwl_tool['class'] = self.tool_class
        if self.documentation is not None:
            cwl_tool['doc'] = self.documentation.text
        # Add Inputs
        if self.inputs:
            cwl_tool['inputs'] = {}
            for in_param in self.inputs:
                cwl_tool['inputs'][in_param.name] = {}
                cwl_tool['inputs'][in_param.name]['type'] = in_param.param_type
                if in_param.edam_format is not None:
                    cwl_tool['inputs'][in_param.name]['format'] = in_param.edam_format
                if in_param.doc is not None:
                    cwl_tool['inputs'][in_param.name]['doc'] = in_param.doc
                if in_param.position is not None:
                    cwl_tool['inputs'][in_param.name]['inputBinding'] = {}
                    cwl_tool['inputs'][in_param.name]['inputBinding']['position'] = \
                             in_param.position
                if in_param.prefix is not None:
                    cwl_tool['inputs'][in_param.name]['inputBinding'] = {}
                    cwl_tool['inputs'][in_param.name]['inputBinding']['prefix'] = \
                             in_param.prefix

        # Add Outputs
        if self.outputs:
            cwl_tool['outputs'] = {}
            for out_param in self.outputs:
                cwl_tool['outputs'][out_param.name] = {}
                cwl_tool['outputs'][out_param.name]['type'] = out_param.param_type
                if out_param.edam_format is not None:
                    cwl_tool['outputs'][out_param.name]['format'] = out_param.edam_format
                if out_param.doc is not None:
                    cwl_tool['outputs'][out_param.name]['doc'] = out_param.doc
                if out_param.glob is not None:
                    cwl_tool['outputs'][out_param.name]['outputBinding'] = {}
                    cwl_tool['outputs'][out_param.name]['outputBinding']['glob'] = \
                             out_param.glob

        # Write CWL file in YAML
        if outfile is None:
            print(yaml.dump(cwl_tool, default_flow_style=False))
        else:
            out_write = open(outfile, 'w')
            out_write.write(yaml.dump(cwl_tool, default_flow_style=False))
            out_write.close()


class Documentation:

    def __init__(self, documentation):
        '''
        documentation: documentation of the tool [STRING]
        '''
        self.text = "|" + documentation


class Parameter:

    def __init__(self, name, param_type, edam_format=None, doc=None):
        '''
        name: parameter name [STRING]
        param_type: [STRING]
        edam_format: uri of edam format [STRING]
        doc: information about the parameter [STRING]
        '''
        self.name = name
        self.param_type = param_type
        self.edam_format = edam_format
        self.doc = doc

class Input(Parameter):

    def __init__(self, name, param_type, edam_format=None, doc=None, position=None,
                 prefix=None):
        '''
        name: parameter name [STRING]
        param_type: [STRING]
        edam_format: uri of edam format [STRING]
        doc: information about the parameter [STRING]
        position: position in the command line [INT]
        prefix: prefix for the option [STRING]
        '''
        Parameter.__init__(self, name, param_type, edam_format, doc)
        self.position = position
        self.prefix = prefix


class Output(Parameter):

    def __init__(self, name, param_type, edam_format=None, doc=None, glob=None):
        '''
        name: parameter name [STRING]
        param_type: [STRING]
        edam_format: uri of edam format [STRING]
        doc: information about the parameter [STRING]
        glob: name of a file in the output directory [STRING]
        '''
        Parameter.__init__(self, name, param_type, edam_format, doc)
        self.glob = glob
