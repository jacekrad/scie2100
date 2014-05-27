'''
Created on 27/05/2014

@author: s4361277
'''
import genome as ge
g1 = ge.readGEOFile('GDS3198.soft', id_column = 0)
g2 = ge.readGEOFile('GDS3198.soft', id_column = 1)

# getGenes() and len()
print len(g1.getGenes())
print len(g2.getGenes())
