'''
Created on 27/05/2014

@author: s4361277
'''
from sequence import *
import genome as ge
from go import *

g = ge.readGEOFile('GDS3198.soft', id_column=1)
meanfold = {}
for gene in g.genes:
    profile = g.getGenes(gene)
    meanfold[gene] = (math.log(profile[0] / profile[3]) + 
                      math.log(profile[1] / profile[4]) + 
                      math.log(profile[2] / profile[5])) / 3

result = sorted(meanfold.items(), key=lambda v: v[1])
genes = []

for r in result[0:100]:
    if not(' ' in r[0]) and len(search(r[0], dbName='uniprot', format='list', limit=1)) == 1:
        genes.append(r[0])

for r in result[-1:-100:-1]:
    if not(' ' in r[0]) and len(search(r[0], dbName='uniprot', format='list', limit=1)) == 1:
        genes.append(r[0])

godb = GODB("yeast_go")
r = godb.get_GO_term_overrepresentation(genes, evalThreshold=1.0)
print "GO terms:"

for term in r:
    print godb.get_GO_description(term)

