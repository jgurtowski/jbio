
from collections import namedtuple

from jbio.io.file import line_record_iterator

NucRecord = namedtuple('NucRecord',
                       ["sstart","send","b3","qstart","qend",
                        "b6", "salen","qalen","b9","pctid",
                        "b11","slen","qlen","b14","sname","qname"])

NucRecordTypes = [int, int, str, int,int,str,int,int,str,float,str,
                  int,int,str,str,str]


def record_iterator(stream):
    return line_record_iterator(NucRecord, NucRecordTypes, stream)

