
from jbio.sequence import *

from jbio.testframework import ensure_eq

def test_window_iterator(config):
    seq = "AAAAC"
    expected_windows = ["AAA","AAA","AAC"]
    expected_windows2 = ["AAA","AAC"]
    test1 = ensure_eq( expected_windows,
                       list(window_iterator(seq, 3)))
    test2 = ensure_eq( expected_windows2,
                       list(window_iterator(seq,3,2)))
    return [test1, test2]

def test_percent_gc(config):
    
    seq = "AAACCCGGG"
    expected_pcts = [float(1)/4,
                       float(2)/4,
                       float(3)/4,
                       float(4)/4,
                       float(4)/4,
                       float(4)/4]
    return ensure_eq(expected_pcts,
                     map(percent_gc, 
                         window_iterator(seq,4)))
    
