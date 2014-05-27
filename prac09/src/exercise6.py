'''
Created on 27/05/2014

@author: s4361277
'''
import genome

g1 = genome.readGEOFile('GDS3198.soft', id_column = 0)
g2 = genome.readGEOFile('GDS3198.soft', id_column = 1)

print "GDS3198.soft contains", len(g1.getGenes()), "probes"
print "GDS3198.soft contains", len(g2.getGenes()), "genes"

