#!/usr/bin/env python

#join on db field

import sys
from itertools import imap

if not len(sys.argv) >= 3 :
    print "join.py db file.txt [leave missing(true,false)]"
    sys.exit(1)

with open(sys.argv[1]) as dbfh:
    sys.stderr.write("Loading db ...\n")
    db = dict(imap(lambda line: (line.strip().split()[0],"\t".join(line.strip().split()[1:])),dbfh))
    sys.stderr.write("done\n")

ignore = False
if(len(sys.argv) > 3):
    ignore = "true" == sys.argv[3]

infh = open(sys.argv[2])
with open(sys.argv[2]) as infh:
    for line in infh:
        arr = line.strip().split()
        key = arr[0]
        dbval = db.get(key, "NOT_IN_DB")
        print "\t".join([key, dbval] + arr[1:])
