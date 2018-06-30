#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: tool_id
label: a_label
baseCommand: cat
class: CommandLineTool
doc: "super_doc"
stdin: "in"
stderr: "err"
stdout: "out"
inputs:
  INTEGER:
    doc: 'documentation_in'
    inputBinding:
      loadContents: True
      position: 0
      prefix: --input
      separate: True
      itemSeparator: ';'
      valueFrom: here
      shellQuote: True
    type: int
outputs:
  OUTPUT1:
    label: label_out
    doc: 'documentation_out'
    outputBinding:
      glob: "find"
      loadContents: True
      outputEval: "eval"
    type: File
