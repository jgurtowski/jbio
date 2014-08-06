from __future__ import print_function


import functools
from functools import partial
from itertools import groupby, imap, repeat, izip, starmap, count, ifilter
from operator import itemgetter, eq, neg
from collections import namedtuple


from jbio.functional import compose
from jbio.misc import reverse_complement
from jbio.io.file import record_to_string

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
    len_aln = lambda a : eg(a) - sg(a) + 1
    is_rev = lambda a : start_getter(a) > end_getter(a)
    num_matches = lambda a_str, b_str : sum(starmap(eq,izip(a_str,b_str)))
    
    def overlap(x, y):
        end = min(eg(x), eg(y))
        overlap = end - sg(y) + 1
        if overlap < 0:
            overlap = 0
        return overlap
    #overlap = lambda x,y : 0 if eg(x) - sg(y) + 1 < 0 else eg(x) - sg(y) + 1

    def score_getter_in_full(a,b):
        ''' a is always <= b '''
        if a == None or overlap(a,b) == 0:
            return num_matches(b.qseq, b.sseq)
        
        seq_orienter = lambda aln, seq : reverse_complement(seq) if is_rev(aln) else seq
        
        a_q_seq, a_s_seq , b_q_seq, b_s_seq = list(starmap(seq_orienter, [(a,a.qseq),(a,a.sseq),
                                                                 (b,b.qseq),(b,b.sseq)]))
        olap = overlap(a,b)
        a_olap_matches = num_matches(a_q_seq[neg(olap):],a_s_seq[neg(olap):]) * neg(1)
        b_olap_matches = num_matches(b_q_seq[:olap], b_s_seq[:olap]) * 0.5
        b_hang_matches = num_matches(b_q_seq[olap:], b_s_seq[olap:])
        
        score = a_olap_matches + b_olap_matches + b_hang_matches
        
        # print("%s|%d:%d:%s\t%s|%d:%d:%s" % (a.qname,sg(a),eg(a),is_rev(a), b.qname,sg(b),eg(b),is_rev(b)))
        # print("Overlap: %d " % olap)
        # print("Score: %d " % score)
        # print(a_q_seq)
        # print(a_s_seq)
        # pad = " " * (sg(b) - sg(a))
        # print(pad + b_q_seq)
        # print(pad + b_s_seq)
        # print()

        return score

    def score_getter_in(a,b):
        if a == None or overlap(a,b) == 0:
            return len_aln(b) * (b.pctid / 100.0)

        #contained
        olap = overlap(a,b)
        if olap >= len_aln(a):
            return len_aln(a) * neg(1)
        elif olap >= len_aln(b):
            return len_aln(b) * neg(1)

        a_olap_matches = olap * (a.pctid / 100.0) * neg(0.5)
        b_olap_matches = olap * (b.pctid / 100.0) * 0.5
        b_hang_matches = (len_aln(b) - olap) * (b.pctid / 100.0)
        
        score = a_olap_matches + b_olap_matches + b_hang_matches
        
        return score

    def score_getter_in_nucmer(a,b):
        if a == None or overlap(a,b) == 0:
            return len_aln(b) * (b.pctid / 100.0)

        olap = overlap(a,b)
        return (len_aln(b) - olap) * pow((b.pctid / 100.0),2)


    is_contained = lambda a,b : sg(b) >= sg(a) and eg(b) <= eg(a)

    end_sorted = sorted(alignments, key=eg, reverse=True)
    alns = sorted(end_sorted, key=sg)
    
    #remove contained
    contained = [False] * len(alns)
    for i in xrange(len(alns)):
        for j in xrange(i):
            if is_contained(alns[j],alns[i]):
                contained[i] = True
                break
                
    alns = map(itemgetter(1), ifilter(compose(lambda x : not x,itemgetter(0)), izip(contained,alns)))
    
    #initialize lis array
    lis = map(LIS_t._make, izip(imap(partial(score_getter_in,None), alns),
                                repeat(-1)))
    
    #DP
    for i in xrange(len(alns)):
        for j in xrange(i):
            #I guess we should do global
            score = lis[j].score + score_getter_in(alns[j], alns[i])
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
    
    

    


