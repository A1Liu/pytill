__uid_attr__ = '__ph_uid__'
__origin_attr__ = '__ph_origin__'
__dict_attr__ = '__ph_dict__'
__logger_kw_attr__ = '__ph_logger__'
__counter__ = 0

def base_obj_summary(obj):
    name = obj.__name__+' ' if hasattr(obj,'__name__') else ''
    return f"<{name}'{obj.__class__.__name__}' object>"
def summarize_obj(obj):
    return str(obj) if len(str(obj)) < 30 else base_obj_summary(obj)
def ph_fmt(origin, id):
    return f'<Placeholder object uid="{id}" origin="{origin}">'
