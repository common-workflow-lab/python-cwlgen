import logging

from .utils import Serializable

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

#  Constant(s)  ------------------------------

CWL_SHEBANG = "#!/usr/bin/env cwl-runner"
CWL_VERSIONS = ['draft-2', 'draft-3.dev1', 'draft-3.dev2', 'draft-3.dev3',
                'draft-3.dev4', 'draft-3.dev5', 'draft-3', 'draft-4.dev1',
                'draft-4.dev2', 'draft-4.dev3', 'v1.0.dev4', 'v1.0']
DEF_VERSION = 'v1.0'


#  Function(s)  ------------------------------

def parse_type(param_type, requires_type=False):
    """
    Parses the parameter type as one of the required types:
    :param requires_type:
    :: https://www.commonwl.org/v1.0/CommandLineTool.html#CommandInputParameter

    :param param_type: a CWL type that is _validated_
    :type param_type: CWLType | CommandInputRecordSchema | CommandInputEnumSchema | CommandInputArraySchema | string |
       array<CWLType | CommandInputRecordSchema | CommandInputEnumSchema | CommandInputArraySchema | string>
    :return: CWLType | CommandInputRecordSchema | CommandInputEnumSchema | CommandInputArraySchema | string |
       array<CWLType | CommandInputRecordSchema | CommandInputEnumSchema | CommandInputArraySchema | string>
    """

    if requires_type is False and param_type is None:
        return None

    if isinstance(param_type, str) and len(param_type) > 0:
        # Must be CWLType
        optional = param_type[-1] == "?"
        if optional:
            _LOGGER.debug("Detected {param_type} to be optional".format(param_type=param_type))
            cwltype = param_type[:-1]
        else:
            cwltype = param_type
        # cwltype = param_type[:-1] if optional else param_type

        # check for arrays
        if len(cwltype) > 2 and cwltype[-2:] == "[]":
            array_type = CommandInputArraySchema(items=cwltype[:-2])
            # How to make arrays optional input: https://www.biostars.org/p/233562/#234089
            return [CwlTypes.DEF_TYPE, array_type] if optional else array_type

        if cwltype not in CwlTypes.TYPES:
            _LOGGER.warning("The type '{param_type}' is not a valid CWLType, expected one of: {types}"
                            .format(param_type=param_type, types=", ".join(str(x) for x in CwlTypes.TYPES)))
            _LOGGER.warning("type is set to {}.".format(CwlTypes.DEF_TYPE))
            return CwlTypes.DEF_TYPE
        return param_type

    elif isinstance(param_type, list):
        return [parse_type(p) for p in param_type]

    elif isinstance(param_type, CommandInputArraySchema) \
            or isinstance(param_type, CommandInputRecordSchema) \
            or isinstance(param_type, CommandInputEnumSchema):
        return param_type  # validate if required

    if requires_type is True:
        raise Exception("'parse_type' was required but failed to parse '{ptype}', exiting")

    _LOGGER.warning("Unable to detect type of param '{param_type}'".format(param_type=param_type))
    return CwlTypes.DEF_TYPE


def get_type_dict(param_type):
    """
    Generic method to the get dict for any of the valid param_type types,
    ie:  CWLType | InputRecordSchema | InputEnumSchema | InputArraySchema | string
       | array<CWLType | InputRecordSchema | InputEnumSchema | InputArraySchema | string>
    :param param_type:
    :type param_type: CWLType | InputRecordSchema | InputEnumSchema | InputArraySchema | string |
                array<CWLType | InputRecordSchema | InputEnumSchema | InputArraySchema | string>
    :return: str | dict
    """
    if isinstance(param_type, str):
        return param_type
    elif isinstance(param_type, list):
        return [get_type_dict(p) for p in param_type]
    elif isinstance(param_type, dict):
        return param_type
    elif getattr(param_type, 'get_dict', None) and callable(getattr(param_type, 'get_dict', None)):
        return param_type.get_dict()
    else:
        raise Exception("Could not convert '{param_type}' to dictionary as it was unrecognised"
                        .format(param_type=type(param_type)))


#  Class(es)  ------------------------------

class CwlTypes:
    DEF_TYPE = "null"

    NULL = "null"
    BOOLEAN = "boolean"
    INT = "int"
    LONG = "long"
    FLOAT = "float"
    DOUBLE = "double"
    STRING = "string"
    FILE = "File"
    DIRECTORY = "Directory"
    STDOUT = "stdout"
    ARRAY = "array"

    NON_NULL_TYPES = [BOOLEAN, INT, LONG, FLOAT, DOUBLE, STRING, FILE, DIRECTORY, STDOUT]
    TYPES = [NULL, None, BOOLEAN, INT, LONG, FLOAT, DOUBLE, STRING, FILE, DIRECTORY, STDOUT]


# functions

class Namespaces(Serializable):
    """
    Define different namespace for the description.
    """

    def __init__(self):
        """
        """
        self.name = "$namespaces"
        self.s = "http://schema.org/"


class Metadata(Serializable):
    """
    Represent metadata described by http://schema.org.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Parameter(Serializable):
    '''
    Based class for parameters (common field of Input and Output) for CommandLineTool and Workflow
    '''

    def __init__(self, param_id, label=None, secondary_files=None, param_format=None,
                 streamable=None, doc=None, param_type=None, requires_type=False):
        '''
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
        :param param_type: type of data assigned to the parameter
        :type param_type: STRING corresponding to CWLType
        '''

        self.id = param_id
        self.label = label
        self.secondaryFiles = secondary_files
        self.format = param_format
        self.streamable = streamable
        self.doc = doc
        self.type = parse_type(param_type, requires_type)

    @classmethod
    def parse_with_id(cls, d, identifier):
        d["id"] = identifier
        return super(Parameter, cls).parse_dict(d)

    # @classmethod
    # def parse_dict(cls, d):
    #     self = super(Parameter, cls).parse_dict(d)
    #     secs = d.get("secondaryFiles")
    #     self.secondaryFiles = []
    #     if secs:
    #         self.secondaryFiles = secs if isinstance(secs, list) else [secs]
    #     return self


class CommandInputArraySchema(Serializable):
    '''
    Based on the parameter set out in the CWL spec:
    https://www.commonwl.org/v1.0/CommandLineTool.html#CommandInputArraySchema
    '''

    def __init__(self, items=None, label=None, input_binding=None):
        '''
        :param items: Defines the type of the array elements.
        :type: `CWLType | CommandInputRecordSchema | CommandInputEnumSchema | CommandInputArraySchema | string | array<CWLType | CommandInputRecordSchema | CommandInputEnumSchema | CommandInputArraySchema | string>`
        :param label: A short, human-readable label of this object.
        :type label: STRING
        :param input_binding:
        :type input_binding: CommandLineBinding
        '''
        self.type = CwlTypes.ARRAY
        self.items = parse_type(items, requires_type=True)
        self.label = label
        self.inputBinding = input_binding


class CommandInputRecordSchema(Serializable):
    """
    Documentation: https://www.commonwl.org/v1.0/Workflow.html#CommandInputRecordSchema
    """

    def __init__(self, label=None, name=None):
        """
        :param fields: Defines the fields of the record.
        :type fields: array<InputRecordField>
        :param label: A short, human-readable label of this object.
        :param name: NF (Name of the InputRecord)
        """
        self.fields = []
        self.label = label
        self.name = name
        self.type = "record"

    class CommandInputRecordField(Serializable):
        """
        Documentation: https://www.commonwl.org/v1.0/Workflow.html#CommandInputRecordField
        """

        def __init__(self, name, input_type, doc=None, input_binding=None, label=None):
            """
            :param name:
            :param input_type:
            :type input_type: CWLType | InputRecordSchema | InputEnumSchema | InputArraySchema | string |
                        array<CWLType | InputRecordSchema | InputEnumSchema | InputArraySchema | string>
            :param doc: A documentation string for this field
            :param input_binding:
            :type input_binding: CommandLineBinding
            :param label:
            """
            self.name = name
            self.type = parse_type(input_type, requires_type=True)
            self.doc = doc
            self.inputBinding = input_binding
            self.label = label

        def get_dict(self):
            d = super(type(self), self).get_dict()
            d["type"] = get_type_dict(self.type)
            return d


class CommandInputEnumSchema(Serializable):
    """
    Documentation: https://www.commonwl.org/v1.0/Workflow.html#CommandInputEnumSchema
    """

    def __init__(self, symbols, label=None, name=None, input_binding=None):
        """
        :param symbols: Defines the set of valid symbols.
        :type symbols: List[str]
        :param label: A short, human-readable label of this object.
        :type label: str
        :param name:
        :type name: str
        :param input_binding:
        :type input_binding: CommandLineBinding
        """
        self.type = "enum"
        self.symbols = symbols
        self.label = label
        self.name = name
        self.inputBinding = input_binding
