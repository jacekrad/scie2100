'''
Created on 30/03/2014

@author: mikael
'''
import numpy as np
import matplotlib.pyplot as plt

from sequence import *

aln = readClustalFile('/Users/samirlal/Desktop/cyp1a1.aln', Protein_Alphabet)
d = aln.calcDistances('fractional')

fig, ax = plt.subplots()
ax.imshow(d, plt.cm.gray, interpolation='nearest')
plt.yticks(np.arange(len(aln)), [s.name for s in aln])
plt.title('Distances')
plt.show()


