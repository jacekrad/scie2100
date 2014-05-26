'''
Created on 20/05/2014
prac08 question 5

@author: s4361277
'''
from sequence import *
from symbol import *
from sstruct import *

# read both protein and structure sequences into lists
proteins = readFastaFile("prot2.fa", Protein_Alphabet)
structures =  readFastaFile("sstr3.fa", DSSP3_Alphabet)

# store protein and structure sequences in dictionary for easy retrieval
protein_map = {}
structure_map = {}

for protein in proteins:
    protein_map.update({protein.name:protein})

for structure in structures:
    structure_map.update({structure.name:structure})

protein = protein_map.get("1EVH")
structure = structure_map.get("1EVH")


alpha = getScores(protein, 0)
calls_a1 = markCountAbove(alpha, width=6, call_cnt=4)


alpha = getScores(protein, 0) # values from column 0
beta = getScores(protein, 1) # values from column 1

calls_a1 = markCountAbove(alpha, width=6, call_cnt=4)
calls_a2 = extendDownstream(alpha, calls_a1, width=4)
calls_a3 = extendUpstream(alpha, calls_a2, width=4)

calls_b1 = markCountAbove(beta, width=5, call_cnt=3)
calls_b2 = extendDownstream(beta, calls_b1, width=4)
calls_b3 = extendUpstream(beta, calls_b2, width=4)

avg_a = calcRegionAverage(alpha, calls_a3)
avg_b = calcRegionAverage(beta, calls_b3)

diff_a = [avg_a[i] - avg_b[i] for i in range(len(avg_a))]
diff_b = [avg_b[i] - avg_a[i] for i in range(len(avg_a))]

calls_a4 = checkSupport(calls_a3, diff_a)
calls_b4 = checkSupport(calls_b3, diff_b)

# print the sequence, structure from file and calculated alpha helix
# and beta sheet structures
print "    ", protein
print "    ", structure
alpha_string = makesstr(calls_a4, 'H')
beta_string = makesstr(calls_b4, 'E')
# create a combined string
combined_string = ""
for i in range(0, len(alpha_string)):
    if beta_string[i] == 'E':
        combined_string += 'E'
    else:
        combined_string += alpha_string[i]
        
print " alpha:   ", alpha_string
print "  beta:   ", beta_string
print "Combined: ", combined_string
# to check the accuracy we simply compare our prediction to the one 
# obtained from sstr3.fa

position = 0
match_count = 0
for element in structure.sequence:
    if element == "H" and calls_a4[position]:
        match_count += 1 # matched alpha helix
    if element == "E" and calls_b4[position]:
        match_count += 1 # matched beta sheet
    if element != "H" and element !="E" and not(calls_a4[position]) and not(calls_b4[position]):
        match_count += 1 # matched other
    position += 1
        
print position, " structures with ", match_count, " correctly matched."
print "Accuracy %.2f%%" % ((float(match_count) /  position) * 100)
