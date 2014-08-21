##
## Functions related to sequence
##

import re
from collections import Counter

def window_iterator(sequence, window_size, step=1):
    '''
    @param sequence sequence to generate windows from
    @param window_size size of the windows to generate
    @param step step size between windows
    @return iterator over the windows
    '''
    yield sequence[:window_size]
    start = step
    while start + window_size <= len(sequence):
        yield sequence[start:start+window_size]
        start += step
    

def percent_gc(sequence):
    '''Simply calculates the percentage of GC'''
    uppercase_seq = sequence.upper()

    checker = re.compile('^[ACGTN]+$')
    if not checker.match(sequence):
        raise Exception("Sequence invalid, only accepts 'ACGTN'")
    
    counts = Counter(sequence)
    return (counts['G']+counts['C']) / float(sum(counts.values()))
