from aliu.debug.placeholder import Placeholder
import numpy as np

def assert_origin_inheritance(origin):
    placeholder = Placeholder(origin)
    assert origin is Placeholder.originof(placeholder)
    if origin is None: return
    mclass = origin.__class__
    if mclass is None: return
    assert isinstance(origin, mclass)
    assert isinstance(placeholder, mclass)
    assert isinstance(placeholder, Placeholder)
    if isinstance(origin,Placeholder): return
    assert not isinstance(Placeholder.originof(placeholder), Placeholder)

def test_inheritance():
    origins = [np.random, np, np.random.random, None, Placeholder, Placeholder(type)]
    [assert_origin_inheritance(origin) for origin in origins]
