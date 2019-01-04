from aliu.debug.placeholder import Placeholder, add_placeholder, originof
import numpy as NUMPY_ORIGINAL_POINTER
np = NUMPY_ORIGINAL_POINTER

# Also tests whether callable functions work
def np_random(seed=42):
    np.random.seed(seed)
    random_array = np.random.random(100)
    return random_array

def assert_rand_arrays(revert = originof):
    global np
    array1 = np_random()
    np = revert(np)
    assert np is NUMPY_ORIGINAL_POINTER
    assert (array1 == np_random()).all()

def test_basic():
    global np
    np = Placeholder(NUMPY_ORIGINAL_POINTER)
    assert_rand_arrays()

def test_class_init():
    rs = Placeholder(np.random.RandomState)
    Placeholder.self_compatible_inheritance = True
    assert isinstance(rs(), rs)
    Placeholder.self_compatible_inheritance = False
    assert isinstance(rs(), np.random.RandomState)

def test_callable():
    original = np.random.random
    np.random.random = Placeholder(np.random.random)
    def revert(numpy):
        numpy.random.random = originof(numpy.random.random)
        return numpy
    assert_rand_arrays(revert)

def test_add_placeholder():
    realrandom = np.random
    remove_placeholder = add_placeholder(np,'random')
    assert np.random is not realrandom
    def revert(numpy):
        global np
        remove_placeholder()
        return np
    assert_rand_arrays(revert=revert)
