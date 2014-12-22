
from collections import namedtuple

FastqRecord = namedtuple('FastqRecord', ['name','seq','desc','qual'])


def record_to_string(record):
    return "\n".join(["@" + record.name, record.seq, "+" + record.desc,
                      record.qual])
