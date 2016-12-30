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
         self.inputs = [] # List of Function objects
         self.outputs = []    # List of Topic objects
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
        if outfile is None:
            print(yaml.dump(cwl_tool, default_flow_style=False))

class Documentation:

    def __init__(self, documentation):
        '''
        documentation: documentation of the tool [STRING]
        '''
        self.text = documentation # [STRING]


class Parameter:

    def __init__(self, name, param_type, edam_format=None, doc=None):
        '''
        name: parameter name [STRING]
        param_type: [STRING]
        edam_format: uri of edam format [STRING]
        doc: information about the parameter [STRING]
        '''
        self.name = name
        self.param_type = Data_type(data_type) # Data_type object
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
