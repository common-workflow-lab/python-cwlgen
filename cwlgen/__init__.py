'''
Library to handle the manipulation and generation of CWL tool
'''

import warnings

warnings.warn(
    "The cwlgen module is deprecated, please use "
    "cwl-utils >= 0.4: https://github.com/common-workflow-language/cwl-utils",
    DeprecationWarning,
    stacklevel=2
)


#  Import  ------------------------------

# General libraries
import logging

# External libraries
import ruamel.yaml
import six
from .version import __version__

from .utils import literal, literal_presenter

from .import_cwl import parse_cwl, parse_cwl_dict

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

# imports for __init__

from .common import *
from .commandlinetool import *
from .workflow import *
from .workflowdeps import *
from .commandlinebinding import CommandLineBinding
from .requirements import *

