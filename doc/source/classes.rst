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

InlineJavascriptReq
"""""""""""""""""""

.. autoclass:: cwlgen.InlineJavascriptReq
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

CWLToolParser
"""""""""""""

.. autoclass:: cwlgen.import_cwl.CWLToolParser
    :members:
    :private-members:
    :special-members:
    :exclude-members: __weakref_

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