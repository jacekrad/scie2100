'''
Created on 08/04/2014

@author: s4361277
question 7
'''
from sequence import *
from alignments import AlignmentCollection, AlignmentThread

HQ659871_1 = getSequence("HQ659871.1", "genbank")
JX416721_1 = getSequence("JX416721.1", "genbank")

matrix_names = ["dna.matrix", "dna.matrix2", "dna.matrix3", "dna.matrix4", "dna.matrix.unknown"]

# list of matrices though which we shall iterate to obtain various alignments
matrices = []
for matrix_name in matrix_names:
    matrix = readSubstMatrix(matrix_name, DNA_Alphabet)
    print "Adding matrix: " + matrix_name + "\n", matrix
    matrices.append(matrix)

local_alignments = AlignmentCollection("question 7 local")
global_alignments = AlignmentCollection("question 7 global")

print "number of cells in alignment matrix = ", len(HQ659871_1) * len(JX416721_1) 

threads = []

print "HQ659871_1 = ", len(HQ659871_1)
print "JX416721_1 = ", len(JX416721_1)

for matrix in matrices:
    print "processing matrix:", matrix.name
    for gap_penalty in range(-1, -20, -1):
        local_alignments.add_alignment(alignLocal(HQ659871_1, JX416721_1, matrix, gap_penalty))
        global_alignments.add_alignment(alignGlobal(HQ659871_1, JX416721_1, matrix, gap_penalty))
    
local_alignments.dump_xml_and_html("question_7_local_alignments")
global_alignments.dump_xml_and_html("question_7_global_alignments")


