
from collections import namedtuple

FastqRecord = namedtuple('FastqRecord', ['name','seq','desc','qual'])


def record_iterator(iterable):
    it = iter(iterable)
    while True:
        try:
            name = it.next().strip()
            if not name.startswith("@"):
                raise Exception("Missing \'@\' in Fastq header")
            name = name[1:]
            seq = it.next().strip()
            desc = it.next().strip()
            if not desc.startswith("+"):
                raise Exception("Missing '\+\' in Description field")
            desc = desc[1:]
            qual = it.next().strip()
            yield FastqRecord(name,seq,desc,qual)

        except StopIteration:
            return

def record_to_string(record):
    return "\n".join(["@" + record.name, record.seq, "+" + record.desc,
                      record.qual])
