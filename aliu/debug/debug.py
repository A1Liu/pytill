import inspect, traceback, logging

def debug(*args,**kwargs):
    frameinfo = inspect.getframeinfo( inspect.currentframe().f_back )
    path = frameinfo.filename
    print('Debug statement at line %s in %s' % (frameinfo.lineno, path ) )
    print(*args,**kwargs)

def handle_exception(exception, frame_object, *args, **kwargs):
    frameinfo = inspect.getframeinfo( frame_object )
    tb_str = traceback.format_exc()

    print( "File \"%s\", line %s:" % (frameinfo.filename, frameinfo.lineno) )
    source = None if frameinfo.code_context is None else frameinfo.code_context[0].strip()
    print( "  Source:\n    %s" %  source )
    print( "  Exception:\n    %s" % tb_str.replace('\n','\n    ').strip() )

def tryfail(func, *args, **kwargs):
    try:
        func, handler = func
        if not callable(handler):
            output = handler
            if isinstance(handler, dict):
                handler = lambda e,*args, **kwargs: output[e] if isinstance(e, type) else output[e.__class__]
            else:
                handler = lambda *args, **kwargs: output
    except TypeError:
        handler = handle_exception

    try:
        return func(*args, **kwargs)
    except Exception as e:
        return handler(e, inspect.currentframe().f_back, *args, **kwargs)

def getLogger(name,level):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
