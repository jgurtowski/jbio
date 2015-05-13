##
# Working with files input/output
##

import sys

from itertools import imap
from functools import partial
from jbio.functional import compose, zipmap

def line_record_iterator(record, types, iterable):
    '''Converts an iterable (of lines) to records with given type'''
    record_maker = compose(record._make, 
                           partial(zipmap,types) ,
                           getattr(str, "split"))
    return imap(record_maker, iterable)


def line_iterator(iterable):
    for line in iterable:
        yield line

def line_item_iterator(iterable):
    for line in iterable:
        yield line.split()

def iterator_over_file(filename, open_func=open):
    with open_func(filename) as fh:
        for item in fh:
            yield item

def iterator_over_file_from_extension(filename):
    import gzip
    openers = {"gz" : gzip.open}
    ext = filename.split(".")

    opener = openers.get(ext[-1], open)

    i_o_f = iterator_over_file(filename, opener)
    
    if "fa" in ext or "fasta" in ext:
        from jbio.fasta import record_iterator
        return record_iterator(i_o_f)
    elif "fq" in ext or "fastq" in ext:
        from jbio.fastq import record_iterator
        return record_iterator(i_o_f)
    else:
        raise Exception("Unknown File Extension \'%s\'" % ext[-1])

            
def record_to_string(record, delim="\t"):
    fields = record._fields
    val_getter = compose(str, partial(getattr, record))
    return delim.join(imap(val_getter, fields))


class FileOrStream:
    '''Opens a File or a Stream from a String'''

    _streams = {"stdin": sys.stdin,
                 "stdout":sys.stdout,
                 "stderr":sys.stderr}

    def __init__(self, s, *args ):
        '''s is a string representation of what you 
        want to open, could be file or string'''

        self.s = s
        self.eargs = args
        self.isStream = False

    def __enter__(self):
        if self.s in FileOrStream._streams:
            self.isStream = True
            return FileOrStream._streams[self.s]
        self.fh = open(self.s, *self.eargs)
        return self.fh
    
    def __exit__(self, ttype ,value, traceback):
        if not self.isStream:
            self.fh.close()
