'''
Created on 01/04/2014

@author: jacekrad
'''
from sequence import *
aln = readClustalFile("../p450.aln", Protein_Alphabet)

gpcr = readClustalFile("../gpcr.aln", Protein_Alphabet)
print gpcr

#gpcr.writeXML("gpcr-blue.xml")
#gpcr.writeHTML("gpcr-blue.html")
#aln.writeHTML("p450-blue.html")


b62 = readSubstMatrix("../blosum62.matrix", Protein_Alphabet)

print b62

a = 'V'
b = 'F'
c = 33

col = []
for seq in aln.seqs:
    col.append(seq[c])
    
print col

# equavilent code
#col = [seq[c] for seq in aln.seqs]


fab = col.count(a) * col.count(b)

print fab / len(aln.seqs)