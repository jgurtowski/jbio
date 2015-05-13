import functools
from itertools import izip, starmap

def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)

def fapply(function, argument):
    '''Just applies a function to its argument'''
    return function(argument)

def zipmap(functions, data):
    return starmap(fapply, izip(functions, data))

def fpass(*args, **kwargs):
    pass

def identity(x):
    return x

def iterApply(func, iterable):
    '''Takes a function and applies that function
        to each iterable in the form of a generator
    '''
    for i in iterable:
        yield func(i)
