'''
Created on 08/04/2014

@author: s4361277
'''
from sequence import *
from alignments import AlignmentCollection, AlignmentThread
import util

p08684_filename="p08884.fasta"
q16802_filename="q16802.fasta"


# question 8
util.searchAndSave("P08684", p08684_filename)
util.searchAndSave("Q16802", q16802_filename)

matrix_names = ["blosum62.matrix", "p450.matrix"]

# list of matrices though which we shall iterate to obtain various alignments
matrices = []
for matrix_name in matrix_names:
    matrix = readSubstMatrix(matrix_name, Protein_Alphabet)
    print "Adding matrix: " + matrix_name + "\n", matrix
    matrices.append(matrix)
    
# read our residue sequences from FASTAs
P08684 = readFastaFile(p08684_filename)[0]
Q16802 = readFastaFile(q16802_filename)[0]

local_alignments = AlignmentCollection("question 10 local")
global_alignments = AlignmentCollection("question 10 global")

for matrix in matrices:
    print "processing matrix:", matrix.name
    for gap_penalty in range(-1, -20, -1):
        local_alignments.add_alignment(alignLocal(P08684, Q16802, matrix, gap_penalty))
        global_alignments.add_alignment(alignGlobal(P08684, Q16802, matrix, gap_penalty))
    
local_alignments.dump_xml_and_html("question_10_local_alignments")
global_alignments.dump_xml_and_html("question_10_global_alignments")
