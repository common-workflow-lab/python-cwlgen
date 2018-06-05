#!/usr/bin/env cwl-runner

$namespaces: {s: http://schema.org/}
arguments: []
baseCommand: grep
class: CommandLineTool
cwlVersion: v1.0
doc: |-
  grep searches for a pattern in a file.
id: grep
inputs:
  input_file:
    doc: input file from which you want to look for the pattern
    inputBinding: {loadContents: false, position: 2, separate: true, shellQuote: true}
    type: File
  pattern:
    doc: pattern to find in the input file
    inputBinding: {loadContents: false, position: 1, separate: true, shellQuote: true}
    type: string
label: print lines matching a pattern
outputs:
  output: {doc: lines found with the pattern, type: stdout}
s:about: grep searches for a pattern in a file.
s:name: grep
stdout: grep.txt
