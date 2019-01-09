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



I've forked this repository to try and get my use of this repository working quickly without 
worrying too much about proper code etiquette. I have and will continue to submit merge requests 
back to the [original repository](https://github.com/common-workflow-language/python-cwlgen).

[![Build Status](https://travis-ci.org/illusional/python-cwlgen.svg?branch=master)](https://travis-ci.org/common-workflow-language/python-cwlgen)
[![codecov](https://codecov.io/gh/illusional/python-cwlgen/branch/master/graph/badge.svg)](https://codecov.io/gh/illusional/python-cwlgen)


# Common Workflow Language

[Common Workflow Language (CWL)](https://www.commonwl.org/v1.0/index.html) is a method to describe workflows,
 and any tools (software) that it may use. The [user guide](http://www.commonwl.org/user_guide/01-introduction/index.html)
 gives a gentle (and better) explanation of what its goals are, and how they are achieved, but broadly:
 
 1. Stop writing bash scripts for long complex jobs.
 2. Take pipelines anywhere (portability).
 3. Try to enforce reproducibility guidelines.
 
This python repository is simply a python wrapper for _most_ of the classes (work in progress), 
allowing you to build the structure of the workflow in Python and have this module generate and export CWL for you.

**Nb:** This isn't going to sanity or quality check Workflows or CommandLineTools for you, use 
[CWLTool](https://github.com/common-workflow-language/cwltool) or [WOMTool](https://cromwell.readthedocs.io/en/develop/WOMtool/) for that.

# Quick-start guide

## Installation

This isn't available through _pip_ (the official repository is), however you can embed it using git submodules, 
or just download the source code.

### Git submodule installation

You can use gitsubmodules to embed the repository into your project (in a folder called `cwlgen/`) with the following command.

`git submodule add git@github.com:illusional/python-cwlgen.git cwlgen/`

Then you can use it by `import cwlgen.cwlgen as cwl`.

#### Updating the repository
Just `cd` into the `cwlgen` folder (the submodule) inside your project, and then run `git pull origin master` 
to update to the latest commit of master. Then change back into the root directory of your project and commit 
the commit hash change.

## How it works ?

There's a pretty close copy of the cwl specifications ([Workflow](https://www.commonwl.org/v1.0/Workflow.html)| 
[CommandLineTool](https://www.commonwl.org/v1.0/CommandLineTool.html)), where the Python classes mirror the CWL spec. 
This repository also includes some of the docstrings to give you context of classes and their properties.

I've tried to include direct links to a classes documentation, however this isn't always possible.

There are some small examples in the `examples/` folder, however for whatever class you need, you simply just init 
that class, for example:

_Creating a CommandLineTool_
```python
# if using gitsubmodules, you can use the following import statement
import cwlgen as cwl

tool_object = cwl.CommandLineTool(cwltool_id="echo-tool", base_command=echo, label=None, doc=None,
                 cwl_version="v1.0", stdin=None, stderr=None, stdout=None, path=None)
tool_object.inputs.append(cwl.CommandInputParameter(param_id, label=None, secondary_files=None, param_format=None,
                 streamable=False, doc=None, input_binding=None, default=None, param_type=None)
                 
# fill in the fields as required

# to get the dictionary representation:
dict_to_export = tool_object.get_dict()

# dump using a yaml exporter
yaml.dump(dict_to_export)
```

All of the classes should work in a similar way. I've removed the `literal` representation from my fork as I 
didn't want to use _ruamel_ at the moment. Otherwise file an issue and I'll have a look into it.
