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
import pycwl


if __name__ == "__main__":

    ## MAIN
    # Create a tool
    cwl_tool = pycwl.CommandLineTool('pouet', 'CommandLineTool', 'pouet cest la vie', 'pouet')

    # Add 2 inputs
    input_1 = pycwl.Input('config_file', 'File', position=1, doc='config file', param_format='http://edamontology.org/format_0000')
    cwl_tool.inputs.append(input_1)
    input_2 = pycwl.Input('threads', 'int', prefix='-t', doc='number of threads')
    cwl_tool.inputs.append(input_2)

    # Add 1 output
    output_1 = pycwl.Output('result_file', 'File', glob='counts.txt', param_format='http://edamontology.org/format_1111', doc='counts of blablabla')
    cwl_tool.outputs.append(output_1)

    # Add documentation
    cwl_tool.documentation = pycwl.Documentation("Ceci est une super documentation")

    # Write both on STDOUT and a file
    cwl_tool.export()
    cwl_tool.export("example.cwl")
