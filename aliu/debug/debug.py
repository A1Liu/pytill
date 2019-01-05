import inspect, traceback, logging, subprocess, hashlib, os

def debug(*args,**kwargs):
    frameinfo = inspect.getframeinfo( inspect.currentframe().f_back )
    path = frameinfo.filename
    print('Debug statement at line %s in %s' % (frameinfo.lineno, path ) )
    print(*args,**kwargs)

def md5(string):
    m = hashlib.md5()
    m.update(string)
    return m.digest()

def get_tups(lines, base, n):
    if base >= len(lines):
        raise IndexError
    line_tups = []
    [line_tups.append( tuple(lines[ (base-i):(base+1) ]) ) for i in range(min(n,base+1))]
    return line_tups

def handle_exception(*args, **kwargs):
    exception, frame_object = args[0:2]
    args = args[2:]
    frameinfo = inspect.getframeinfo( frame_object )
    lines = traceback.format_exc().strip().split('\n')[3:]
    tb_str = '\n'.join(lines)

    print( "File \"%s\", line %s:" % (frameinfo.filename, frameinfo.lineno) )
    source = None if frameinfo.code_context is None else frameinfo.code_context[0].strip()
    print( "  Source:\n    %s" %  source )
    print( "  Traceback (most recent call last):\n    %s" % tb_str.replace('\n','\n  ').strip() )

def tryfail(*args, **kwargs):
    try:
        func = args.pop(0)
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

def getLogger(name,level = None):
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    return logger

def getsource(obj):
	return inspect.getsource(obj)

def getfile(obj):
	return inspect.getfile(obj)

def atom(file_name):
	subprocess.call(['open','-a','Atom',os.path.abspath(file_name)])

def editsource(obj):
	atom(getfile(obj))
