#!/usr/bin/env python

##Converts a fasta file
#To fastq by just using 'I' for quality

import sys
from jbio.io.file import iterator_over_file
from jbio.fasta import record_iterator as fasta_iterator
from jbio.fastq import FastqRecord, record_to_string as fq_to_str

QUAL_STR = "I"

if not len(sys.argv) == 2:
    sys.exit("fastaToFastq.py in.fa \n")

for record in fasta_iterator(iterator_over_file(sys.argv[1])):
    print fq_to_str(FastqRecord(record.name, record.seq, "",
                                QUAL_STR * len(record.seq)))
