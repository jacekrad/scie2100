'''
Created on 01/04/2014

@author: jacekrad
'''
from sequence import *
aln = readClustalFile("../p450.aln", Protein_Alphabet)

gpcr = readClustalFile("../gpcr.aln", Protein_Alphabet)
print gpcr

gpcr.writeXML("gpcr-blue.xml")
gpcr.writeHTML("gpcr-blue.html")


b62 = readSubstMatrix("../blosum62.matrix", Protein_Alphabet)

print b62