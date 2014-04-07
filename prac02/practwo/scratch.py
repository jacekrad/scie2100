'''
Created on 01/04/2014

@author: jacekrad
'''
from sequence import *
aln = readClustalFile("../p450.aln", Protein_Alphabet)

gpcr = readClustalFile("../gpcr.aln", Protein_Alphabet)
print gpcr

gpcr.writeXML("gpcr-blue.xml")
gpcr.writeHTML("gpcr-blue-q3-4.html")
aln.writeHTML("p450-blue-q3-4.html")


blosum62_matrix = readSubstMatrix("../blosum62.matrix", Protein_Alphabet)

print blosum62_matrix

# a = 'V'
# b = 'F'
# c = 33
# 
# col = []
# for seq in aln.seqs:
#     col.append(seq[c])
#     
# #print col
# 
# # equavilent code
# #col = [seq[c] for seq in aln.seqs]
# 
# 
# fab = col.count(a) * col.count(b)
# 
# #print fab / len(aln.seqs)
# 
# p450_aln = readClustalFile("../p450.aln", Protein_Alphabet)
# p450_matrix = p450_aln.calcSubstMatrix()
# p450_matrix.writeFile("p450.matrix")
# 
# 
# rhodopsin_aln = readClustalFile("../rhodopsin.aln", Protein_Alphabet)
# rhodopsin_matrix = rhodopsin_aln.calcSubstMatrix()
# rhodopsin_matrix.writeFile("rhodopsin.matrix")
# 
# 
# 
# zzz = p450_matrix
#  
# print zzz.scoremat == rhodopsin_matrix.scoremat
# print zzz
# print rhodopsin_matrix
# 
# 
# 
# 
#  
# background = readDistrib("../blosum62_matrix.distrib")
#  
# p450_matrix_b = p450_aln.calcSubstMatrix(background)
# p450_matrix_b.writeFile("p450_b.matrix")
# print p450_matrix_b
#  
# rhodopsin_matrix_b = rhodopsin_aln.calcSubstMatrix(background)
# rhodopsin_matrix_b.writeFile("rhodopsin_b.matrix")
# print rhodopsin_matrix_b
# 
# 
# class Test():
#     a = 1
#     def __init__(self):
#         pass
#     
#     def setA(self, var):
#         self.a = var
#     
#     
#         
# t = Test()
# 
# print t.a
# print Test.a
# t.setA(3)
# print t.a
# print Test.a
# Test.v = a