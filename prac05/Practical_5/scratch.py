'''
Created on 30/04/2014

@author: s4361277
'''

from sequence import *
from phylo import *

tree = readNewick('cyp1a1.tree')
aln = readClustalFile('cyp1a1.aln', Protein_Alphabet)
for seq in aln:
    node = tree.findLabel(seq.name)
    a = tree.getAncestorsOf(node)
    print seq.name, 'has-distance', node.dist, 'from ancestor', a.label
    

# q 3
tree = runUPGMA(aln, "fractional")
tree2 = runUPGMA(aln, "k2p")
tree3 = runUPGMA(aln, "poisson")

print tree
print tree2
print tree3

#q4 

aln2 = readClustalFile("cyp_mouse.aln", Protein_Alphabet)
q4tree = aln.calcDistances("fractional")

print q4tree

#q5

# tree = PhyloTree(PhyloNode("root"))
# 
# aln = readClustalFile('cyp_mouse.aln', Protein_Alphabet)
# tree.putAlignment(aln)
# newickBeforeParsimony = tree.strSequences(10, 15)
# tree.parsimony()