from .debug import getLogger as getLogger_basic, tryfail
import logging,re

__origin_attr__ = '__ph_origin__'
__kwargs_attr__ = '__ph_kwargs__'
__logger_kw_attr__ = '__ph_logger__'

origin_format_string  = '<Placeholder object origin="%s">'
logging_format_string = '%(levelname)s: %(name)s:\n  %(message)s'
remove_path = re.compile(r'<.*?origin=')
DelAttr = lambda: None # This class should never be instanced

ph_super = lambda placeholder: super(Placeholder, placeholder)
ph_getattr =   lambda ph,attr: ph_super(ph).__getattribute__( attr )
originof = lambda placeholder: ph_getattr(placeholder,__origin_attr__)
kwargsof = lambda placeholder: ph_getattr(placeholder,__kwargs_attr__)
loggerof = lambda placeholder: kwargsof(placeholder).get(__logger_kw_attr__)
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
    def decorated(*args, **kwargs):
        output = func(*args, **kwargs)
        if output is not None:
            logger = getLogger(repr_origin(output),loggerof(placeholder).level+1)
            output = Placeholder(output,**{'__class__': placeholder, __logger_kw_attr__:logger})
        return output
    return decorated

def callable_from(placeholder):
    kwargs = kwargsof(placeholder)
    obj = kwargs.get('__call__') if '__call__' in kwargs else originof(placeholder)
    if isinstance(obj, type):
        should_decorate = Placeholder.self_compatible_inheritance
        return decorate_callable(placeholder, obj) if should_decorate else obj
    else:
        return obj.__call__

def fail_handler(placeholder):
    def handler(e,*args,**kwargs):

def setorigin(placeholder, origin):
    ph_super(placeholder).__setattr__(__origin_attr__, origin )

def setkwargs(placeholder, kwarg_dict):
    origin = originof( placeholder )
    kwargs = { '__class__':origin.__class__, **kwarg_dict}
    if __logger_kw_attr__ not in kwargs: kwargs[__logger_kw_attr__] = getLogger(placeholder)
    kwargs = {key:value for key,value in kwargs.items() if value is not DelAttr}
    ph_super(placeholder).__setattr__(__kwargs_attr__, kwargs )

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
    kwargsof = staticmethod(kwargsof)

    def __init__(self, origin, **kwargs):
        setorigin(self, origin)
        setkwargs(self, kwargs)
        loggerof(self).debug(f"Initialized placeholder for object '{origin}' with kwargs={kwargs}")

    def __getitem__(self, key):
        output = originof(self).__getitem__(key)
        loggerof(self).debug(f"Retrieved item '{output}' using key '{key}'")
        return output
    def __setitem__(self, key, value):
        originof(self).__setitem__(key,value)
        loggerof(self).debug(f"Set item '{key}' to value '{value}'")
    def __delitem__(self, key):
        value = originof(self).__getitem__(key)
        originof(self).__delitem__(key)
        loggerof(self).debug(f"Deleted item '{value}' using key '{key}'")

    def __setattr__(self, name, value):
        log,_ = ( "Keyword",kwargsof(self).update({name:value}) ) if name in kwargsof(self) \
                else ( "Model",setattr(originof(self), name, value) )
        loggerof(self).debug("%s attribute '%s' set to '%s'" % (log, name, value) )

    def __call__(self, *args, **kwargs):
        func = callable_from(self)
        output = func(*args, **kwargs)
        message = "Function call with (*args=%s, **kwargs=%s):\n  %s called with output '%s'"
        func_type = "Kwarg override" if '__call__' in kwargsof(self) else "Model"
        loggerof(self).debug(message % (args, kwargs, func_type, output) )
        return output

    def __getattribute__(self, attribute):
        output = kwargsof(self).get(attribute) if attribute in kwargsof(self) \
                else getattr( originof(self), attribute )
        loggerof(self).debug("Attribute '%s' retrieved with value '%s'" % (attribute, output) )
        return output

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
