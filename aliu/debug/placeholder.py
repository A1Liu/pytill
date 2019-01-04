from .debug import getLogger as getLogger_basic, tryfail
import logging,re

__origin_attr__ = '__ph_origin__'
__dict_attr__ = '__ph_dict__'
__logger_kw_attr__ = '__ph_logger__'

origin_format_string  = '<Placeholder object origin="%s">'
logging_format_string = '%(levelname)s: %(name)s:\n  %(message)s'
remove_path = re.compile(r'<.*?origin=')
DelAttr = lambda: None # This class should never be instanced

ph_super = lambda placeholder: super(Placeholder, placeholder)
ph_getattr =   lambda ph,attr: ph_super(ph).__getattribute__( attr )
originof = lambda placeholder: ph_getattr(placeholder,__origin_attr__)
dictof = lambda placeholder: ph_getattr(placeholder,__dict_attr__)
loggerof = lambda placeholder: dictof(placeholder).get(__logger_kw_attr__)
repr_origin =   lambda origin: origin_format_string % summarize_obj(origin)
repr_ph =  lambda placeholder: repr_origin( originof(placeholder) )

def summarize_obj(obj):
    name = tryfail((lambda x: x.__name__, 'Unnamed'), obj)
    type = obj.__class__.__name__
    return "%s %s object" % (name, type)


def getLogger(obj, level = logging.DEBUG):
    name = repr_ph(obj) if isinstance(obj, Placeholder) else obj
    return getLogger_basic(name,level)

def decorate_callable(placeholder, func):
    def decorated(*args, **dict):
        output = func(*args, **dict)
        if output is not None:
            logger = getLogger(repr_origin(output),loggerof(placeholder).level+1)
            output = Placeholder(output,**{'__class__': placeholder, __logger_kw_attr__:logger})
        return output
    return decorated

def callable_from(placeholder):
    dict = dictof(placeholder)
    obj = dict.get('__call__') if '__call__' in dict else originof(placeholder)
    if isinstance(obj, type):
        should_decorate = Placeholder.self_compatible_inheritance
        return decorate_callable(placeholder, obj) if should_decorate else obj
    else:
        return obj.__call__

def setorigin(placeholder, origin):
    ph_super(placeholder).__setattr__(__origin_attr__, origin )

def setdict(placeholder, dict):
    if __logger_kw_attr__ not in dict: dict[__logger_kw_attr__] = getLogger(placeholder)
    ph_super(placeholder).__setattr__(__dict_attr__, dict )

def log_func(func, placeholder, message, *args, **kwargs):
    output = func(*args, **kwargs)
    loggerof(placeholder).debug( message.replace( '%(output)s',str(output) ) )
    return output

class Placeholder():
    """
    Placeholder Class
    General concept is that instances of this class replace an existing object
    and imitate it - using the placeholder will be akin to using the initial object,
    except that the placeholder gives you the ability to look into module internals.

    NOTE: Currently works kinda weirdly with inheritance and the isinstance builtin.
    The Placeholder.self_compatible_inheritance option allows for the following customization:
    ph = Placeholder(list)
    Placeholder.self_compatible_inheritance = True # Default value
    assert isinstance(ph(), ph)
    Placeholder.self_compatible_inheritance = False
    assert isinstance(ph(), list)
    """

    logging_format_string = logging_format_string
    self_compatible_inheritance = True
    originof = staticmethod(originof)
    dictof = staticmethod(dictof)

    def __init__(self, origin, **kwargs):
        setorigin(self, origin)
        setdict(self, kwargs)
        loggerof(self).debug(f"Initialized placeholder for object '{origin}' with {__dict_attr__}={kwargs}")

    def __setattr__(self, name, value):
        message = f" attribute '{name}' set to '{value}'"
        if name in dictof(self):
            return log_func(dictof(self).update, self, "Keyword"+message, {name:value})
        return log_func(setattr, self, "Object"+message, originof(self), name, value)

    def __call__(self, *args, **kwargs):
        func = callable_from(self)
        func_type = "Kwarg override" if '__call__' in dictof(self) else "Model"
        message = f"Function call with (*args={args}, **kwargs={kwargs}): " + \
                  f"{func_type} called with output '%(output)s'"
        return log_func(callable_from(self), self, message, *args, **kwargs)

    def __getattribute__(self, attribute):
        prop_dict = dictof(self)
        if attribute == __dict_attr__:
            return log_func(lambda: prop_dict, self, f"Retrieved '{attribute}' (Placeholder property dictionary)." )
        message = f"Retrieved <origin>.{attribute} with value '%(output)s'"
        if attribute in prop_dict:
            return log_func(dictof(self).get, self, message, attribute )
        return log_func(getattr, self, message, originof(self), attribute )

    def __getitem__(self, key):
        return log_func(originof(self).__getitem__, self, f"Retrieved item '%(output)s' using key '{key}'", key)
    def __setitem__(self, key, value):
        log_func(originof(self).__setitem__, self,f"Set item '{key}' to value '{value}'", key, value )
    def __delitem__(self, key):
        logfunc(originof(self).__delitem__, self, f"Deleted item from <origin> using key '{key}'", key )
    def __repr__(self):
        return repr_ph(self)
    def __str__(self):
        return str(originof(self))

def add_placeholder(obj, attribute):
    # Usage:
    # remove_placeholder = add_placeholder(my_object, 'my_object_attribute')
    # # Do something with the object
    # remove_placeholder()
    origin = getattr(obj, attribute)
    placeholder = Placeholder(origin)
    setattr(obj, attribute, placeholder)
    return lambda: setattr(obj, attribute, origin)
