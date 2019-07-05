import logging

# External libraries
import ruamel.yaml

from cwlgen.commandlinebinding import CommandLineBinding
from .common import CWL_VERSIONS, DEF_VERSION, CWL_SHEBANG, Namespaces, Parameter
from .requirements import *
from .utils import literal, literal_presenter, Serializable

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

#  Function(s)  ------------------------------

#  Class(es)  ------------------------------


class CommandOutputBinding(Serializable):
    """
    Describes how to generate an output parameter based on the files produced.
    """

    def __init__(self, glob=None, load_contents=None, output_eval=None):
        """
        :param glob: Find corresponding file(s)
        :type glob: STRING
        :param load_contents: For each file matched, read up to the 1st 64 KiB of text and
                              place it in the contents field
        :type load_contents: BOOLEAN
        :param output_eval: Evaluate an expression to generate the output value
        :type output_eval: STRING
        """
        self.glob = glob
        self.loadContents = load_contents
        self.outputEval = output_eval


class CommandInputParameter(Parameter):
    """
    An input parameter for a :class:`cwlgen.CommandLineTool`.
    """

    parse_types = {"inputBinding": [CommandLineBinding]}

    def __init__(
        self,
        param_id,
        label=None,
        secondary_files=None,
        param_format=None,
        streamable=None,
        doc=None,
        input_binding=None,
        default=None,
        param_type=None,
    ):
        """
        :param param_id: unique identifier for this parameter
        :type param_id: STRING
        :param label: short, human-readable label
        :type label: STRING
        :param secondary_files: If type is a file, describes files that must be
                                included alongside the primary file(s)
        :type secondary_files: STRING
        :param param_format: If type is a file, uri to ontology of the format or exact format.
        :type param_format: STRING
        :param streamable: If type is a file, true indicates that the file is read or written
                           sequentially without seeking
        :type streamable: BOOLEAN
        :param doc: documentation
        :type doc: STRING
        :param input_binding: describes how to handle the input
        :type input_binding: :class:`cwlgen.CommandLineBinding` object
        :param default: default value
        :type default: STRING
        :param param_type: type of data assigned to the parameter corresponding to CWLType
        :type param_type: STRING
        """
        Parameter.__init__(
            self,
            param_id=param_id,
            label=label,
            secondary_files=secondary_files,
            param_format=param_format,
            streamable=streamable,
            doc=doc,
            param_type=param_type,
        )
        self.inputBinding = input_binding
        self.default = default


class CommandOutputParameter(Parameter):
    """
    An output parameter for a :class:`cwlgen.CommandLineTool`.
    """

    parse_types = {"outputBinding": [CommandOutputBinding]}

    def __init__(
        self,
        param_id,
        label=None,
        secondary_files=None,
        param_format=None,
        streamable=None,
        doc=None,
        output_binding=None,
        param_type=None,
    ):
        """
        :param param_id: unique identifier for this parameter
        :type param_id: STRING
        :param label: short, human-readable label
        :type label: STRING
        :param secondary_files: If type is a file, describes files that must be
                                included alongside the primary file(s)
        :type secondary_files: STRING
        :param param_format: If type is a file, uri to ontology of the format or exact format
        :type param_format: STRING
        :param streamable: If type is a file, true indicates that the file is read or written
                           sequentially without seeking
        :type streamable: BOOLEAN
        :param doc: documentation
        :type doc: STRING
        :param output_binding: describes how to handle the output
        :type output_binding: :class:`cwlgen.CommandOutputBinding` object
        :param param_type: type of data assigned to the parameter corresponding to CWLType
        :type param_type: STRING
        """
        Parameter.__init__(
            self,
            param_id,
            label,
            secondary_files,
            param_format,
            streamable,
            doc,
            param_type,
        )
        self.outputBinding = output_binding


class CommandLineTool(Serializable):
    """
    Contain all informations to describe a CWL command line tool.
    """

    __CLASS__ = "CommandLineTool"

    parse_types = {'inputs': [[CommandInputParameter]], "outputs": [[CommandOutputParameter]]}
    ignore_fields_on_parse = ["namespaces", "class"]
    ignore_fields_on_convert = ["namespaces", "class", "metadata", "requirements"]

    def __init__(
        self,
        tool_id=None,
        base_command=None,
        label=None,
        doc=None,
        cwl_version=None,
        stdin=None,
        stderr=None,
        stdout=None,
        path=None
    ):
        """
        :param tool_id: Unique identifier for this tool
        :type tool_id: str
        :param base_command: command line for the tool
        :type base_command: str | list[STRING]
        :param label: label of this tool
        :type label: str
        :param doc: documentation for the tool, usually longer than the label
        :type doc: str
        :param cwl_version: version of the CWL tool
        :type cwl_version: str
        :param stdin: path to a file whose contents must be piped into stdin
        :type stdin: str
        :param stderr: capture stderr into the given file
        :type stderr: str
        :param stdout: capture stdout into the given file
        :type stdout: str

        inputs (:class:`cwlgen.CommandInputParameter` objects),
        outputs (:class:`cwlgen.CommandOutputParameter` objects),
        arguments (:class:`cwlgen.CommandLineBinding` objects),
        hints (any | :class:`cwlgen.Requirement` objects)
        and requirements (:class:`cwlgen.Requirement` objects)
        are stored in lists which are initialized empty.
        """
        if cwl_version not in CWL_VERSIONS:
            _LOGGER.warning(
                "CWL version {} is not recognized as a valid version.".format(
                    cwl_version
                )
            )
            _LOGGER.warning("CWL version is set up to {}.".format(DEF_VERSION))
            cwl_version = DEF_VERSION
        self.cwlVersion = cwl_version
        self.id = tool_id
        self.label = label
        self.requirements = []  # List of Several object inhereting from [Requirement]
        self.hints = []
        self.inputs = []  # List of [CommandInputParameter] objects
        self.outputs = []  # List of [CommandOutputParameter] objects
        self.baseCommand = base_command
        self.arguments = []  # List of [CommandLineBinding] objects
        self.doc = doc
        self.stdin = stdin
        self.stderr = stderr
        self.stdout = stdout
        self.successCodes = []
        self.temporaryFailCodes = []
        self.permanentFailCodes = []
        self._path = path
        self.namespaces = Namespaces()
        self.metadata = {}

    def get_dict(self):

        d = super(CommandLineTool, self).get_dict()

        d["class"] = self.__CLASS__

        if self.metadata:
            for key, value in self.metadata.__dict__.items():
                d["s:" + key] = value
            # - Add Namespaces
            d[self.namespaces.name] = {}
            for k, v in self.namespaces.__dict__.items():
                if "$" not in v:
                    d[self.namespaces.name][k] = v

        if self.requirements:
            d["requirements"] = {r.get_class(): r.get_dict() for r in self.requirements}
        return d

    def export_string(self):
        ruamel.yaml.add_representer(literal, literal_presenter)
        cwl_tool = self.get_dict()
        return ruamel.yaml.dump(cwl_tool, default_flow_style=False)

    def export(self, outfile=None):
        """
        Export the tool in CWL either on STDOUT or in outfile.
        """
        rep = self.export_string()

        # Write CWL file in YAML
        if outfile is None:
            six.print_(CWL_SHEBANG, "\n", sep="")
            six.print_(rep)
        else:
            out_write = open(outfile, "w")
            out_write.write(CWL_SHEBANG + "\n\n")
            out_write.write(rep)
            out_write.close()
