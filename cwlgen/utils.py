"""
Set of util functions and classes
"""


class literal(str): pass


def literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style="|")


class Serializable(object):

    @staticmethod
    def serialize(obj):
        if isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, bool):
            return obj
        if isinstance(obj, list):
            return [Serializable.serialize(x) for x in obj]
        if isinstance(obj, dict):
            return {k: Serializable.serialize(v) for k, v in obj.items() if v is not None}
        if callable(getattr(obj, "get_dict", None)):
            return obj.get_dict()
        raise Exception("Can't serialize '{unsupported_type}'".format(unsupported_type=type(obj)))

    @staticmethod
    def should_exclude_object(value):
        return value is None or ((isinstance(value, list) or isinstance(value, dict)) and len(value) == 0)

    def get_dict(self):
        d = {}
        ignore_attributes = set()
        if hasattr(self, "ignore_attributes") and self.ignore_attributes:
            ignore_attributes = set(self.ignore_attributes)

        for k, v in vars(self).items():
            if self.should_exclude_object(v) or k.startswith("_") or k in ignore_attributes or k == "ignore_attributes":
                continue
            s = self.serialize(v)
            if self.should_exclude_object(s):
                continue
            d[k] = s
        return d
        # return {k: self.serialize(v) for k, v in vars(self).items() if v is not None}
