from sequence import *
from symbol import *

p450aln=readClustalFile('p450.aln', Protein_Alphabet)
#print aln
rhoaln=readClustalFile('rhodopsin.aln', Protein_Alphabet)

b62Matrix = readSubstMatrix('blosum62.matrix', Protein_Alphabet)
print b62Matrix

p450Matrix = p450aln.calcSubstMatrix()
print p450Matrix
p450Matrix.writeFile("p450.matrix")

rhoMatrix = rhoaln.calcSubstMatrix()
print rhoMatrix
rhoMatrix.writeFile("rhodopsin.matrix")

from prob import *
new_distrib = readDistrib('blosum62.distrib')


p450MatrixBackground = p450aln.calcSubstMatrix(new_distrib)
print p450MatrixBackground
p450MatrixBackground.writeFile("p450.matrix")

rhoMatrixBackground = rhoaln.calcSubstMatrix(new_distrib)
print rhoMatrixBackground
rhoMatrixBackground.writeFile("rhodopsin.matrix")

