##Framework for running tests

from __future__ import print_function

import sys
import os
import inspect
import importlib
from operator import eq
from collections import namedtuple
from functools import partial

EnsureFailure = namedtuple('EnsureFailure',
                           ['operator','expected','test'])

def ensure(function, expected, test):
    '''ensure, like assert, applies function over 
    expected and test
    and makes sure it is true'''
    def _ensure():
        if not function(expected,test):
            return EnsureFailure(function, expected,test)
        return True

    return _ensure

ensure_eq = partial(ensure,eq)

def run_tests(iterable):
    '''Takes an iterable of tests and runs each one'''
    for test in iterable:
        test_result = test()
        if type(test_result) == EnsureFailure:
            raise Exception, test_result
        else:
            print("Test Passed")

DEFAULT_TEST_CONFIG = {
    "test_data_path": "test_data"
}

def auto_load_tests(package,config=DEFAULT_TEST_CONFIG):
    '''Automatically loads tests from package
    Makes sure __all__ is maintained
    returns a test runner'''
    tests = []
    test_generators = []
    for module in package.__all__:
        module_path = os.path.join(package.__name__, module)
        module_items = importlib.import_module('.'+module, package.__name__)
        for name in dir(module_items):
            if name.startswith("test_"):
                test_generator = getattr(module_items, name)
                test_generators.append(test_generator)
                generated_tests = test_generator(config)
                if type(generated_tests) == type([]):
                    tests += generated_tests
                else:
                    tests.append(generated_tests)
    #filter(print, test_generators)
    return lambda : run_tests(tests)

    





