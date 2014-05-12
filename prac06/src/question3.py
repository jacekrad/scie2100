'''
Created on 07/05/2014

@author: s4361277
'''
from genome import *
import matplotlib.pyplot as plt
from webservice import *

ge38 = readGEOFile('GDS38.soft', id_column=1)
cln2_genes = ge38.getGenes("CLN2")
# 1497 is the probe id obtained from the file
cln2R = ge38.getPearson("CLN2")

gecln2R = GeneExpression("CLN2", [1], cln2R)
gecln2Rsorted = gecln2R.sort(0)

# cut the top 5 entries into a new list
# cln2 will be in the first position so we exclude it
top5 = gecln2Rsorted[1:6]

for gene in top5:
    print "-------------", gene, "Gene Ontology term names: "
    rows = search("taxonomy:4932+AND+gene:" + gene, "uniprot", format="list")
    terms = getGOTerms(rows[0])
    count = 0
    for term in terms:
        count += 1
        defs = getGODef(term)
        print count, ". ", defs.get("name")
