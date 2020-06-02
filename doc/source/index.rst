.. python-cwlgen - Python library for manipulation and generation of CWL tools.


Python-CWLGen (**Deprecated**)
=========================================

.. warning::

   ``python-cwlgen`` is now deprecated, please use `cwl-utils >= 0.4 <https://github.com/common-workflow-language/cwl-utils>`_.

Example migration:

.. code-block:: bash

   from cwl_utils import parser_v1_0
   
   # You could alias this as cwlgen to simplify the migration
   from cwl_utils import parser_v1_0 as cwlgen


Migration notes:
+++++++++++++++++++++

- Method changes

  - ``get_dict() → save()`` 
  - ``parse_cwl(cwlfile)`` → ``load_document(cwlfile)``
  - ``parse_dict`` → No super clear analogue, but loaded through ``_RecordLoader(CommandLineTool)`` || ``_UnionLoader((CommandLineToolLoader, ...workflow + other loaders)``

- Field names:

  - Uses ``camelCase`` instead of ``snake_case``
  - No more special field names, eg:
    - ``tool_id`` | ``workflow_id`` | ``input_id`` | etc → ``id``
    - ``StepInput``: ``inputs`` → ``in_``
    
- Other notes:

  - Classes aren't nested anymore, ie: ``cwlgen.InitialWorkDirRequirement.Dirent`` → ``cwlutils``.
  - Take care if you're migrating to a newer spec, as some classes might have changed names (notably: ``InputParameter`` -> ``WorkflowInputParameter``)
  - Don't forget to catch all references of cwlgen, as missing one (or using mismatch versions of the parser) will cause:
  
    .. code-block:: python

       raise RepresenterError('cannot represent an object: %s' % (data,))
       ruamel.yaml.representer.RepresenterError: cannot represent an object:
       <cwlgen.common.CommandInputArraySchema object at 0x1100a5780>

If you have issues with the migration, please see `this thread <https://github.com/common-workflow-language/python-cwlgen/issues/27>`_ or raise an issue on CWLUtils.
    

.. image:: https://travis-ci.org/common-workflow-language/python-cwlgen.svg?branch=master&style=flat
    :target: https://travis-ci.org/common-workflow-language/python-cwlgen
    :alt: Travis Build Status

.. image:: https://readthedocs.org/projects/python-cwlgen/badge/?version=latest
    :target: https://python-cwlgen.readthedocs.io/en/latest/?badge=latest)
    :alt: Documentation

.. image:: https://badge.fury.io/py/cwlgen.svg
    :target: https://pypi.org/project/cwlgen/
    :alt: Pypi module

.. image:: https://codecov.io/gh/common-workflow-language/python-cwlgen/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/common-workflow-language/python-cwlgen
    :alt: Code Coverage


Python-cwlgen is a python library for the programmatic generation of CWL v1.0.
It supports the generation of CommandLineTool and Workflows.

The library works for both Python 2.7.12+ and 3.6.0+.

Quick-start
===========

You can install Python-CWLGen through pip with the following command:

.. code-block:: bash

   pip install cwlgen

The classes very closely (if not exactly) mirror the CWL v1.0 specification. You can find
more about their parameters in the following specifications:

- :class:``cwlgen.CommandLineTool``
- :class:``cwlgen.Workflow``


Python-cwlgen
=============
.. toctree::
   :maxdepth: 2

   installation
   user_guide
   references

Python-cwlgen API documentation
===============================
.. toctree::
   :maxdepth: 1

   classes
   commandlinetoolclasses
   workflowclasses
   changelogs

..
  Indices and tables
  ==================

  * :ref:``genindex``
  * :ref:``modindex``
  * :ref:``search``
