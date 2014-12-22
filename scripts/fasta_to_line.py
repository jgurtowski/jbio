#!/usr/bin/env python

import sys

from jbio.io.file import iterator_over_file
from jbio.fasta import record_iterator as fasta_iterator

if not len(sys.argv) == 2:
    sys.exit("fasta_to_line.py in.fa")


for record in fasta_iterator(iterator_over_file(sys.argv[1])):
    print "\t".join([record.name, record.seq])
