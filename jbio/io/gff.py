##
#
##

from collections import namedtuple
from itertools import ifilter
from jbio.io.file import line_record_iterator

GFFRecord_t = namedtuple("GFF_Record_t",
                          ["seqname",
                           "source",
                           "feature",
                           "start",
                           "end",
                           "score",
                           "strand",
                           "frame",
                           "attribute"])
GFFRecord_types = [str, str,str, int, int, float,
                   str, int, str]


def record_iterator(string_iterable):
    '''@param string_iterable iterable containing
    string versions of records
    
    @return iterator over the records
    '''
    
    filter_func = lambda l: not l.startswith("#")

    return line_record_iterator(GFFRecord_t,
                                GFFRecord_types,
                                ifilter(filter_func,
                                        string_iterable))

