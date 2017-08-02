#!/usr/bin/env cwl-runner

id: my_tool
label: my_tool is magic
baseCommand: run_my_tool
doc: Magic is no magic without secrets...
class: CommandLineTool
inputs:
  config_file:
    format: http://edamontology.org/format_2330
    doc: config file
    type: File
    inputBinding:
      position: 1
  threads:
    doc: number of threads
    type: int
    inputBinding:
      prefix: -t
outputs:
  result_file:
    format: http://edamontology.org/format_2330
    doc: magic results
    type: File
    outputBinding:
      glob: counts.txt
s:name: my tool
s:about: I let you guess
s:publication:
- id: one_doi
- id: another_doi
s:license:
- MIT
$namespace:
  s: http://schema.org/
