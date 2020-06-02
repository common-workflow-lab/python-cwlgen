.. python-cwlgen - Python library for manipulation and generation of CWL tools.

***********
API classes
***********

Workflow and CommandLineTool
============================

See the links below to the `CommandLineTool` and `Workflow` classes:

- :class:`cwlgen.CommandLineTool`
- :class:`cwlgen.Workflow`

Requirements
============

Requirement
"""""""""""

This is the (abstract) base requirement class.

.. autoclass:: cwlgen.Requirement
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

InlineJavascriptRequirement
"""""""""""""""""""""""""""

.. autoclass:: cwlgen.InlineJavascriptRequirement
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

SchemaDefRequirement
""""""""""""""""""""

See the Schema section Below:

- :class:`cwlgen.SchemaDefRequirement`


SubworkflowFeatureRequirement
"""""""""""""""""""""""""""""

.. autoclass:: cwlgen.SubworkflowFeatureRequirement
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

ScatterFeatureRequirement
""""""""""""""""""""""""""

.. autoclass:: cwlgen.ScatterFeatureRequirement
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

MultipleInputFeatureRequirement
"""""""""""""""""""""""""""""""

.. autoclass:: cwlgen.MultipleInputFeatureRequirement
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

StepInputExpressionRequirement
"""""""""""""""""""""""""""""""

.. autoclass:: cwlgen.StepInputExpressionRequirement
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

SoftwareRequirement
"""""""""""""""""""

.. autoclass:: cwlgen.SoftwareRequirement
    :members:
    :private-members:
    :special-members:
    :exclude-members: SoftwarePackage,__weakref__

.. autoclass:: cwlgen.SoftwareRequirement.SoftwarePackage
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__


InitialWorkDirRequirement
""""""""""""""""""""""""""

.. autoclass:: cwlgen.InitialWorkDirRequirement
    :members:
    :private-members:
    :special-members:
    :exclude-members: Dirent,__weakref__

.. autoclass:: cwlgen.InitialWorkDirRequirement.Dirent
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__


EnvVarRequirement
"""""""""""""""""""

.. autoclass:: cwlgen.EnvVarRequirement
    :members:
    :private-members:
    :special-members:
    :exclude-members: EnvironmentDef,__weakref__

.. autoclass:: cwlgen.EnvVarRequirement.EnvironmentDef
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

ShellCommandRequirement
"""""""""""""""""""""""

.. autoclass:: cwlgen.ShellCommandRequirement
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

ResourceRequirement
"""""""""""""""""""

.. autoclass:: cwlgen.ResourceRequirement
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__


Schema
======

.. autoclass:: cwlgen.SchemaDefRequirement
    :members:
    :private-members:
    :special-members:
    :exclude-members: InputRecordSchema,InputEnumSchema,InputArraySchema,__weakref__


Workflow Input Schema
"""""""""""""""""""""

.. autoclass:: cwlgen.SchemaDefRequirement.InputRecordSchema
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

.. autoclass:: cwlgen.SchemaDefRequirement.InputEnumSchema
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

.. autoclass:: cwlgen.SchemaDefRequirement.InputArraySchema
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref__

- :class:`CommandLineBinding`

    When listed under inputBinding in the input schema, the term "value"
    refers to the the corresponding value in the input object. For binding objects listed in
    CommandLineTool.arguments, the term "value" refers to the effective value after evaluating valueFrom.


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
