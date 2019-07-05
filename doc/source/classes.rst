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

CommandInputArraySchema
"""""""""""""""""""""""

.. autoclass:: cwlgen.CommandInputArraySchema
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

As of release v0.3.0 the existing importing CWL has been replaced by an
automated deserialization. Each function that inherits from the :class:`Serializable`
class will have a ``parse_dict`` method.

If you're adding a class and want to provide a hint on how to parse a particular
field, you can add a static ``parse_types`` dictionary onto your class with the
fieldname and a list of types that you want to try and parse as. If your input
can be a list (eg: ``T[]``), or a dictionary with the identifier as the key
(eg: ``{ $identifier: T }``, you can let your type be ``[T]`` in the ``parse_types``
dict. It will automatically inject this identifier in the constructor.
See the ``Serializable.parse_dict`` class for more information.

.. code-block:: python

   class Workflow:
       parse_types = {
           # Parse inputs as : [InputParameter] or { id: InputParameter }
           "inputs": [[InputParameter]],

           # will attempt to parse extraParam as a string, then SecondaryType,
           # then (TertiaryType[] || { $identifier: TertiaryType }
           "extraParam": [str, SecondaryType, [TertiaryType]]
       }

.. autofunction:: cwlgen.parse_cwl

.. autofunction:: cwlgen.parse_cwl_dict
