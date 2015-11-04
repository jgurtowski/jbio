#!/usr/bin/env python

import sys

from itertools import imap,chain

from jbio.io.file import iterator_over_file_from_extension as ioffe

if not len(sys.argv) >= 2:
    sys.exit("fastq_to_line.py in.fq [in2.fq ...]")


fastq_iterators = imap(ioffe, sys.argv[1:])

for record in chain.from_iterable(fastq_iterators):
    print "\t".join([record.name, record.desc, record.seq, record.qual])
                 


