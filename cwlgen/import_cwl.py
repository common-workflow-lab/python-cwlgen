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
        return cwlgen.CommandLineTool()

    def _load_id(self, tool, id_el):
        """
        Load the content of id into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.CommandLineTool`
        :param id_el: Content of id
        :type id_el: STRING or [STRING]
        """
        tool.tool_id = id_el

    def _load_baseCommand(self, tool, command_el):
        """
        Load the content of baseCommand into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.CommandLineTool`
        :param command_el: Content of baseCommand
        :type command_el: STRING
        """
        tool.base_command = command_el

    def _load_label(self, tool, label_el):
        """
        Load the content of label into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.CommandLineTool`
        :param label_el: Content of label
        :type label_el: STRING
        """
        tool.label = label_el

    def _load_doc(self, tool, doc_el):
        """
        Load the content of doc into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.CommandLineTool`
        :param doc_el: Content of doc
        :type doc_el: STRING
        """
        tool.doc = doc_el

    def _load_cwlVersion(self, tool, cwl_version_el):
        """
        Load the content of cwlVersion into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.CommandLineTool`
        :param cwl_version_el: Content of cwlVersion
        :type cwl_version_el: STRING
        """
        tool.cwl_version = cwl_version_el

    def _load_stdin(self, tool, stdin_el):
        """
        Load the content of stdin into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.CommandLineTool`
        :param stdin_el: Content of stdin
        :type stdin_el: STRING
        """
        tool.stdin = stdin_el

    def _load_stderr(self, tool, stderr_el):
        """
        Load the content of stderr into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.CommandLineTool`
        :param stderr_el: Content of stderr
        :type stderr_el: STRING
        """
        tool.stderr = stderr_el

    def _load_stdout(self, tool, stdout_el):
        """
        Load the content of stdout into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.CommandLineTool`
        :param stdout_el: Content of stdout
        :type stdout_el: STRING
        """
        tool.stdout = stdout_el

    def _load_class(self, tool, class_el):
        """
        Display message to inform that cwlgen only deal with CommandLineTool for the moment.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.CommandLineTool`
        :param class_el: Content of class
        :type class_el: STRING
        """
        if class_el != 'CommandLineTool':
            logger.warning('cwlgen library only handle CommandLineTool for the moment')

    def _load_inputs(self, tool, inputs_el):
        """
        Load the content of inputs into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.CommandLineTool`
        :param inputs_el: Content of inputs
        :type inputs_el: LIST or DICT
        """
        inp_parser = InputsParser()
        inp_parser.load_inputs(tool.inputs, inputs_el)

    def _load_outputs(self, tool, outputs_el):
        """
        Load the content of inputs into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.CommandLineTool`
        :param outputs_el: Content of outputs
        :type outputs_el: LIST or DICT
        """
        inp_parser = OutputsParser()
        inp_parser.load_outputs(tool.outputs, outputs_el)

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
            except AttributeError:
                logger.warning(key + " content is not processed (yet).")
        return tool


class InputsParser(object):
    """
    Class to parse content of inputs from an existing CWL Tool.
    """

    def load_inputs(self, inputs, inputs_el):
        """
        Load the content of inputs into the inputs list.

        :param inputs: list to store inputs
        :type inputs: LIST
        :param inputs_el: Content of inputs
        :type inputs_el: LIST or DICT
        """
        # For the moment, only deal with the format exported by cwlgen
        for key, value in inputs_el.items():
            input_obj = cwlgen.CommandInputParameter(key)
            inputs.append(input_obj)


class OutputsParser(object):
    """
    Class to parse content of outputs from an existing CWL Tool.
    """

    def load_outputs(self, outputs, outputs_el):
        """
        Load the content of outputs into the outputs list.

        :param outputs: list to store outputs
        :type outputs: LIST
        :param outputs_el: Content of outputs
        :type outputs_el: LIST or DICT
        """
        # For the moment, only deal with the format exported by cwlgen
        for key, value in outputs_el.items():
            output_obj = cwlgen.CommandOutputParameter(key)
            outputs.append(output_obj)
