'''
Created on 08/04/2014

@author: s4361277
question 7
'''
from sequence import *
from alignments import AlignmentCollection
import Tkinter as tk
import tkalign
import util

seqA = getSequence("HQ659871.1", "genbank")
seqB = getSequence("JX416721.1", "genbank")

dna_matrix = readSubstMatrix("dna.matrix", DNA_Alphabet)

alignments = AlignmentCollection("question 7")

print "number of cells in alignment matrix = ", len(seqA) * len(seqB) 

for gap_penalty in range(-1, -20, -1):
    alignments.add_alignment(alignGlobal(seqA, seqB, dna_matrix, gap_penalty))
    print gap_penalty, ": done"

alignments.dump_xml_and_html("question_7_alignments")


#root = tk.Tk()
#root.geometry("2250x1080+0+0")

#for gap_penalty in range(-2, -20, -2):
#    tkalign.AlignmentFrame(root, alignGlobal(seqA, seqB, dna_matrix, gap_penalty), "DNA matrix")

#root.mainloop()  



