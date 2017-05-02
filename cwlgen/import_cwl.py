'''
Library to handle the manipulation and generation of CWL tool
'''

#  Import  ------------------------------

# General libraries
import os
import argparse
import sys
import logging

# External libraries
import ruamel.yaml as ryaml
import six
import cwlgen

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#  Class(es)  ------------------------------ 

class CWLToolParser(object):
    """
    Class to import content from an existing CWL Tool.
    """

    def _init_tool(self, cwl_dict):
        """
        Init tool from existing CWL tool.
    
        :param cwl_dict: Full content of CWL file
        :type cwl_dict: DICT
        """
        tool = cwlgen.CommandLineTool(tool_id=cwl_dict.get('id', None),
                                      base_command=cwl_dict.get('baseCommand', None),
                                      label=cwl_dict.get('label', None),
                                      doc=cwl_dict.get('doc', None),
                                      cwl_version=cwl_dict.get('cwlVersion', None),
                                      stdin=cwl_dict.get('stdin', None),
                                      stderr=cwl_dict.get('stderr', None),
                                      stdout=cwl_dict.get('stdout', None))
        return tool

    def import_cwl(self, cwl_path):
        """
        Load content of cwl into the :class:`cwlgen.CommandLineTool` object.
    
        :param cwl_path: Path of the CWL tool to be loaded.
        :type cwl_path: STRING
        :return: CWL tool content in cwlgen model.
        :rtype: :class:`cwlgen.CommandLineTool`
        """
        with open(cwl_path) as yaml_file:
            cwl_dict = ryaml.load(yaml_file, Loader=ryaml.Loader)
        tool = self._init_tool(cwl_dict)
        for key in cwl_dict.keys():
            try:
                getattr(self, '_load_{}'.format(key))(tool, cwl_dict[key]) 
            except:
                logger.warning(key + " is not processed.")
        return tool
