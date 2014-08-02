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


def iterator_over_file(filename, open_func=open):
    with open_func(filename) as fh:
        for item in fh:
            yield item

def iterator_over_file_from_extension(filename):
    import gzip
    openers = {"gz" : gzip.open}

    ext = filename.split(".")[-1]
    opener = openers.get(ext, open)

    return iterator_over_file(filename, opener)
            
def record_to_string(record, delim="\t"):
    fields = record._fields
    val_getter = compose(str, partial(getattr, record))
    return delim.join(imap(val_getter, fields))
