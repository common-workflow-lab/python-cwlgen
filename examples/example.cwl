id: pouet
label: pouet cest la vie
baseCommand: pouet
class: CommandLineTool
inputs:
  config_file:
    type: File
    doc: config file
    format: http://edamontology.org/format_0000
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
    doc: counts of blablabla
    format: http://edamontology.org/format_1111
    outputBinding:
      glob: counts.txt
