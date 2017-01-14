#!/usr/bin/env cwl-runner

cwlVersion: v1.0
id: an_id
label: a description with spaces.
baseCommand: a_command
class: CommandLineTool
doc: documentation
inputs:
  an_in_id:
    type: File
outputs:
  an_out_id:
    type: File
