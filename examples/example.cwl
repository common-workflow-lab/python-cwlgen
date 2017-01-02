baseCommand: pouet
class: CommandLineTool
doc: '|Ceci est une super documentation'
id: pouet
inputs:
  config_file:
    doc: config file
    format: http://edamontology.org/format_0000
    inputBinding:
      position: 1
    type: File
  threads:
    doc: number of threads
    inputBinding:
      prefix: -t
    type: int
label: pouet cest la vie
outputs:
  result_file:
    doc: counts of blablabla
    format: http://edamontology.org/format_1111
    outputBinding:
      glob: counts.txt
    type: File
