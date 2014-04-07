'''
Created on 01/04/2014

@author: jacekrad
'''
from __future__ import print_function
from sequence import *

blosum62_matrix = readSubstMatrix("../blosum62.matrix", Protein_Alphabet)

p450_aln = readClustalFile("../p450.aln", Protein_Alphabet)
p450_matrix = p450_aln.calcSubstMatrix()
p450_matrix.writeFile("p450.matrix")


rhodopsin_aln = readClustalFile("../rhodopsin.aln", Protein_Alphabet)
rhodopsin_matrix = rhodopsin_aln.calcSubstMatrix()
rhodopsin_matrix.writeFile("rhodopsin.matrix")

print ("=================================== BLOSUM62 =======================================", file=sys.stderr)
print (blosum62_matrix, file=sys.stderr)
print ("===================================== P450 =========================================", file=sys.stderr)
print (p450_matrix, file=sys.stderr)
print ("================================== RHODOPSIN =======================================", file=sys.stderr)
print (rhodopsin_matrix, file=sys.stderr)

# deltas in the score matrices between blosum62 and out p450 & rhodopsin
p450_deltas = {}
rhodopsin_deltas = {}

# for each residue pair calculate the delta between blosum62 and our scores
for key_pair in blosum62_matrix.scoremat:
    p450_deltas[key_pair] = p450_matrix.scoremat[key_pair] - blosum62_matrix.scoremat[key_pair]
    rhodopsin_deltas[key_pair] = rhodopsin_matrix.scoremat[key_pair] - blosum62_matrix.scoremat[key_pair]

#for key_pair in p450_deltas:
#    print(p450_deltas[key_pair], ",", key_pair, file=sys.stdout)
    
for key_pair in rhodopsin_deltas:
    print(rhodopsin_deltas[key_pair], ",", key_pair, file=sys.stdout)
