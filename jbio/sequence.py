from collections import namedtuple

FastaRecord = namedtuple('FastaRecord', ['name','seq'])
FastqRecord = namedtuple('FastqRecord', ['name','seq','desc','qual'])


#BUG: Seems to be broken when given an iterator_over_file
# that only has one entry
def fasta_iterator(iterable):
    '''Iterable is just a collection of strings
    Could be Lines
    Expects that ">" will be at the start of entries
    '''
    it = iter(iterable)
    first = it.next()
    
    if not first or not first.startswith(">"):
        raise Exception("No \'>\' at start of Fasta")
    name = first.strip()[1:]
    seq = ""
    while True:
        #print "tippy"
        l = it.next()
        #print "top"
        if not l or l.startswith(">"):
            #print "in if"
            yield FastaRecord(name, seq)
            if not l:
                break
            name = l.strip()[1:]
            seq = ""
        else:
            seq += l.strip()
            #print "adding seq"
