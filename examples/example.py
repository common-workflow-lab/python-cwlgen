#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.6.0
## Creation : 12-30-2016

'''
Example of usage of the pycwl library
'''

###########  Import  ###########

# General libraries
import os
import argparse
import sys

# External libraries
import pycwl


if __name__ == "__main__":

    ## MAIN
    # Create a tool
    cwl_tool = pycwl.CommandLineTool(tool_id='my_tool', label='my_tool is magic', base_command='run_my_tool')

    # Add documentation
    cwl_tool.doc = "Magic is no magic without secrets..."

    # Add 2 inputs
    input_1_binding = pycwl.CommandLineBinding(position=1)
    input_1 = pycwl.CommandInputParameter('config_file', param_type='File', input_binding=input_1_binding, doc='config file', param_format='http://edamontology.org/format_2330')
    cwl_tool.inputs.append(input_1)
    input_2_binding = pycwl.CommandLineBinding(prefix='-t')
    input_2 = pycwl.CommandInputParameter('threads', param_type='int', input_binding=input_2_binding, doc='number of threads')
    cwl_tool.inputs.append(input_2)

    # Add 1 output
    output_1_binding = pycwl.CommandOutputBinding(glob='counts.txt')
    output_1 = pycwl.CommandOutputParameter('result_file', param_type='File', output_binding=output_1_binding, param_format='http://edamontology.org/format_2330', doc='magic results')
    cwl_tool.outputs.append(output_1)

    # Write in an output file
    #cwl_tool.export()
    cwl_tool.export("example.cwl")
