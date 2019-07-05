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
    Method that parses a CWL file and will a
    :class:`cwlgen.Workflow` or :class:`cwlgen.CommandLineTool`.
    Note: this will not import additional files.

    :param cwl_path: PATH to the CWL file
    :type cwl_path: str
    :return: :class:`cwlgen.Workflow` | :class:`cwlgen.CommandLineTool`
    """

    with open(cwl_path) as yaml_file:
        cwl_dict = ryaml.load(yaml_file, Loader=ryaml.Loader)
    return parse_cwl_dict(cwl_dict)


def parse_cwl_dict(cwl_dict):
    """
    Method that parses a dictionary and will return a
    :class:`cwlgen.Workflow` or :class:`cwlgen.CommandLineTool`.

    :param cwl_dict: The dictionary to pass, must contain a 'class' field.
    :type cwl_dict: :class:`dict`
    :return: :class:`cwlgen.Workflow` | :class:`cwlgen.CommandLineTool`
    """
    cl = cwl_dict.get("class")

    if cl == "CommandLineTool":
        return cwlgen.CommandLineTool.parse_dict(cwl_dict)
    elif cl == "Workflow":
        return cwlgen.Workflow.parse_dict(cwl_dict)

    raise NotImplementedError("The CWL class '" + str(cl) + "' was not a recognised CWL class")
