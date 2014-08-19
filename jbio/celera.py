##
#Functions for working with Celera output
##

from collections import namedtuple


FRG_t = namedtuple('FRG_t', ["type","ident","container","parent","hang","position"])
Unitig_t = namedtuple('Unitig_t', ["id", "header","frags"])

def unitig_layout_iterator(string_iterable):
    '''Iterates over all of the unitigs
    unitig 1
    len 0
    cns
    qlt
    data.unitig_coverage_stat  1.000000
    data.unitig_microhet_prob  1.000000
    data.unitig_status         X
    data.unitig_suggest_repeat F
    data.unitig_suggest_unique F
    data.unitig_force_repeat   F
    data.unitig_force_unique   F
    data.contig_status         U
    data.num_frags             1071
    data.num_unitigs           0
    FRG type R ident     20549 container         0 parent     59207 hang    136   3755 position  11621      0
    FRG type R ident     72784 container     20549 parent     20549 hang    290  -3884 position   7734    292
    '''
    
    it = iter(string_iterable)
    try:
        first = it.next()
    except StopIteration:
        first = None
        
    if not first or not first.startswith("unitig"):
        raise Exception("No \'unitig\' at start of file")
    
    unitig_id = first.strip().split()[1]
    header = ""
    frags = []
    while True:
        try:
            l = it.next()
        except StopIteration:
            l = None
        if not l or l.startswith("unitig"):
            yield Unitig_t(unitig_id, header, frags)
            if not l:
                break
            unitig_id = l.strip().split()[1]
            header = ""
            frags = []
        else:
            if l.startswith("FRG"):
                arr = l.strip().split()
                frags.append(FRG_t(arr[2],int(arr[4]),int(arr[6]),int(arr[8]),(int(arr[10]),
                                                                               int(arr[11])),
                                   (int(arr[13]),int(arr[14]))))
            else:
                header += l
