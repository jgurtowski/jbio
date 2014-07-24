
from collections import namedtuple

Blast6SeqRecord = namedtuple('Blast6SeqRecord',["qname","sname","pctid",
                                                "length","mismatch","gapopen",
                                                "qstart","qend","sstart",
                                                "send", "evalue","bitscore",
                                                "qlen","slen","qseq","sseq"])

Blast6SeqTypes = [str, str, float, int, int, int, int, int ,int, int,
                  float, float, int, int, str, str]


Blast6Record = namedtuple('Blast6SeqRecord',["qname","sname","pctid",
                                                "length","mismatch","gapopen",
                                                "qstart","qend","sstart",
                                                "send", "evalue","bitscore",
                                                "qlen","slen"])

Blast6Types = [str, str, float, int, int, int, int, int ,int, int,
                  float, float, int, int]


