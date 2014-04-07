'''
Created on 01/04/2014
question 6
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

background = readDistrib("../blosum62.distrib")

p450_matrix_b = p450_aln.calcSubstMatrix(background)
p450_matrix_b.writeFile("p450_b.matrix")
 
rhodopsin_matrix_b = rhodopsin_aln.calcSubstMatrix(background)
rhodopsin_matrix_b.writeFile("rhodopsin_b.matrix")


print ("===================================== P450 =========================================", file=sys.stderr)
print (p450_matrix, file=sys.stderr)
print ("================================== RHODOPSIN =======================================", file=sys.stderr)
print (rhodopsin_matrix, file=sys.stderr)

print ("===================================== P450 background ==============================", file=sys.stderr)
print (p450_matrix_b, file=sys.stderr)
print ("================================== RHODOPSIN background ============================", file=sys.stderr)
print (rhodopsin_matrix_b, file=sys.stderr)

# deltas in the score matrices between blosum62 and out p450 & rhodopsin
p450_b_deltas = {}
rhodopsin_b_deltas = {}

# for each residue calculate score dalta between original p450 and one with new background
for key_pair in p450_matrix.scoremat:
    p450_b_deltas[key_pair] = p450_matrix_b.scoremat[key_pair] - p450_matrix.scoremat[key_pair]
    
# for each residue calculate score dalta between original rhodopsin and one with new background
for key_pair in rhodopsin_matrix.scoremat:
    rhodopsin_b_deltas[key_pair] = rhodopsin_matrix_b.scoremat[key_pair] - rhodopsin_matrix.scoremat[key_pair]    

#for key_pair in p450_b_deltas:
#    print(p450_b_deltas[key_pair], ",", key_pair, file=sys.stdout)
    
for key_pair in rhodopsin_b_deltas:
    print(rhodopsin_b_deltas[key_pair], ",", key_pair, file=sys.stdout)
