id: my_tool
label: my_tool is magic
baseCommand: run_my_tool
class: CommandLineTool
doc: Magic is no magic without secrets...
inputs:
  config_file:
    type: File
    doc: config file
    format: http://edamontology.org/format_2330
    inputBinding:
      position: 1
  threads:
    type: int
    doc: number of threads
    inputBinding:
      prefix: -t
outputs:
  result_file:
    type: File
    doc: magic results
    format: http://edamontology.org/format_2330
    outputBinding:
      glob: counts.txt
