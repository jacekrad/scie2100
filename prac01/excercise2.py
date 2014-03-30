'''
Created on 30/03/2014

@author: jacekrad
'''
from sequence import *


seq1 = Sequence('AAAAAAAAGGGG')
print seq1.alphabet

seq2 = Sequence('AAAAAAAAGGUG')
print seq2.alphabet

seq3 = Sequence('AWAAAAAAGGVG')
print seq3.alphabet

ambiguous_RNA =  Sequence('AGC')
print ambiguous_RNA.alphabet

z_sequence = Sequence('Z')
