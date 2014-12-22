#!/usr/bin/env python

import sys

from jbio.io.celera import unitig_layout_iterator
from jbio.io.file import iterator_over_file

if not len(sys.argv) == 2:
    sys.exit("getsingeltonfrags.py unitigs.layout")

for unitig in unitig_layout_iterator(iterator_over_file(sys.argv[1])):
    if len(unitig.frags) == 1:
        
        print "frg iid %d isdeleted t" % unitig.frags[0].ident






