'''
Created on 08/04/2014

@author: s4361277
question 7
'''
from sequence import *
from alignments import AlignmentCollection, AlignmentThread
import Tkinter as tk
import tkalign
import util
from copy import *

seqA = getSequence("HQ659871.1", "genbank")
seqB = getSequence("JX416721.1", "genbank")

dna_matrix = readSubstMatrix("dna.matrix", DNA_Alphabet)
dna_matrix2 = readSubstMatrix("dna.matrix2", DNA_Alphabet)
dna_matrix3 = readSubstMatrix("dna.matrix3", DNA_Alphabet)
print dna_matrix
alignments = AlignmentCollection("question 7")

print "number of cells in alignment matrix = ", len(seqA) * len(seqB) 

threads = []

for gap_penalty in range(-1, -10, -1):
    thread1 = AlignmentThread(deepcopy(seqA), deepcopy(seqB), "dna.matrix", gap_penalty)
    thread1.start()
    threads.append(thread1)
    thread2 = AlignmentThread(deepcopy(seqA), deepcopy(seqB), "dna.matrix2", gap_penalty)
    thread2.start()
    threads.append(thread2)
    thread3 = AlignmentThread(deepcopy(seqA), deepcopy(seqB), "dna.matrix3", gap_penalty)
    thread3.start()
    threads.append(thread3)


# wait for all threads to finish


#for t in threads:
#    t.join()
    # add result to our collection
#    alignments.add_alignment(t.result_alignment)


#alignments.dump_xml_and_html("question_7_alignments")


#root = tk.Tk()
#root.geometry("2250x1080+0+0")

#for gap_penalty in range(-2, -20, -2):
#    tkalign.AlignmentFrame(root, alignGlobal(seqA, seqB, dna_matrix, gap_penalty), "DNA matrix")

#root.mainloop()  



