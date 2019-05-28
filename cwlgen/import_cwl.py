'''
Library to handle the manipulation and generation of CWL tool
'''

#  Import  ------------------------------

# General libraries
import os
import six
import logging

# External libraries
import ruamel.yaml as ryaml
import cwlgen

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

#  Class(es)  ------------------------------


def parse_cwl(cwl_path):
    """
    Method that parse a CWL file.

    :param cwl_path: PATH to the CWL file
    :type cwl_path: STRING
    """

    with open(cwl_path) as yaml_file:
        cwl_dict = ryaml.load(yaml_file, Loader=ryaml.Loader)
    return parse_cwl_dict(cwl_dict)


def parse_cwl_dict(cwl_dict):
    cl = cwl_dict['class']

    if cl == "CommandLineTool":
        return cwlgen.CommandLineTool.parse_dict(cwl_dict)
    elif cl == "Workflow":
        return cwlgen.Workflow.parse_dict(cwl_dict)

    return None
