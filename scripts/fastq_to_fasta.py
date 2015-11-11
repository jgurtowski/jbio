#!/usr/bin/env python

import sys

from itertools import chain, imap

from jbio.io.file import iterator_over_file
from jbio.fastq import record_iterator as fastq_record_iterator
from jbio.functional import compose

if len(sys.argv) < 2:
    sys.exit("fastq_to_fasta.py in.fq [in.fq ..]\n")

fastq_file = compose(fastq_record_iterator, iterator_over_file)

fastq_stream = chain.from_iterable(imap(fastq_file, sys.argv[1:]))

for record in fastq_stream:
    print ">" + record.name
    print record.seq
