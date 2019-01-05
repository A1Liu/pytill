from aliu.debug.placeholder import Placeholder
from aliu.debug.debug import *

def add_placeholder(obj, attribute):
    # Usage:
    # remove_placeholder = add_placeholder(my_object, 'my_object_attribute')
    # # Do something with the object
    # remove_placeholder()
    origin = getattr(obj, attribute)
    placeholder = Placeholder(origin)
    setattr(obj, attribute, placeholder)
    return lambda: setattr(obj, attribute, origin)
