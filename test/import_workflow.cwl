class: Workflow
cwlVersion: v1.0
doc: This is a documentation string
id: 1stWorkflow
inputs:
  name_of_file_to_extract:
    id: name_of_file_to_extract
    type: string
  tarball:
    id: tarball
    type: File
  test_input:
    default: def_in
    doc: documentation_in
    format: format_1930
    id: test_input
    label: label_in
    secondaryFiles: sec_file_in
    streamable: true
    type: File
outputs:
  compiled_class:
    id: compiled_class
    outputSource: compile/classfile
    type: File
steps:
  compile:
    in:
      src:
        id: src
        source: untar/extracted_file
    out:
    - classfile
    run: arguments.cwl
  untar:
    in:
      extractfile:
        id: extractfile
        source: name_of_file_to_extract
      tarfile:
        id: tarfile
        source: tarball
    out:
    - extracted_file
    run: tar-param.cwl