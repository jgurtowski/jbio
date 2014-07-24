##
# Working with files input/output
##
from itertools import imap
from functools import partial
from jbio.functional import compose, zipmap

def line_record_iterator(record, types, iterable):
    '''Converts an iterable (of lines) to records with given type'''
    record_maker = compose(record._make, 
                           partial(zipmap,types) ,
                           getattr(str, "split"))
    return imap(record_maker, iterable)


def iterator_over_file(filename,*open_args):
    with open(filename,*open_args) as fh:
        for item in fh:
            yield item
            
