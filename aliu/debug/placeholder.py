from .debug import getLogger, tryfail
from .placeholder_utils import __uid_attr__, __origin_attr__, __dict_attr__, \
__logger_kw_attr__, __counter__
from .placeholder_utils import base_obj_summary,summarize_obj,ph_fmt
import logging

# Utils
ph_super = lambda placeholder: super(Placeholder, placeholder)
ph_getattr =   lambda ph,attr: ph_super(ph).__getattribute__( attr )

# Get placeholder attributes
originof = lambda placeholder: ph_getattr(placeholder,__origin_attr__)
dictof =   lambda placeholder: ph_getattr(placeholder,__dict_attr__)
uidof =    lambda placeholder: dictof(placeholder).get(__uid_attr__)
loggerof = lambda placeholder: dictof(placeholder).get(__logger_kw_attr__)

# Convert placeholder to string
def repr_ph(placeholder):
    return ph_fmt( summarize_obj(originof(placeholder)),uidof(placeholder) )
def ph_logger_name(origin, id):
    return ph_fmt( base_obj_summary(origin),id )

def placeholder_silent(origin,**kwargs):
    uid = Placeholder.get_uid()
    logger = getLogger(ph_logger_name(origin, uid),kwargs.pop('level',logging.WARNING))
    prop_dict = {
        __uid_attr__:uid, # Easier to implement when this is in the dictionary
        # Also allows for editing later.
        __logger_kw_attr__:logger, **kwargs}
    output = Placeholder(output,**prop_dict)

def decorate_callable(placeholder, func):
    def decorated(*args, **kwargs):
        output = func(*args, **kwargs)
        if output is not None:
            uid = Placeholder.get_uid()
            logger = getLogger(ph_logger_name(output, uid),logging.WARNING)
            kwargs = {
                '__class__':placeholder,
                __uid_attr__:uid, # Easier to implement when this is in the dictionary
                # Also allows for editing later.
                __logger_kw_attr__:logger }
            output = Placeholder(output,**kwargs)
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

def log_func(*args, **kwargs):
    func, placeholder, message = args[0:3]
    args[:] = args[3:]
    output = func(*args, **kwargs)
    loggerof(placeholder).debug( message.replace( '%(output)s',str(summarize_obj(output)) ) )
    return output

class Placeholder(): # TODO Add unique id function
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

    self_compatible_inheritance = True
    originof = staticmethod(originof)
    dictof = staticmethod(dictof)

    @staticmethod
    def get_uid(): # Returns a unique id
        global __counter__
        __counter__+=1
        return __counter__

    def __init__(self, origin, **kwargs):
        ph_super(self).__setattr__( __origin_attr__, origin )
        prop_dict = {__uid_attr__:Placeholder.get_uid(), **kwargs}
        if __logger_kw_attr__ not in prop_dict:
            logger_name = ph_logger_name(origin, prop_dict[__uid_attr__])
            prop_dict[__logger_kw_attr__] = getLogger( logger_name )
        ph_super(self).__setattr__( __dict_attr__, prop_dict )
        loggerof(self).debug(f"INIT: Placeholder({summarize_obj(origin)},**{kwargs})")

    def __delattr__(self, name):
        message =  f"DEL: {summarize_obj(originof(self))}.{name}"
        return log_func(originof(self).__delattr__, self, message, name)

    def __setattr__(self, name, value):
        message = f"SET: {name}={value}"
        if name in dictof(self):
            return log_func(dictof(self).update, self, message, {name:value})
        return log_func(setattr, self, message, originof(self), name, value)

    def __call__(self, *args, **kwargs):
        message = f"CALL: (*args={args}, **kwargs={kwargs}) returned %(output)s"
        return log_func(callable_from(self), self, message, *args, **kwargs)

    def __getattribute__(self, attribute):
        prop_dict = dictof(self)
        message = f"GET: {summarize_obj(originof(self))}.{attribute}=%(output)s"
        if attribute == __dict_attr__:
            return log_func(lambda: prop_dict, self, message )
        if attribute in prop_dict: return log_func(dictof(self).get, self, message, attribute )
        return log_func(getattr, self, message, originof(self), attribute )

    def __new__(*args, **kwargs):
        output = log_func(originof(self).__new__,self, f"NEW: (*args={args}, **kwargs={kwargs})", *args, **kwargs)
        return Placeholder(output,)

    def __eq__(self, value):
        return log_func(originof(self).__eq__,self, f"EQ: self=={value} is %(output)s", value)
    def __ge__(self, value):
        return log_func(originof(self).__ge__,self, f"GE: self>={value} is %(output)s", value)
    def __gt__(self, value):
        return log_func(originof(self).__gt__,self, f"GT: self>{value} is %(output)s", value)
    def __le__(self, value):
        return log_func(originof(self).__le__,self, f"LE: self<={value} is %(output)s", value)
    def __lt__(self, value):
        return log_func(originof(self).__lt__,self, f"LT: self<{value} is %(output)s", value)
    def __ne__(self, value):
        return log_func(originof(self).__ne__,self, f"NE: self!={value} is %(output)s", value)


    ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
    # TODO __eq__ for self==value

    def __getitem__(self, key):
        return log_func(originof(self).__getitem__, self, f"GETITEM: self[{key}]=%(output)s", key)
    def __setitem__(self, key, value):
        log_func(originof(self).__setitem__, self,f"SETITEM: self[{key}]={value}", key, value )
    def __delitem__(self, key):
        log_func(originof(self).__delitem__, self, f"DELITEM: del self[{key}]", key )
    def __repr__(self):
        return repr_ph(self)
    def __str__(self):
        return str(originof(self))
