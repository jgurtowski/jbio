
import string

def reverse_complement(seq):
    complements = string.maketrans('acgtACGTNn-', 'tgcaTGCANn-')
    return seq.translate(complements)[::-1]

def varfloor(floor, value):
    if value < floor:
        return floor
    return value
