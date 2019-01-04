# -*- coding: utf-8 -*-


def contents(module,include_hidden = False):
    """ Gets a copy-paste ready import statement,
    given a string that represents the name of 
    a module.
    
    Params:
    ------------------------------------------
    module: string
    Name of the module
    include_hidden: bool, default False
    Whether to include 'hidden' functions
    """
    print('from {} import '.format(module),end = '')
    exec("import {}".format(module))
    local_vars = locals()
    exec("package = dir({})".format(module),globals(),local_vars)
    func_string = ""
    for name in local_vars['package']:
        if not name.startswith('_') or include_hidden:
            func_string+=name + ','
    print(func_string[:-1])