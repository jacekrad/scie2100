'''
Created on 07/05/2014

@author: s4361277
'''
from genome import *
import matplotlib.pyplot as plt
from sys import exit

ge3716 = readGEOFile("GDS3716.soft")

ratio = GeneExpression('GDS3716_ratio')

# set up age-matched sample indices (0: healthy, 1: cancer) 
paired_ERpos = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [33, 34, 35, 36, 37, 38, 39, 40, 41]] 
paired_ERneg = [[9, 10, 11, 12, 13, 14, 15, 16, 17], [24, 25, 26, 27, 28, 29, 30, 31, 32]]
 

i = 0  # sample counter 
while i < len(paired_ERpos[0]): 
    name = 'S' + str(i + 1) + '_ER+/Healthy'  # meaningful name for column header 
    ratio.addSamples(name, ge3716.getRatio(paired_ERpos[1][i], paired_ERpos[0][i]))
    i += 1 
    
i = 0 # reset counter
while i < len(paired_ERneg[0]): 
    name = 'S' + str(i + 1) + '_ER-/Healthy'  # meaningful name for column header 
    ratio.addSamples(name, ge3716.getRatio(paired_ERneg[1][i], paired_ERneg[0][i]))
    i += 1     

ratiovalues = ratio.matrix[:] 
plt.hist(ratiovalues.ravel(), bins=50)
plt.show()
