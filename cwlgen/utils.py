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
    The Serializable class contains logic to automatically serialize a class based on
    its attributes. This behaviour can be overridden via the ``get_dict`` method on its
    subclasses with a call to super. Fields can be ignored by the base converter through
    the ``ignore_field_on_convert`` static attribute on your subclass.

    The parsing behaviour (beta) is similar, however it will attempt to set all attributes
    from the dictionary onto a newly initialised class. If your initialiser has required
    arguments, this converter will do its best to pull the id out of the dictionary to provide
    to your initializer (or pull it from the { $id: value } dictionary). Typing hints can be
    provided by the ``parse_types`` static attribute, and required attributes can be tagged
    the ``required_fields`` attribute.
    """


    """
    This is a special field, with format: {fieldName: str, [Serializable]}
    If the field name is present in the dict, then it will call the parse_dict(cls, d)
    method on that type. It should return None if it can't parse that dictionary. This 
    means the type will need to override the ``parse_dict`` method.
    """
    parse_types = {}        # type: {str, [type]}
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
        req_fields = set(self.required_fields or [])

        if hasattr(self, "ignore_attributes") and self.ignore_attributes:
            ignore_attributes = set(self.ignore_attributes)

        if self.ignore_fields_on_convert:
            ignore_attributes = ignore_attributes.union(self.ignore_fields_on_convert)

        for k, v in vars(self).items():
            is_required = k in req_fields
            should_skip = (
                self.should_exclude_object(v)
                or k.startswith("_")
                or k in ignore_attributes
                or k == "ignore_attributes"
            )
            if not is_required and should_skip:
                continue
            s = self.serialize(v)
            if self.should_exclude_object(s):
                continue
            d[k] = s
        return d

    @classmethod
    def parse_dict(cls, d):
        return cls.parse_dict_generic(cls, d)

    @staticmethod
    def parse_dict_generic(T, d, parse_types=None, required_fields=None, ignore_fields_on_parse=None):

        if parse_types is None and hasattr(T, "parse_types"):
            parse_types = T.parse_types
        if required_fields is None and hasattr(T, "required_fields"):
            required_fields = T.required_fields
        if ignore_fields_on_parse is None and hasattr(T, "ignore_fields_on_parse"):
            ignore_fields_on_parse = T.ignore_fields_on_parse

        pts = parse_types
        req = {r: False for r in required_fields}
        ignore = set(ignore_fields_on_parse)

        # may not be able to just initialise blank class
        # but we can use inspect to get required params and init using **kwargs
        try:
            required_init_kwargs = T.get_required_input_params_for_cls(T, d)
            self = T(**required_init_kwargs)
        except Exception as e:
            return None

        for k, v in d.items():
            if k in ignore: continue
            val = T.try_parse(v, pts.get(k))
            if val is None: continue
            if not hasattr(self, k):
                raise KeyError("Key '%s' does not exist on type '%s'" % (k, type(self)))
            self.__setattr__(k, val)
            req[k] = True

        if not all(req.values()):
            # There was a required field that wasn't mapped
            req_fields = ", ".join(r for r in req if not req[r])
            clsname = T.__name__

            raise Exception("The fields %s were not found when parsing type '%s'" % (req_fields, clsname))

        return self

    @classmethod
    def parse_with_id(cls, d, identifier):
        if not isinstance(d, dict):
            raise Exception("parse_with_id will require override to handle default object of type '%s'" % type(d))
        d["id"] = identifier
        return d

    @staticmethod
    def get_required_input_params_for_cls(cls, valuesdict):
        try:
            argspec = inspect.getfullargspec(cls.__init__)
        except:
            # we're in Python 2
            argspec = inspect.getargspec(cls.__init__)

        args, defaults = argspec.args, argspec.defaults
        required_param_keys = set(args[1:-len(defaults)]) if defaults is not None and len(defaults) > 0 else args[1:]

        inspect_ignore_keys = {"self", "args", "kwargs"}
        # Params can't shadow the built in 'id', so we'll put in a little hack
        # to guess the required param name that ends in

        id_field_names = [k for k in required_param_keys if k == "id" or k.endswith("_id")]
        id_field_name = None
        id_field_value = valuesdict.get("id")

        if len(id_field_names) == 1:
            id_field_name = id_field_names[0]
            inspect_ignore_keys.add(id_field_name)
        elif len(id_field_names) > 1:
            print("Warning, can't determine if there are multiple id fieldnames")

        required_init_kwargs = {k: valuesdict[k] for k in required_param_keys if (k not in inspect_ignore_keys)}
        if id_field_name:
            required_init_kwargs[id_field_name] = id_field_value

        return required_init_kwargs

    @staticmethod
    def try_parse(value, types):
        if types is None: return value
        if isinstance(value, (dict, list)) and len(value) == 0: return []

        # If it's an array, we should call try_parse (recursively)

        if isinstance(value, list):
            retval = [Serializable.try_parse(t, types) for t in value]
            invalid_values = get_indices_of_element_in_list([False if v is None else True for v in retval], False)
            if invalid_values:
                invalid_valuesstr = ','.join(str(i) for i in invalid_values)
                invalid_itemstr = ", ".join([str(value[i]) for i in invalid_values])
                raise Exception("Couldn't parse items at indices " + invalid_valuesstr + ", corresponding to: " + invalid_itemstr)
            return retval

        for T in types:
            retval = Serializable.try_parse_type(value, T)
            if retval:
                return retval

        return


    @staticmethod
    def try_parse_type(value, T):
        # We're all good, don't need to do anything
        if not isinstance(T, list) and isinstance(value, T): return value

        # if T is a primitive (str, bool, int, float), just return the T representation of retval
        elif T in _unparseable_types:
            try:
                if isinstance(value, list):
                    return [T(v) for v in value]
                return T(value)
            except:
                return None

        # the type is [T] which is our our indicator that T will be a (list | dictionary) (with key 'id')
        elif isinstance(T, list):
            T = T[0]

            if T in _unparseable_types:
                try:
                    if isinstance(value, list):
                        return [T(v) for v in value]
                    return T(value)
                except:
                    return None
            elif isinstance(value, list):
                return [T.parse_dict(vv) for vv in value]
            elif isinstance(value, dict):
                # We'll need to map the 'id' back in
                retval = []
                for nested_key in value:
                    dd = value[nested_key]
                    retval.append(T.parse_with_id(dd, nested_key))
                return retval
            else:
                raise Exception("Don't recognise type '%s', expected dictionary or list" % type(value))

        # T is the retval, or an array of the values (because some params are allowed to be both
        return T.parse_dict_generic(T, value) if not isinstance(value, list) else [T.parse_dict_generic(T, vv) for vv in value]


def get_indices_of_element_in_list(searchable, element):
    indices = []
    for i in range(len(searchable)):
        if element == searchable[i]:
            indices.append(i)
    return indices


def value_or_default(value, default):
    return value if value is not None else default
