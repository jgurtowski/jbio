#!/usr/bin/env python

import sys

from operator import itemgetter, attrgetter
from itertools import imap

from jbio.io.file import iterator_over_file
from jbio.io.blast import record_iterator as blast_record_iterator
from jbio.alignment import group

if not len(sys.argv) == 2:
    sys.exit("percent.py input.blast6.q")

ifile = iterator_over_file(sys.argv[1])
alignments = blast_record_iterator(ifile)
grouped_alns = group(itemgetter(0), alignments)

for record_group in grouped_alns:
    record_group = list(record_group)
    length_getter = lambda r: r.qend - r.qstart if r.qstart < r.qend else r.qstart - r.qend
    trans_len = record_group[0].qlen
    name = record_group[0].qname
    aln_lengths_sum = sum(imap(length_getter, record_group))
    print name, aln_lengths_sum / float(trans_len)
