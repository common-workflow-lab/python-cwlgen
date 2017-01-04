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
    cwl_tool = pycwl.CommandLineTool('my_tool', 'CommandLineTool', 'my_tool is magic', 'run_my_tool')

    # Add documentation
    cwl_tool.doc = "Magic is no magic without secrets..."

    # Add 2 inputs
    input_1 = pycwl.Input('config_file', 'File', position=1, doc='config file', param_format='http://edamontology.org/format_2330')
    cwl_tool.inputs.append(input_1)
    input_2 = pycwl.Input('threads', 'int', prefix='-t', doc='number of threads')
    cwl_tool.inputs.append(input_2)

    # Add 1 output
    output_1 = pycwl.Output('result_file', 'File', glob='counts.txt', param_format='http://edamontology.org/format_2330', doc='magic results')
    cwl_tool.outputs.append(output_1)

    # Write in an output file
    #cwl_tool.export()
    cwl_tool.export("example.cwl")
