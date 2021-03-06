from collections import namedtuple

FastaRecord = namedtuple('FastaRecord', ['name','seq'])
    

def record_iterator(iterable):
    '''Iterable is just a collection of strings
    Could be Lines
    Expects that ">" will be at the start of entries
    '''
    it = iter(iterable)
    try:
        first = it.next()
    except StopIteration:
        first = None

    if not first or not first.startswith(">"):
        raise Exception("No \'>\' at start of Fasta")
    name = first.strip()[1:]
    seq = ""
    while True:
        try:
            l = it.next()
        except StopIteration:
            l = None
        if not l or l.startswith(">"):
            yield FastaRecord(name, seq)
            if not l:
                break
            name = l.strip()[1:]
            seq = ""
        else:
            seq += l.strip()


def record_to_string(record):
    return ">" + record.name +"\n"+record.seq
