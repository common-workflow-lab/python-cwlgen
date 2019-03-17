# python-cwlgen

(From original repository)

[![Build Status](https://travis-ci.org/common-workflow-language/python-cwlgen.svg?branch=master)](https://travis-ci.org/common-workflow-language/python-cwlgen)
[![codecov](https://codecov.io/gh/common-workflow-language/python-cwlgen/branch/master/graph/badge.svg)](https://codecov.io/gh/common-workflow-language/python-cwlgen)
[![Documentation Status](https://readthedocs.org/projects/python-cwlgen/badge/?version=latest)](http://python-cwlgen.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/cwlgen.svg)](https://badge.fury.io/py/cwlgen)

Python-cwlgen is a python library for the generation of CWL programmatically.
It supports the generation of CommandLineTool, Workflow and DockerRequirement.
The library works for both Python 2.7.12+ and 3.6.0.

------------------------


# Common Workflow Language

[Common Workflow Language (CWL)](https://www.commonwl.org/v1.0/index.html) is a language to describe workflows. 
The [user guide](http://www.commonwl.org/user_guide/01-introduction/index.html)
 gives a gentle explanation of what its goals are, but broadly:
 
 1. Stop writing bash scripts for long complex jobs.
 2. Take pipelines anywhere (portability).
 3. Enforce reproducibility guidelines.
 
This python repository is a python wrapper for _most_ of the classes (work in progress), 
allowing you to build the structure of the workflow in Python and have this module generate and export CWL for you.

**Nb:** This isn't going to sanity or quality check Workflows or CommandLineTools for you, use 
[CWLTool](https://github.com/common-workflow-language/cwltool) or [WOMTool](https://cromwell.readthedocs.io/en/develop/WOMtool/) for that.

## Quick-start guide

You can install python-cwlgen through pip with the following command:

```
pip install cwlgen
```

## How it works ?

There's a pretty close copy of the cwl specifications ([Workflow](https://www.commonwl.org/v1.0/Workflow.html)| 
[CommandLineTool](https://www.commonwl.org/v1.0/CommandLineTool.html)), where the Python classes mirror the CWL spec. 
This repository also includes docstrings to give you context of classes and their properties.

The `examples/` folder contains some simple examples, however , 
you can simply initialise that class, for example:

_Creating a CommandLineTool_
```python
import cwlgen

tool_object = cwlgen.CommandLineTool(tool_id="echo-tool", base_command="echo", label=None, doc=None,
                 cwl_version="v1.0", stdin=None, stderr=None, stdout=None, path=None)
tool_object.inputs.append(
    cwlgen.CommandInputParameter("myParamId", param_type="string", label=None, secondary_files=None, param_format=None,
                 streamable=None, doc=None, input_binding=None, default=None)
)

# to get the dictionary representation:
dict_to_export = tool_object.get_dict()

# to get the string representation (YAML)
yaml_export = tool_object.export_string()

# print to console
tool_object.export()

# print to file
with open("echotool.cwl", "w") as f:
    tool_object.export(f)
```
