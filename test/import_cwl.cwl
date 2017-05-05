#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: tool_id
label: a_label
baseCommand: share
class: CommandLineTool
doc: "super_doc"
stdin: "in"
stderr: "err"
stdout: "out"
inputs:
  INPUT1:
    label: label_in
    secondaryFiles: 'sec_file_in'
    format: format_1930
    streamable: True
    default: 'def_in'
    doc: 'documentation_in'
    inputBinding:
      loadContents: True
      position: 0
      prefix: --input
      separate: True
      itemSeparator: ';'
      valueFrom: here
      shellQuote: True
    type: File
outputs:
  OUTPUT1:
    label: label_out
    secondaryFiles: 'sec_file_out'
    format: format_1930
    streamable: True
    doc: 'documentation_out'
    type: File
