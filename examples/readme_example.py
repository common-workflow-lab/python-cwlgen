import cwlgen

tool_object = cwlgen.CommandLineTool(tool_id="echo-tool", base_command="echo", label=None, doc=None,
                                     cwl_version="v1.0", stdin=None, stderr=None, stdout=None, path=None)
tool_object.inputs.append(
    cwlgen.CommandInputParameter("myParamId", label=None, secondary_files=None, param_format=None,
                                 streamable=None, doc=None, input_binding=None, default=None, param_type="string")
)

# to get the dictionary representation:
dict_to_export = tool_object.get_dict()

# to get the string representation (YAML)
yaml_export = tool_object.export_string()

# print to console
tool_object.export()
