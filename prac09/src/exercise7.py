'''
Created on 27/05/2014

@author: s4361277
'''
from sequence import *
import genome as ge
import matplotlib.pyplot as plt
import numpy as np

g = ge.readGEOFile('GDS3198.soft', id_column=1)
meanfold = {}
for gene in g.genes:
    profile = g.getGenes(gene)
    meanfold[gene] = (math.log(profile[0] / profile[3]) + 
                      math.log(profile[1] / profile[4]) + 
                      math.log(profile[2] / profile[5])) / 3

# pull out NaNs
scores = [y for y in meanfold.values() if not np.isnan(y)]
hist, bins = np.histogram(scores, bins=50)
width = 0.7 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center', width=width)
plt.title("Question 7")
plt.show()
result = sorted(meanfold.items(), key=lambda v: v[1])
print '========== Wildtype may down-regulate =========='
for r in result[0:100]:
        print r[0], r[1]

print '========== Wildtype may up-regulate =========='
for r in result[-1:-100:-1]:
        print r[0], r[1]
