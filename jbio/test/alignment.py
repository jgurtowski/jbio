
import os

from itertools import groupby, imap
from functools import partial
from operator import attrgetter

import gzip 

from jbio.alignment import *
from jbio.io.file import iterator_over_file_from_extension as ioffe
from jbio.io.blast import record_iterator as blast_record_iterator
from jbio.functional import compose


def test_LIS(config):
    
    test_data_path = config.get("test_data_path")
    alignment_file = os.path.join(test_data_path,
                                  "channel_286_read_45_1406145606_2D.blast6.gz")
    blast_alignment_getter = compose(blast_record_iterator, ioffe)
    
    return lambda : LIS(attrgetter("sstart"), attrgetter("send"), None,
                        blast_alignment_getter(alignment_file))
    
    
