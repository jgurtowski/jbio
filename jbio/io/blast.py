from itertools import chain
from collections import namedtuple

from jbio.io.file import line_record_iterator

Blast6SeqRecord = namedtuple('Blast6SeqRecord',["qname","sname","pctid",
                                                "length","mismatch","gapopen",
                                                "qstart","qend","sstart",
                                                "send", "evalue","bitscore",
                                                "qlen","slen","qseq","sseq"])

Blast6SeqTypes = [str, str, float, int, int, int, int, int ,int, int,
                  float, float, int, int, str, str]


Blast6Record = namedtuple('Blast6Record',["qname","sname","pctid",
                                          "length","mismatch","gapopen",
                                          "qstart","qend","sstart",
                                          "send", "evalue","bitscore",
                                          "qlen","slen"])

Blast6Types = [str, str, float, int, int, int, int, int ,int, int,
               float, float, int, int]


def record_iterator(string_iterable):
    '''
    @param string_iterable iterable containing string versions of records
    
    @return iterator over records
    '''
    try:
        first_record = string_iterable.next()
    except StopIteration:
        return []

    nfields = len(first_record.split())
    h = { len(Blast6Types): (Blast6Record, Blast6Types),
          len(Blast6SeqTypes): (Blast6SeqRecord, Blast6SeqTypes)}
    btypes = h.get(nfields)
    if not btypes:
        raise Exception, "Not a valid blast string iterable"
    
    return line_record_iterator(btypes[0],btypes[1], chain([first_record],
                                                           string_iterable))
