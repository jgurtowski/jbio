#!/usr/bin/env python

import sys

from itertools import imap

from jbio.io.file import iterator_over_file
from jbio.fasta import record_iterator as fasta_iterator

##Create Kmers

if not len(sys.argv) == 3:
    sys.exit("Usage: kmer.py k-size in.fa\n")

fn = sys.argv[2]
ksize = int(sys.argv[1])

for record in fasta_iterator(iterator_over_file(fn)):
    seq = record.seq
    starts = range(len(seq)-ksize+1)
    kmers = imap(lambda start: seq[start:start+ksize], starts)
    for kmer in kmers:
        print kmer
