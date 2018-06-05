.. python-cwlgen - Python library for manipulation and generation of CWL tools.

.. _user_guide:

**********
User Guide
**********

This user guide assumes you have at least some basic knowledge about CWL.

.. Note::
    Here is a `CWL user guide`_ for an introduction to tool and workflows wrappers.

.. _`CWL user guide`: https://www.commonwl.org/user_guide/

The aim is to help you through the different steps to build your CWL tool with
python-cwlgen.

.. Note::
    If you find a bug, have any questions or suggestions, please `submit an issue on Github`_.

.. _`submit an issue on Github`: https://github.com/common-workflow-language/python-cwlgen/issues/new

Basic example
-------------
Through this little tutorial, we will go step by step through the example you can `find on Github`_. It aims to wrap the `grep` command.

.. _`find on Github`: https://github.com/common-workflow-language/python-cwlgen/blob/master/examples/example.py

Initialize your tool
""""""""""""""""""""

You need to initialize a `CommandLineTool` object

.. code-block:: python

    import cwlgen
    cwl_tool = cwlgen.CommandLineTool(tool_id='grep',
                                      label='print lines matching a pattern',
                                      base_command='grep')

Now that you have your object, you can attach the different elements of a tool description.

Add Inputs
""""""""""

Now we need to add inputs to our tool. We are going to only wrap a simple version of the `grep` command with a input file and a pattern.

First the input file:

.. code-block:: python

    file_binding = cwlgen.CommandLineBinding(position=2)
    input_file = cwlgen.CommandInputParameter('input_file',
                                              param_type='File',
                                              input_binding=file_binding,
                                              doc='input file from which you want to look for the pattern')
    cwl_tool.inputs.append(input_file)

And finally the pattern:

.. code-block:: python

    pattern_binding = cwlgen.CommandLineBinding(position=1)
    pattern = cwlgen.CommandInputParameter('pattern',
                                           param_type='string',
                                           input_binding=pattern_binding,
                                           doc='pattern to find in the input file')
    cwl_tool.inputs.append(pattern)

.. Note::
    You can specify more information concerning your inputs:  `Input documentation`_

.. _`Input documentation`: http://python-cwlgen.readthedocs.io/en/latest/classes.html#input-and-outputs

This is it for the inputs, now let's add some outputs and the description will be ready to be tested.

Add an Output
"""""""""""""

The only output which is retrieved in our example is a File with the line containing the pattern. Here is how to add this output:

.. code-block:: python

    output = cwlgen.CommandOutputParameter('output',
                                           param_type='stdout',
                                           doc='lines found with the pattern')
    cwl_tool.outputs.append(output)
    # Now specify a name for your output file
    cwl_tool.stdout = "grep.txt"

Add Documentation and Metadata
""""""""""""""""""""""""""""""

You can ask bunch of information and metadata concerning your tool.
For instance you can add some documentation:

.. code-block:: python

    cwl_tool.doc = "grep searches for a pattern in a file."

For the metadata:

.. code-block:: python

    metadata = {'name': 'grep',
                'about' : 'grep searches for a pattern in a file.'}
    cwl_tool.metadata = cwlgen.Metadata(**metadata)

Write your tool
"""""""""""""""

Finally, you can export your tool description with the `export()` method.

.. code-block:: python

    cwl_tool.export()  # On STDOUT
    cwl_tool.export(outfile="grep.cwl")  # As a file (grep.cwl)

You can then try your tool description (using `cwltool`_ for instance):

.. _`cwltool`: https://github.com/common-workflow-language/cwltool/

.. code-block:: bash

    cwltool grep.cwl --input_file underdog_lyrics.txt --pattern lost