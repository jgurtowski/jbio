from __future__ import print_function


import functools
from functools import partial
from itertools import groupby, imap, repeat, izip
from operator import itemgetter
from collections import namedtuple

from jbio.functional import compose

LIS_t = namedtuple('LIS_t', ["score","prev"])

def directionless_start_end_getters(start_getter, end_getter):
    '''if alignment is reversed, make it so that it's forward'''

    is_rev = lambda a : start_getter(a) > end_getter(a)
    sg = lambda b : end_getter(b) if is_rev(b) else start_getter(b)
    eg = lambda c : start_getter(c) if is_rev(c) else end_getter(c)

    return (sg,eg)

def best_scoring_non_overlapping(start_getter, end_getter, score_getter,
                                 alignment_iterable):
    '''Gets the best scoring non-overlapping alignments
    sections with respect to the query sequence

    @param start_getter function to get the start of the alignment
    @param end_getter function to get the end of the alignment
    @param score_getter function to sort the alignments by score
                        larger score is better
    @param alignments list of tuples (start, end)
    
    @return list containing the set of best scoring 
    non-overlapping alignments
    '''    
    sg,eg = directionless_start_end_getters(start_getter, end_getter)
    
    sorted_aligns = sorted(alignment_iterable,
                           key=score_getter, reverse=True)

    not_overlap = lambda c, o: eg(c) < sg(o) or sg(c) > eg(o)
    not_overlap_any = lambda a, aln_set : all(map(functools.partial(not_overlap,a), aln_set))
    return functools.reduce( lambda x, y : x + [y] if not_overlap_any(y,x) else x, 
                             sorted_aligns, [])


def longest_non_overlapping(start_getter, end_getter, alignment_iterable):
    '''Gets the longest non-overlapping alignment
    sections with respect to the query sequence

    @param start_getter function to get the start of the alignment
    @param end_getter function to get the end of the alignment
    @param alignments list of tuples (start, end)
    
    @return list containing the set of longest non-overlapping alignments
    '''
    alen = lambda a : eg(a) - sg(a)
    return best_scoring_non_overlapping(start_getter, end_getter,
                                        alen, alignment_iterable)



def group(key_func, alignment_iterable):
    '''
    Groups alignments by key_func, only returns the groups
    as an iterable
    '''
    
    return imap(compose(list,itemgetter(1)), 
                groupby(alignment_iterable, 
                        key=key_func))




def LIS(start_getter, end_getter, score_getter, alignments):
    '''Score getter takes two alignments and returns a score'''


    sg,eg = directionless_start_end_getters(start_getter, end_getter)
    len_aln = lambda a : end_getter(a) - start_getter(a) + 1

    def score_getter_in(a,b):
        if a == None:
            olap = 0
        else:
            olap = eg(a) - sg(b)
            olap = 0 if olap < 0 else olap
        
        blen = eg(b) - sg(b)

        return (blen - olap) * pow((b.pctid / 100.0),2)
        
    alns = sorted(alignments, key=sg)
    
    #initialize lis array
    lis = map(LIS_t._make, izip(imap(partial(score_getter_in,None), alns),
                                repeat(-1)))
    
    n = len(alns)
    #DP
    for i in xrange(n):
        for j in xrange(i):
            #I guess we should do global
            score = lis[j].score + score_getter_in(alns[j], alns[i])
            if score > lis[i].score:
                lis[i] = LIS_t(score, j)
                
    #traceback
    max_pos, _ = max(enumerate(lis), key=itemgetter(1))
    tb = [False] * n
    cur_max = max_pos
    while True:
        tb[cur_max] = True
        cur_max = lis[cur_max].prev
        if cur_max == -1:
            break
    
    return filter(itemgetter(0), izip(tb,lis,alns))
    
    

    


