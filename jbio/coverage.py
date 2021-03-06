import operator
from itertools import count, compress
from functools import partial
from operator import itemgetter

def coverage_array_from_ranges(ranges, max_len=None, 
                               start_getter=itemgetter(0),
                               end_getter=itemgetter(1),
                               update_func=lambda _,y : y+1,
                               initial_array_val=0):
    '''Takes a list of ranges (start, end) (alignment positions)
    and returns a list that has the coverage at each position
    If ranges is not a tuple, supply start_getter and end_getter
    so we can get the start and end

    update_func updates the coverage values
                it should take two params, the current range object
                and the array value to be updated (old value)
                It should return a new value for the array element
                
    start and end begin from 0 and are inclusive
    '''
    
    cov_arr = [initial_array_val] * max_len if max_len else []
    for r in ranges:
        start, end = start_getter(r), end_getter(r)
        if start > end:
            start, end = end, start
        if start < 0 or end < 0:
            raise "Start or End less than 0"
        if max_len and (start > max_len or end > max_len):
            raise "Start or End is greater than max_len %d" % max_len
        
        if end >= len(cov_arr):
            cov_arr += [initial_array_val] * ((end-len(cov_arr)) + 1)
        
        for i in range(start,end+1,1):
            cov_arr[i] = update_func(r, cov_arr[i])

    return cov_arr


def pairwise(iterable,func=operator.add):
    it = iter(iterable)
    prev = next(it)
    for el in it:
        yield func(el,prev)
        prev = el


def accumulate_mod(iterable, func=operator.add):
    it = iter(iterable)
    total = next(it)
    yield total
    for element in it:
        if element == 0:
            total = 0
        else:
            total = func(total,element)
        yield total

def get_marked_ranges(arr):
    '''Takes an array v with wanted elements marked as 1
    all other elements are 0. This function returns
    the index ranges of these 1's'''
    
    #subtract adjacent elements to find -1
    #flip these to 1's and change everything else to 0
    #so that we can use it to find the index
    breaks = map(lambda x: 1 if x == -1 else 0 , pairwise(arr + [0],operator.sub))

    #create a cumsum of the inverse to know how many elements
    #are a part of this region
    lengths = accumulate_mod(arr)

    #zip up the indexes with the lengths
    z = zip(count(),list(lengths))

    #use the breaks to select only the indexes we want
    #and use the cumsum to know how many elements came
    #previously
    endAndLength = compress(z,breaks)

    return map(lambda (e,l): (e-l+1,e), endAndLength)

    
    





