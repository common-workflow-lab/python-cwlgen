#!/usr/bin/env python

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.6.0
## Creation : 12-30-2016

'''
Example of usage of the cwlgen library
'''

###########  Import  ###########

import cwlgen

if __name__ == "__main__":

    # Create a tool
    cwl_tool = cwlgen.CommandLineTool(tool_id='my_tool', label='my_tool is magic',\
                                     base_command='run_my_tool')

    # Add documentation
    cwl_tool.doc = "Magic is no magic without secrets..."

    # Add 2 inputs
    input_1_binding = cwlgen.CommandLineBinding(position=1)
    input_1 = cwlgen.CommandInputParameter('config_file', param_type='File',\
                                          input_binding=input_1_binding,\
                                          doc='config file',\
                                          param_format='http://edamontology.org/format_2330')
    cwl_tool.inputs.append(input_1)
    input_2_binding = cwlgen.CommandLineBinding(prefix='-t')
    input_2 = cwlgen.CommandInputParameter('threads', param_type='int',\
                                          input_binding=input_2_binding,\
                                          doc='number of threads')
    cwl_tool.inputs.append(input_2)

    # Add 1 output
    output_1_binding = cwlgen.CommandOutputBinding(glob='counts.txt')
    output_1 = cwlgen.CommandOutputParameter('result_file', param_type='File',\
                                            output_binding=output_1_binding,\
                                            param_format='http://edamontology.org/format_2330',\
                                            doc='magic results')
    cwl_tool.outputs.append(output_1)

    # Add Metadata
    metadata = {'name': 'my tool',
                'about': 'I let you guess',
                'publication': [{'id': 'one_doi'}, {'id': 'another_doi'}],
                'license': ['MIT']}
    cwl_tool.metadata = cwlgen.Metadata(**metadata)

    # Write in an output file
    #cwl_tool.export()
    cwl_tool.export("example.cwl")
