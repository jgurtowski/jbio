#!/usr/bin/env python

#Strips off the range of an alignment for a reads in blasr m4 format
#for use with cmd line filtering tools

import sys

from jbio.io.file import iterator_over_file

if len(sys.argv) == 1:
    infh = sys.stdin
else:
    infh = iterator_over_file(sys.argv[1])
    

for line in infh:
    arr = line.strip().split()
    slash_split = arr[0].split("/")
    if "_" in slash_split[-2]:
        print "\t".join(["/".join(slash_split[:-1]) , slash_split[-1]] + arr[1:])
    else:
        print "\t".join(["/".join(slash_split), slash_split[-1]] + arr[1:])
