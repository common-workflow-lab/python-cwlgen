from .utils import Serializable


class CommandLineBinding(Serializable):
    """
    The binding behavior when building the command line depends on the data type of the value.
    If there is a mismatch between the type described by the input schema and the effective value,
    such as resulting from an expression evaluation, an implementation must use the data type of the effective value.

    Documentation: https://www.commonwl.org/v1.0/CommandLineTool.html#CommandLineBinding
    """

    def __init__(self, load_contents=None, position=None, prefix=None, separate=None,
                 item_separator=None, value_from=None, shell_quote=None):
        """
        :param load_contents: Read up to the fist 64 KiB of text from the file and
                              place it in the "contents" field of the file object
        :type load_contents: BOOLEAN
        :param position: The sorting key
        :type position: INT
        :param prefix: Command line prefix to add before the value
        :type prefix: STRING
        :param separate:
        :type separate: BOOLEAN
        :param item_separator: Join the array elements into a single string separated by this item
        :type item_separator: STRING
        :param value_from: Use this as the value
        :type value_from: STRING
        :param shell_quote: Value is quoted on the command line
        :type shell_quote: BOOLEAN
        """
        self.loadContents = load_contents
        self.position = position
        self.prefix = prefix
        self.separate = separate
        self.itemSeparator = item_separator
        self.valueFrom = value_from
        self.shellQuote = shell_quote
