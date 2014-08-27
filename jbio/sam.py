from collections import namedtuple

from functional import zipmap

SamRecord_t = namedtuple('SamRecord', ['qname', 'flag',
                                     'rname', 'pos',
                                     'mapq', 'cigar',
                                     'rnext', 'pnext',
                                     'tlen', 'seq', 'qual',
                                     'tags','header'])

SamRecordTypes = [str, int, str, int, int, str,
                  str, int , int , str, str]


TAG_TYPES = {'A': str, 'i': int, 'f': float,
             'Z': str}


def cigar_iterator(cigar_str):
    '''
    Iterates over a cigar string and returns a tuple 
    (Cigar_Letter, int(count))
    '''
    count = ""
    for c in cigar_str:
        if c.isdigit():
            count += c
        else:
            yield( c, int(count))
            count = ""

def record_iterator(iterable):
    '''Ignores header (@) for now
    '''

    def next_v(itr):
        try:
            v = itr.next()
        except StopIteration:
            v = None
        return v

    it = iter(iterable)
    first = next_v(it)
    if not first:
        return 
    
    header = ""
    line = first
    while line.startswith("@"):
        header += line.strip()
        line = next_v(it)
        if not line or not line.startswith("@"):
            break
    
    if not line:
        return 
    
    while line:
        arr = line.strip().split()
        sam_record_arr = list(zipmap(SamRecordTypes,arr[:11]))
        tags = {}
        for tag in arr[11:]:
            tag_name,tag_type,tag_value = tag.split(":")
            ttfunc = TAG_TYPES.get(tag_type, None)
            if not ttfunc:
                raise Exception, "Unimplemented tag type %s" % tag_type
            tags[tag_name] = ttfunc(tag_value)

        sam_record_arr.append(tags)
        sam_record_arr.append(header)
        yield SamRecord_t._make(sam_record_arr)
        
        line = next_v(it)

    
    
    


