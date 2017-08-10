"""
Set of util functions and classes
"""

class literal(str): pass

def literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style = "|")
