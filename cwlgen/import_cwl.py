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
import cwlgen.workflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#  Class(es)  ------------------------------

def parse_cwl(cwl_path):
    with open(cwl_path) as yaml_file:
        cwl_dict = ryaml.load(yaml_file, Loader=ryaml.Loader)
        cl = cwl_dict['class']

    if cl == "CommandLineTool":
        p = CWLToolParser()
        return p.import_cwl(cwl_path)
    if cl == "Workflow":
        p = CWLToolParser()
        return p.import_cwl(cwl_path)
    return None

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
        tool.id = id_el

    def _load_requirements(self, tool, req_el):
        pass

    def _load_hints(self, tool, req_el):
        pass

    def _load_baseCommand(self, tool, command_el):
        """
        Load the content of baseCommand into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.CommandLineTool`
        :param command_el: Content of baseCommand
        :type command_el: STRING
        """
        tool.baseCommand = command_el

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
        tool.cwlVersion = cwl_version_el

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
        for key, element in cwl_dict.items():
            try:
                getattr(self, '_load_{}'.format(key))(tool, element)
            except AttributeError:
                logger.warning(key + " content is not processed (yet).")
        return tool

def dict_or_idlist_items(v):
    if isinstance(v, dict):
        return v.items()
    o = []
    for i in v:
        e = dict(i)
        del e['id']
        o.append( (i['id'], e) )
    return o

class InputsParser(object):
    """
    Class to parse content of inputs from an existing CWL Tool.
    """

    def _load_label(self, input_obj, label_el):
        """
        Load the content of type into the input object.

        :param input_obj: input obj
        :type input_obj: : :class:`cwlgen.CommandInputParameter`
        :param label_el: Content of label
        :type label_el: STRING
        """
        input_obj.label = label_el

    def _load_secondaryFiles(self, input_obj, secfile_el):
        """
        Load the content of secondaryFiles into the input object.

        :param input_obj: input obj
        :type input_obj: : :class:`cwlgen.CommandInputParameter`
        :param secfile_el: Content of secondaryFile
        :type secfile_el: STRING
        """
        input_obj.secondaryFile = secfile_el

    def _load_format(self, input_obj, format_el):
        """
        Load the content of format into the input object.

        :param input_obj: input obj
        :type input_obj: : :class:`cwlgen.CommandInputParameter`
        :param format_el: Content of format
        :type format_el: STRING
        """
        input_obj.format = format_el

    def _load_streamable(self, input_obj, stream_el):
        """
        Load the content of streamable into the input object.

        :param input_obj: input obj
        :type input_obj: : :class:`cwlgen.CommandInputParameter`
        :param stream_el: Content of streamable
        :type type_el: BOOLEAN
        """
        input_obj.streamable = stream_el

    def _load_doc(self, input_obj, doc_el):
        """
        Load the content of doc into the input object.

        :param input_obj: input obj
        :type input_obj: : :class:`cwlgen.CommandInputParameter`
        :param doc_el: Content of doc
        :type doc_el: STRING
        """
        input_obj.doc = doc_el

    def _load_inputBinding(self, input_obj, inpb_el):
        """
        Load the content of inputBinding into the input object.

        :param input_obj: input obj
        :type input_obj: : :class:`cwlgen.CommandInputParameter`
        :param inpb_el: Content of inputBinding
        :type inpb_el: DICT
        """
        ibparser = InputBindingParser()
        ibparser.load_inbinding(input_obj, inpb_el)

    def _load_default(self, input_obj, def_el):
        """
        Load the content of default into the input object.

        :param input_obj: input obj
        :type input_obj: : :class:`cwlgen.CommandInputParameter`
        :param default_el: Content of default
        :type default_el: STRING
        """
        input_obj.default = def_el

    def _load_type(self, input_obj, type_el):
        """
        Load the content of type into the input object.

        :param input_obj: input obj
        :type input_obj: : :class:`cwlgen.CommandInputParameter`
        :param type_el: Content of type
        :type type_el: STRING
        """
        input_obj.type = type_el

    def load_inputs(self, inputs, inputs_el):
        """
        Load the content of inputs into the inputs list.

        :param inputs: list to store inputs
        :type inputs: LIST
        :param inputs_el: Content of inputs
        :type inputs_el: LIST or DICT
        """
        # For the moment, only deal with the format exported by cwlgen
        for key, value in dict_or_idlist_items(inputs_el):
            input_obj = cwlgen.CommandInputParameter(key)
            for key, element in value.items():
                try:
                    getattr(self, '_load_{}'.format(key))(input_obj, element)
                except AttributeError:
                    logger.warning(key + " content for input is not processed (yet).")
            inputs.append(input_obj)


class InputBindingParser(object):
    """
    Class to parse content of inputBinding of input from existing CWL Tool.
    """

    def _load_loadContents(self, inbinding_obj, loadcontents_el):
        """
        Load the content of loadContents into the inputBinding object.

        :param inbinding_obj: input_binding object
        :loadContents inbinding_obj: : :class:`cwlgen.CommandLineBinding`
        :param loadcontents_el: Content of loadContents
        :loadContents loadcontents_el: BOOLEAN
        """
        inbinding_obj.loadContents = loadcontents_el

    def _load_position(self, inbinding_obj, position_el):
        """
        Load the content of position into the inputBinding object.

        :param inbinding_obj: input_binding object
        :loadContents inbinding_obj: : :class:`cwlgen.CommandLineBinding`
        :param position_el: Content of loadContents
        :loadContents position_el: INT
        """
        inbinding_obj.position = position_el

    def _load_prefix(self, inbinding_obj, prefix_el):
        """
        Load the content of prefix into the inputBinding object.

        :param inbinding_obj: input_binding object
        :loadContents inbinding_obj: : :class:`cwlgen.CommandLineBinding`
        :param prefix_el: Content of loadContents
        :loadContents prefix_el: STRING
        """
        inbinding_obj.prefix = prefix_el

    def _load_separate(self, inbinding_obj, separate_el):
        """
        Load the content of separate into the inputBinding object.

        :param inbinding_obj: input_binding object
        :loadContents inbinding_obj: : :class:`cwlgen.CommandLineBinding`
        :param separate_el: Content of loadContents
        :loadContents separate_el: BOOLEAN
        """
        inbinding_obj.separate = separate_el

    def _load_itemSeparator(self, inbinding_obj, itemsep_el):
        """
        Load the content of itemSeparator into the inputBinding object.

        :param inbinding_obj: input_binding object
        :loadContents inbinding_obj: : :class:`cwlgen.CommandLineBinding`
        :param itemsep_el: Content of loadContents
        :loadContents itemsep_el: STRING
        """
        inbinding_obj.itemSeparator = itemsep_el

    def _load_valueFrom(self, inbinding_obj, valuefrom_el):
        """
        Load the content of valueFrom into the inputBinding object.

        :param inbinding_obj: input_binding object
        :loadContents inbinding_obj: : :class:`cwlgen.CommandLineBinding`
        :param valuefrom_el: Content of loadContents
        :loadContents valuefrom_el: STRING
        """
        inbinding_obj.valueFrom = valuefrom_el

    def _load_shellQuote(self, inbinding_obj, shellquote_el):
        """
        Load the content of shellQuote into the inputBinding object.

        :param inbinding_obj: input_binding object
        :loadContents inbinding_obj: : :class:`cwlgen.CommandLineBinding`
        :param shellquote_el: Content of loadContents
        :loadContents shellquote_el: BOOLEAN
        """
        inbinding_obj.shellQuote = shellquote_el

    def load_inbinding(self, input_obj, inbinding_el):
        """
        Load the content of inputBinding into the input object.

        :param input_obj: input object
        :type input_obj: :class:`cwlgen.CommandInputParameter`
        :param inbinding_el: Content of inputs
        :type inbinding_el: DICT
        """
        inbinding_obj = cwlgen.CommandLineBinding()
        for key, value in inbinding_el.items():
            try:
                getattr(self, '_load_{}'.format(key))(inbinding_obj, value)
            except AttributeError:
                logger.warning(key + " content for inputBinding is not processed (yet).")
            input_obj.inputBinding = inbinding_obj


class OutputsParser(object):
    """
    Class to parse content of outputs from an existing CWL Tool.
    """

    def _load_label(self, output_obj, label_el):
        """
        Load the content of type into the output object.

        :param output_obj: output obj
        :type output_obj: : :class:`cwlgen.CommandInputParameter`
        :param label_el: Content of label
        :type label_el: STRING
        """
        output_obj.label = label_el

    def _load_secondaryFiles(self, output_obj, secfile_el):
        """
        Load the content of secondaryFiles into the output object.

        :param output_obj: output obj
        :type output_obj: : :class:`cwlgen.CommandInputParameter`
        :param secfile_el: Content of secondaryFile
        :type secfile_el: STRING
        """
        output_obj.secondaryFile = secfile_el

    def _load_format(self, output_obj, format_el):
        """
        Load the content of format into the output object.

        :param output_obj: output obj
        :type output_obj: : :class:`cwlgen.CommandInputParameter`
        :param format_el: Content of format
        :type format_el: STRING
        """
        output_obj.format = format_el

    def _load_streamable(self, output_obj, stream_el):
        """
        Load the content of streamable into the output object.

        :param output_obj: output obj
        :type output_obj: : :class:`cwlgen.CommandInputParameter`
        :param stream_el: Content of streamable
        :type type_el: BOOLEAN
        """
        output_obj.streamable = stream_el

    def _load_doc(self, output_obj, doc_el):
        """
        Load the content of doc into the output object.

        :param output_obj: output obj
        :type output_obj: : :class:`cwlgen.CommandInputParameter`
        :param doc_el: Content of doc
        :type doc_el: STRING
        """
        output_obj.doc = doc_el

    def _load_outputBinding(self, output_obj, outpb_el):
        """
        Load the content of outputBinding into the output object.

        :param output_obj: output obj
        :type output_obj: : :class:`cwlgen.CommandOutputParameter`
        :param outpb_el: Content of outputBinding
        :type outpb_el: DICT
        """
        obparser = OutputBindingParser()
        obparser.load_outbinding(output_obj, outpb_el)

    def _load_type(self, output_obj, type_el):
        """
        Load the content of type into the output object.

        :param output_obj: output obj
        :type output_obj: : :class:`cwlgen.CommandInputParameter`
        :param type_el: Content of type
        :type type_el: STRING
        """
        output_obj.type = type_el

    def _load_outputSource(self, output_obj, type_el):
        """
        Load the content of type into the output object.

        :param output_obj: output obj
        :type output_obj: : :class:`cwlgen.CommandInputParameter`
        :param type_el: Content of type
        :type type_el: STRING
        """
        output_obj.outputSource = type_el

    def load_outputs(self, outputs, outputs_el):
        """
        Load the content of outputs into the outputs list.

        :param outputs: list to store outputs
        :type outputs: LIST
        :param outputs_el: Content of outputs
        :type outputs_el: LIST or DICT
        """
        # For the moment, only deal with the format exported by cwlgen
        for key, value in dict_or_idlist_items(outputs_el):
            output_obj = cwlgen.CommandOutputParameter(key)
            for key, element in value.items():
                try:
                    getattr(self, '_load_{}'.format(key))(output_obj, element)
                except AttributeError:
                    logger.warning(key + " content for output is not processed (yet).")
            outputs.append(output_obj)


class OutputBindingParser(object):
    """
    Class to parse content of outputBinding of output from existing CWL Tool.
    """

    def _load_glob(self, outbinding_obj, glob_el):
        """
        Load the content of glob into the outputBinding object.

        :param outbinding_obj: outputBinding object
        :glob outbinding_obj: : :class:`cwlgen.CommandOutputBinding`
        :param glob_el: Content of glob
        :glob glob_el: STRING
        """
        outbinding_obj.glob = glob_el

    def _load_loadContents(self, outbinding_obj, loadcontents_el):
        """
        Load the content of loadContents into the outputBinding object.

        :param outbinding_obj: outputBinding object
        :loadContents outbinding_obj: : :class:`cwlgen.CommandOutputBinding`
        :param loadcontents_el: Content of loadContents
        :loadContents loadcontents_el: BOOLEAN
        """
        outbinding_obj.loadContents = loadcontents_el

    def _load_outputEval(self, outbinding_obj, outputeval_el):
        """
        Load the content of outputEval into the outputBinding object.

        :param outbinding_obj: outputBinding object
        :outputEval outbinding_obj: : :class:`cwlgen.CommandOutputBinding`
        :param outputeval_el: Content of outputEval
        :outputEval outputeval_el: STRING
        """
        outbinding_obj.outputEval = outputeval_el

    def load_outbinding(self, output_obj, outbinding_el):
        """
        Load the content of outputBinding into the output object.

        :param output_obj: output object
        :type output_obj: :class:`cwlgen.CommandOutputParameter`
        :param outbinding_el: Content of outputBinding element
        :type outbinding_el: DICT
        """
        outbinding_obj = cwlgen.CommandOutputBinding()
        for key, value in outbinding_el.items():
            try:
                getattr(self, '_load_{}'.format(key))(outbinding_obj, value)
            except AttributeError:
                logger.warning(key + " content for outputBinding is not processed (yet).")
            output_obj.outputBinding = outbinding_obj


class StepsParser(object):
    """
    Class to parse content of steps of workflow from existing CWL Workflow.
    """
    def __init__(self, basedir=None):
        self.basedir = basedir

    def _load_in(self, step_obj, in_el):
        for key, val in in_el.items():
            o = cwlgen.workflow.WorkflowStepInput(key)
            if isinstance(val, dict) and 'default' in val:
                o.default = val['default']
            else:
                o.src = val
            step_obj.inputs.append(o)

    def _load_out(self, step_obj, in_el):
        for val in in_el:
            o = cwlgen.workflow.WorkflowStepOutput(val)
            step_obj.outputs.append(o)

    def _load_run(self, step_obj, in_el):
        if isinstance(in_el, basestring):
            path = os.path.join(self.basedir, in_el)
            #logger.info("Parsing: %s", path)
            step_obj.run = parse_cwl(path)


    def load_steps(self, steps_obj, steps_elm):
        """
        Load the content of step into the output object.

        :param output_obj: output object
        :type output_obj: :class:`cwlgen.CommandOutputParameter`
        :param outbinding_el: Content of outputBinding element
        :type outbinding_el: DICT
        """
        for key, value in steps_elm.items():
            step_obj = cwlgen.workflow.WorkflowStep(key)
            for key, element in value.items():
                try:
                    getattr(self, '_load_{}'.format(key))(step_obj, element)
                except AttributeError:
                    logger.warning(key + " content for input is not processed (yet).")
            steps_obj.append(step_obj)


class CWLWorkflowParser(object):

    def __init__(self, basedir=None):
        self.basedir = basedir

    def _init_workflow(self, cwl_dict):
        """
        Init tool from existing CWL tool.

        :param cwl_dict: Full content of CWL file
        :type cwl_dict: DICT
        """
        return cwlgen.workflow.Workflow()

    def import_cwl(self, cwl_path):
        """
        Load content of cwl into the :class:`cwlgen.workflow.Workflow` object.

        :param cwl_path: Path of the CWL tool to be loaded.
        :type cwl_path: STRING
        :return: CWL tool content in cwlgen model.
        :rtype: :class:`cwlgen.workflow.Workflow`
        """
        with open(cwl_path) as yaml_file:
            cwl_dict = ryaml.load(yaml_file, Loader=ryaml.Loader)
        tool = self._init_workflow(cwl_dict)
        self.basedir = os.path.dirname(cwl_path)
        for key, element in cwl_dict.items():
            try:
                getattr(self, '_load_{}'.format(key))(tool, element)
            except AttributeError:
                logger.warning(key + " workflow content is not processed (yet).")
        return tool

    def _load_id(self, tool, id_el):
        """
        Load the content of id into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.CommandLineTool`
        :param id_el: Content of id
        :type id_el: STRING or [STRING]
        """
        tool.id = id_el

    def _load_cwlVersion(self, tool, cwl_version_el):
        """
        Load the content of cwlVersion into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.workflow.Workflow`
        :param cwl_version_el: Content of cwlVersion
        :type cwl_version_el: STRING
        """
        tool.cwlVersion = cwl_version_el


    def _load_class(self, tool, class_el):
        """
        Display message to inform that cwlgen only deal with Workflow for the moment.

        :param tool: Workflow object from cwlgen
        :type tool: :class:`cwlgen.workflow.Workflow`
        :param class_el: Content of class
        :type class_el: STRING
        """
        if class_el != 'Workflow':
            logger.warning('cwlgen library only handle Workflow for the moment')

    def _load_requirements(self, tool, req_el):
        pass

    def _load_inputs(self, tool, inputs_el):
        """
        Load the content of inputs into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.workflow.Workflow`
        :param inputs_el: Content of inputs
        :type inputs_el: LIST or DICT
        """
        inp_parser = InputsParser()
        inp_parser.load_inputs(tool.inputs, inputs_el)

    def _load_outputs(self, tool, outputs_el):
        """
        Load the content of inputs into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.workflow.Workflow`
        :param outputs_el: Content of outputs
        :type outputs_el: LIST or DICT
        """
        inp_parser = OutputsParser()
        inp_parser.load_outputs(tool.outputs, outputs_el)


    def _load_steps(self, tool, outputs_el):
        """
        Load the content of inputs into the tool.

        :param tool: Tool object from cwlgen
        :type tool: :class:`cwlgen.workflow.Workflow`
        :param outputs_el: Content of outputs
        :type outputs_el: LIST or DICT
        """
        inp_parser = StepsParser(self.basedir)
        inp_parser.load_steps(tool.steps, outputs_el)
