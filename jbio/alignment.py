from __future__ import print_function

import functools
from functools import partial
from itertools import groupby, imap, repeat, izip, starmap, count, ifilter
from operator import itemgetter, eq, neg
from collections import namedtuple

from jbio.functional import compose
from jbio.misc import reverse_complement, varfloor
from jbio.io.file import record_to_string

LIS_t = namedtuple('LIS_t', ["score","prev"])

#Alignment functions
Alignment_Functions_t = namedtuple('Alignment_Functions_t',
                                   ['is_reverse',
                                    'directionless_start_end_getters',
                                    'best_scoring_non_overlapping_greedy',
                                    'longest_non_overlapping_greedy',
                                    'remove_contained',
                                    'overlap',
                                    'len_aln',
                                    'score_getter_matching_consensus_estimated',
                                    'score_getter_mummer_scorelocal',
                                    'LIS'])

def alignment_functions(start_getter, end_getter):
    ''' 
    Returns Alignment Functions that are generic with
    respect to the type of alignments passed int
    '''
    
    def is_reverse(a):
        return start_getter(a) > end_getter(a)
    
    def directionless_start_end_getters():
        '''if alignment is reversed, make it so that it's forward'''
        sg = lambda b : end_getter(b) if is_reverse(b) else start_getter(b)
        eg = lambda c : start_getter(c) if is_reverse(c) else end_getter(c)
        return (sg,eg)

    sg,eg = directionless_start_end_getters()

    def best_scoring_non_overlapping_greedy(score_getter, alignment_iterable):
        '''Gets the best scoring non-overlapping alignments
        sections with respect to the query sequence
        @param score_getter function to sort the alignments by score
        larger score is better
        @param alignments list of tuples (start, end)
    
        @return list containing the set of best scoring 
        non-overlapping alignments
        '''    
        sorted_aligns = sorted(alignment_iterable,
                               key=score_getter, reverse=True)

        not_overlap = lambda c, o: eg(c) < sg(o) or sg(c) > eg(o)
        not_overlap_any = lambda a, aln_set : all(map(functools.partial(not_overlap,a), aln_set))
        return functools.reduce( lambda x, y : x + [y] if not_overlap_any(y,x) else x, 
                                 sorted_aligns, [])


    def longest_non_overlapping_greedy(alignment_iterable):
        '''Gets the longest non-overlapping alignment
        sections with respect to the query sequence
        @param alignments list of tuples (start, end)
    
        @return list containing the set of longest non-overlapping alignments
        '''
        alen = lambda a : eg(a) - sg(a)
        return best_scoring_non_overlapping_greedy(alen, alignment_iterable)


    def remove_contained(alignments):
        '''Removes alignments contained within other alignments
        @param alignments list of alignments
        @return list of alignments with contained alignments removed
        '''
    
        is_contained = lambda a,b : sg(b) >= sg(a) and eg(b) <= eg(a)

        #remove contained
        contained = [False] * len(alignments)
        for i in xrange(len(alignments)):
            for j in xrange(i):
                if is_contained(alignments[j],alignments[i]):
                    contained[i] = True
                    break
                
        return map(itemgetter(1), 
                   ifilter(compose(lambda x : not x,itemgetter(0)), 
                           izip(contained,alignments)))
    def len_aln(x):
        return eg(x) - sg(x) + 1

    def overlap(x, y):
        '''Calculates overlap between x and y'''
        return varfloor(0, min(eg(x), eg(y)) - sg(y) + 1)

    def score_getter_matching_consensus_estimated(a, b):
        '''Scoring Function for filtering alignments for downstream
        consensus. Overlaps are sort of encouraged '''
        if a == None or overlap(a,b) == 0:
            return len_aln(b) * (b.pctid / 100.0)

        olap = overlap(a,b)
        a_olap_matches = olap * (a.pctid / 100.0) * neg(0.5)
        b_olap_matches = olap * (b.pctid / 100.0) * 0.5
        b_hang_matches = (len_aln(b) - olap) * (b.pctid / 100.0)
        
        score = a_olap_matches + b_olap_matches + b_hang_matches
    
        return score

    def score_getter_mummer_scorelocal( a, b):
        '''Similar to ScoreLocal in deltafilter'''
        if a == None or overlap(a,b) == 0:
            return len_aln(b) * (b.pctid / 100.0)

        return (len_aln(b) - overlap(a,b)) * pow((b.pctid / 100.0),2)

    def LIS(score_getter, alignments):
        '''Score getter takes two alignments and returns a score,
           Should probably choose from the above scoring functions'''
    
        end_sorted = sorted(alignments, key=eg, reverse=True)
        alns = sorted(end_sorted, key=sg)
    
        #initialize lis array
        lis = map(LIS_t._make, izip(imap(partial(score_getter,None), alns),
                                repeat(-1)))
        #DP
        for i in xrange(len(alns)):
            for j in xrange(i):
                ##Score getter needs to know about how it's being used (Oh well)
                score = lis[j].score + score_getter(alns[j], alns[i])
                if score > lis[i].score:
                    lis[i] = LIS_t(score, j)
                
        #traceback
        max_pos, _ = max(enumerate(lis), key=itemgetter(1))
        tb = [False] * len(alns)
        cur_max = max_pos
        while True:
            tb[cur_max] = True
            cur_max = lis[cur_max].prev
            if cur_max == -1:
                break
    
        #filter(print, imap(lambda x: "\t".join(map(str,x)) , izip(count(),tb,lis,imap(record_to_string,alns))))
        return filter(itemgetter(0), izip(tb,lis,alns))


    #END - get_alignment_functions
    return Alignment_Functions_t(is_reverse,
                                 directionless_start_end_getters,
                                 best_scoring_non_overlapping_greedy,
                                 longest_non_overlapping_greedy,
                                 remove_contained,
                                 overlap,
                                 len_aln,
                                 score_getter_matching_consensus_estimated,
                                 score_getter_mummer_scorelocal,
                                 LIS)

def group(key_func, alignment_iterable):
    '''
    Groups alignments by key_func, only returns the groups
    as an iterable
    '''
    return imap(compose(list,itemgetter(1)), 
                groupby(alignment_iterable, 
                        key=key_func))



    
    

    


