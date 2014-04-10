'''
Created on 08/04/2014

@author: s4361277
'''
from sequence import *
import Tkinter as tk
import tkalign
import util

#top = tk.Tk()
#frame = tk.Frame


#top.mainloop()

p08684_filename="p08884.fasta"
q16802_filename="q16802.fasta"

s1 = Sequence("THISLINE-", Protein_Alphabet, gappy=True)
s2 = Sequence("ISALIGNED", Protein_Alphabet)
aln = Alignment([s1, s2])

print aln

seqA = getSequence("HQ659871.1", "genbank")
seqB = getSequence("JX416721.1", "genbank")

dna_matrix = readSubstMatrix("dna.matrix", DNA_Alphabet)


# question 6
#alignment = alignGlobal(seqA, seqB, dna_matrix, -4)


#print alignment

#alignment.writeHTML("h1n1.html")

#alignGlobal(seqA, seqB, dna_matrix, -2).writeHTML("matrix1-gap2.html")
#alignGlobal(seqA, seqB, dna_matrix, -4).writeHTML("matrix1-gap4.html")
#alignGlobal(seqA, seqB, dna_matrix, -6).writeHTML("matrix1-gap6.html")
#alignGlobal(seqA, seqB, dna_matrix, -8).writeHTML("matrix1-gap8.html")

# question 8

util.searchAndSave("P08684", p08684_filename)
util.searchAndSave("Q16802", q16802_filename)

blosum62_matrix = readSubstMatrix("blosum62.matrix", Protein_Alphabet)
p450_supplied_matrix = readSubstMatrix("p450.matrix", Protein_Alphabet)
p450_prac02_matrix = readSubstMatrix("p450_prac02.matrix", Protein_Alphabet)

p08684_sequence = readFastaFile(p08684_filename)[0]
q16802_sequence = readFastaFile(q16802_filename)[0]

blosum_alignment = alignGlobal(p08684_sequence, q16802_sequence, p450_supplied_matrix, -6)


print p08684_sequence
print q16802_sequence

print blosum_alignment

root = tk.Tk()
root.geometry("2250x1080+0+0")
tkalign.AlignmentFrame(root, alignGlobal(p08684_sequence, q16802_sequence, blosum62_matrix, -2), "BLOSUM62 matrix")
tkalign.AlignmentFrame(root, alignGlobal(p08684_sequence, q16802_sequence, blosum62_matrix, -4), "BLOSUM62 matrix")
tkalign.AlignmentFrame(root, alignGlobal(p08684_sequence, q16802_sequence, blosum62_matrix, -6), "BLOSUM62 matrix")
tkalign.AlignmentFrame(root, alignGlobal(p08684_sequence, q16802_sequence, blosum62_matrix, -8), "BLOSUM62 matrix")
tkalign.AlignmentFrame(root, alignGlobal(p08684_sequence, q16802_sequence, blosum62_matrix, -10), "BLOSUM62 matrix")
tkalign.AlignmentFrame(root, alignGlobal(p08684_sequence, q16802_sequence, blosum62_matrix, -12), "BLOSUM62 matrix")

tkalign.AlignmentFrame(root, alignGlobal(p08684_sequence, q16802_sequence, p450_supplied_matrix, -2), "P450 matrix")
tkalign.AlignmentFrame(root, alignGlobal(p08684_sequence, q16802_sequence, p450_supplied_matrix, -4), "P450 matrix")
tkalign.AlignmentFrame(root, alignGlobal(p08684_sequence, q16802_sequence, p450_supplied_matrix, -6), "P450 matrix")
tkalign.AlignmentFrame(root, alignGlobal(p08684_sequence, q16802_sequence, p450_supplied_matrix, -8), "P450 matrix")
tkalign.AlignmentFrame(root, alignGlobal(p08684_sequence, q16802_sequence, p450_supplied_matrix, -10), "P450 matrix")
tkalign.AlignmentFrame(root, alignGlobal(p08684_sequence, q16802_sequence, p450_supplied_matrix, -12), "P450 matrix")
root.mainloop()  



