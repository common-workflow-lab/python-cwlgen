"""
Set of util functions and classes
"""
import inspect

class literal(str): pass

_unparseable_types = [str, int, float, bool]


def literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style="|")


class Serializable(object):
    """
    Serializable docstring
    """


    """
    This is a special field, with format: [(fieldName: str, [Serializable])]
    If the field name is present in the dict, then it will call the parse_dict(cls, d)
    method on that type. It should return None if it can't parse that dictionary. This means
    the type will need to override the parse_dict method.
    """
    parse_types = []        # type: [(str, [type])]
    ignore_fields_on_parse = []
    ignore_fields_on_convert = []
    required_fields = []    # type: str

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
        if obj is None:
            return None     # some types allow None as value, such as default so we should explicitly allow it
        raise Exception("Can't serialize '{unsupported_type}'".format(unsupported_type=type(obj)))

    @staticmethod
    def should_exclude_object(value):
        return value is None or ((isinstance(value, list) or isinstance(value, dict)) and len(value) == 0)

    def get_dict(self):
        d = {}
        ignore_attributes = set()
        if hasattr(self, "ignore_attributes") and self.ignore_attributes:
            ignore_attributes = set(self.ignore_attributes)

        if self.ignore_fields_on_convert:
            ignore_attributes = ignore_attributes.union(self.ignore_fields_on_convert)

        for k, v in vars(self).items():
            if self.should_exclude_object(v) or k.startswith("_") or k in ignore_attributes or k == "ignore_attributes":
                continue
            s = self.serialize(v)
            if self.should_exclude_object(s):
                continue
            d[k] = s
        return d

    @classmethod
    def parse_with_id(cls, d, identifier):
        if not isinstance(d, dict):
            raise Exception("parse_with_id will require override to handle default object of type '%s'" % type(d))
        d["id"] = identifier
        return d

    @classmethod
    def parse_dict(cls, d):
        pts = {t[0]: t[1] for t in cls.parse_types}
        req = {r: False for r in cls.required_fields}
        ignore = set(cls.ignore_fields_on_parse)

        # may not be able to just initialise blank class
        # but we can use inspect to get required params and init using **kwargs

        params = dict(inspect.signature(cls.__init__).parameters)
        inspect_ignore_keys = {"self", "args", "kwargs"}
        required_param_keys = {k for k in params if params[k].default == inspect._empty}

        # Params can't shadow the built in 'id', so we'll put in a little hack
        # to guess the required param name that ends in

        id_field_names = [k for k in required_param_keys if k == "id" or k.endswith("_id")]
        id_field_name = None
        id_field_value = d.get("id")

        if len(id_field_names) == 1:
            id_field_name = id_field_names[0]
            inspect_ignore_keys.add(id_field_name)
        elif len(id_field_names) > 1:
            print("Warning, can't determine if there are multiple id fieldnames")

        required_init_kwargs = { k: d[k] for k in required_param_keys if (k not in inspect_ignore_keys) }
        if id_field_name:
            required_init_kwargs[id_field_name] = id_field_value

        self = cls(**required_init_kwargs)

        for k, v in d.items():
            val = None
            if k in ignore: continue
            types = pts.get(k)
            if types:
                idx = 0
                while idx < len(types) and val is None:
                    T = types[idx]
                    if T in _unparseable_types:
                        val = T(val)
                    elif isinstance(T, list):
                        T = T[0]
                        if isinstance(v, list):
                            val = [T.parse_dict(vv) for vv in v]
                        elif isinstance(v, dict):
                            val = []
                            for nested_key in v:
                                dd = v[nested_key]
                                val.append(T.parse_with_id(dd, nested_key))
                    else:
                        val = T.parse_dict(v) if not isinstance(v, list) else [T.parse_dict(vv) for vv in v]
            else:
                val = v

            if val is not None:
                req[k] = True

            self.__setattr__(k, val)

        if not all(req.values()):
            # There was a required field that wasn't mapped
            req_fields = ", ".join(r for r in req if not req[r])
            clsname = cls.__name__

            raise Exception("The fields %s were not found when parsing type '%",format(req_fields, clsname))

        return self



