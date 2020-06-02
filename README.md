# python-cwlgen (deprecated)

## Deprecated

`python-cwlgen` is now deprecated, please use [`cwl-utils >= 0.4`](https://github.com/common-workflow-language/cwl-utils).

```sh
from cwl_utils import parser_v1_0

# You could alias this as cwlgen to simplify the migration
from cwl_utils import parser_v1_0 as cwlgen
```

Migration notes:

- Method changes
  - `get_dict() → save()` 
  - `parse_cwl(cwlfile)` → `load_document(cwlfile)`
  - `parse_dict` → No super clear analogue, but loaded through `_RecordLoader(CommandLineTool)` || `_UnionLoader((CommandLineToolLoader, ...workflow + other loaders)`

- Field names:
  - Uses `camelCase` instead of `snake_case`
  - No more special field names, eg:
    - `tool_id` | `workflow_id` | `input_id` | etc → `id`
    - `StepInput`: `inputs` → `in_`
    
- Other notes:
  - Classes aren't nested anymore, ie: `cwlgen.InitialWorkDirRequirement.Dirent` → `cwl_utils.parser_v1_0.Dirent`.
  - Take care if you're migrating to a newer spec, as some classes might have changed names (notably: `InputParameter` -> `WorkflowInputParameter`)
  - Don't forget to catch all references of cwlgen, as missing one (or using mismatch versions of the parser) will cause:
  
    ```python
    raise RepresenterError('cannot represent an object: %s' % (data,))
    ruamel.yaml.representer.RepresenterError: cannot represent an object: 
    <cwlgen.common.CommandInputArraySchema object at 0x1100a5780>
    ```
    
If you have issues with the migration, please see [this thread](https://github.com/common-workflow-language/python-cwlgen/issues/27) or raise an issue on CWLUtils.
    
---

## Original README

[![Build Status](https://travis-ci.org/common-workflow-language/python-cwlgen.svg?branch=master)](https://travis-ci.org/common-workflow-language/python-cwlgen)
[![codecov](https://codecov.io/gh/common-workflow-language/python-cwlgen/branch/master/graph/badge.svg)](https://codecov.io/gh/common-workflow-language/python-cwlgen)
[![Documentation Status](https://readthedocs.org/projects/python-cwlgen/badge/?version=latest)](http://python-cwlgen.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/cwlgen.svg)](https://badge.fury.io/py/cwlgen)

Python-cwlgen is a python library for the generation of CWL programmatically.
It supports the generation of CommandLineTool, Workflow and DockerRequirement.
The library works for both Python 2.7.12+ and 3.6.0.

------------------------


## Common Workflow Language

[Common Workflow Language (CWL)](https://www.commonwl.org/v1.0/index.html) is a language to describe workflows. 
The [user guide](http://www.commonwl.org/user_guide/01-introduction/index.html)
 gives a gentle explanation of what its goals are, but broadly:
 
 1. Stop writing bash scripts for long complex jobs.
 2. Take pipelines anywhere (portability).
 3. Enforce reproducibility guidelines.
 
This python repository is a python wrapper for _most_ of the classes (work in progress), 
allowing you to build the structure of the workflow in Python and have this module generate and export CWL for you.

**Nb:** This doesn't check the logic of Workflows or CommandLineTools for you.  
[CWLTool](https://github.com/common-workflow-language/cwltool) has a `--validate` mode that you can use.

## Quick-start guide

You can install python-cwlgen through pip with the following command:

```bash
pip install cwlgen
```

### How it works?

This repository contains a number of python classes that mirror the CWL specifications ([Workflow](https://www.commonwl.org/v1.0/Workflow.html)| 
[CommandLineTool](https://www.commonwl.org/v1.0/CommandLineTool.html)). In essence, each class's initializer has all 
of the properties it expects, which may be another object. The classes include the relevant docstrings to give you 
context of classes and their properties.

The `examples/` folder contains some simple examples, however in essence you simply initialize the class you're 
trying to build. An initializer for a class has all of the properties it expects which may be another object.


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
tool_object.export("echotool.cwl")
```

## References

CWL is developed by an informal, multi-vendor working group consisting of organizations and individuals 
aiming to enable scientists to share data analysis workflows. 
The [CWL project is on Github](https://github.com/common-workflow-language/common-workflow-language).


## Known issues

- `SchemaDefRequirement` doesn't parse the `types` subfield into the specific types 
(`InputRecordSchema | InputEnumSchema |  InputArraySchema`), but leaves them as a simple dictionary.