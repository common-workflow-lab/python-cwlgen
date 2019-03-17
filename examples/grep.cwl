#!/usr/bin/env cwl-runner

$namespaces:
  s: http://schema.org/
baseCommand: grep
class: CommandLineTool
cwlVersion: v1.0
doc: grep searches for a pattern in a file.
id: grep
inputs:
- doc: input file from which you want to look for the pattern
  id: input_file
  inputBinding:
    position: 2
  type: File
- doc: pattern to find in the input file
  id: pattern
  inputBinding:
    position: 1
  type: string
label: print lines matching a pattern
metadata:
  about: grep searches for a pattern in a file.
  name: grep
outputs:
- doc: lines found with the pattern
  id: output
  type: stdout
s:about: grep searches for a pattern in a file.
s:name: grep
stdout: grep.txt
