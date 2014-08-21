
from jbio.coverage import *
from jbio.testframework import ensure_eq

def test_coverage_array_from_ranges(config):
    
    ranges_ok = [ (1, 3),
                  (3, 4),
                  (3, 5) ]

    ranges_ok_expect = [0,1,1,3,2,1]
    
    range_test = ensure_eq(ranges_ok_expect, 
                           coverage_array_from_ranges(ranges_ok))
    
    return range_test

def test_get_marked_ranges(config):
    
    test_arr = [0,0,0,1,1,1,0,0,1,0]
    expected_ranges = [(3,5),(8,8)]
    
    range_test = ensure_eq(expected_ranges,
                           get_marked_ranges(test_arr))
    
    return range_test
    
