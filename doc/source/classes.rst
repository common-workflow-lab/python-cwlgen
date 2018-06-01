.. python-cwlgen - Python library for manipulation and generation of CWL tools.

.. _classes:

***********
API classes
***********

.. _cwl_tool:

CWL Tool
========

CommandLineTool
"""""""""""""""

.. autoclass:: cwlgen.CommandLineTool
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

.. _cwl_workflow:

CWL Workflow
============

Workflow
""""""""

.. autoclass:: cwlgen.workflow.Workflow
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

InputParameter
""""""""""""""

.. autoclass:: cwlgen.workflow.InputParameter
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

WorkflowStep
""""""""""""

.. autoclass:: cwlgen.workflow.WorkflowStep
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__


.. _in_out:

Input and outputs
=================

CommandInputParameter
"""""""""""""""""""""

.. autoclass:: cwlgen.CommandInputParameter
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

CommandOutputParameter
""""""""""""""""""""""

.. autoclass:: cwlgen.CommandOutputParameter
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

CommandLineBinding
""""""""""""""""""

.. autoclass:: cwlgen.CommandLineBinding
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

CommandOutputBinding
""""""""""""""""""""

.. autoclass:: cwlgen.CommandOutputBinding
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

.. _requirements:

Requirements
============

Requirement
"""""""""""

.. autoclass:: cwlgen.Requirement
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

InlineJavascriptReq
"""""""""""""""""""

.. autoclass:: cwlgen.InlineJavascriptReq
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

DockerRequirement
"""""""""""""""""

.. autoclass:: cwlgen.DockerRequirement
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

Import CWL
==========

CWLToolParser
"""""""""""""

.. autoclass:: cwlgen.import_cwl.CWLToolParser
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref_
_
InputsParser
""""""""""""

.. autoclass:: cwlgen.import_cwl.InputsParser
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

InputBindingParser
""""""""""""""""""

.. autoclass:: cwlgen.import_cwl.InputBindingParser
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

OutputsParser
"""""""""""""

.. autoclass:: cwlgen.import_cwl.OutputsParser
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

OutputBindingParser
"""""""""""""""""""

.. autoclass:: cwlgen.import_cwl.OutputBindingParser
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

CWLWorkflowParser
"""""""""""""""""

.. autoclass:: cwlgen.import_cwl.CWLWorkflowParser
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

StepsParser
"""""""""""

.. autoclass:: cwlgen.import_cwl.StepsParser
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__