.. python-cwlgen - Python library for manipulation and generation of CWL tools.


Welcome to python-cwlgen's documentation!
=========================================

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

- :class:`cwlgen.CommandLineTool`
- :class:`cwlgen.Workflow`


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

  * :ref:`genindex`
  * :ref:`modindex`
  * :ref:`search`
