'''
Created on 08/04/2014

@author: s4361277
'''
from sequence import *
s1 = Sequence("THISLINE-", Protein_Alphabet, gappy=True)
s2 = Sequence("ISALIGNED", Protein_Alphabet)
aln = Alignment([s1, s2])

print aln