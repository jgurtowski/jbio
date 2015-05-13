
from collections import namedtuple

FastqRecord = namedtuple('FastqRecord', ['name','seq','desc','qual'])


def record_iterator(iterable):
    it = iter(iterable)
    while True:
        try:
            name = it.next()
            if not name.startswith("@"):
                raise Exception("Missing \'@\' in Fastq header")
            name = name[1:]
            seq = it.next()
            desc = it.next()
            if not desc.startswith("+"):
                raise Exception("Missing '\+\' in Description field")
            desc = desc[1:]
            qual = it.next()
            return FastqRecord(name,seq,desc,qual)
        except StopIteration:
            if not name or not seq or not desc or not qual:
                raise Exception("Bad Fastq File")

def record_to_string(record):
    return "\n".join(["@" + record.name, record.seq, "+" + record.desc,
                      record.qual])
