'''
Created on 07/05/2014

@author: s4361277
'''
from genome import *
import matplotlib.pyplot as plt

ge3716 = readGEOFile("GDS3716.soft")


# print ge3716.getHeaders()

#print ge3716[0]

#print ge3716.getHeaderIndex('GSM512539')

#print ge3716.getSamples([33, 0])

ratio = GeneExpression('GDS3716_ratio')
logratio = GeneExpression('GDS3716_log_ratio')

#ratio.addSamples('S1_ER+/Healthy', ge3716.getRatio(33, 0))

# set up age-matched sample indices (0: healthy, 1: cancer) 
paired_ERpos = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [33, 34, 35, 36, 37, 38, 39, 40, 41]] 
paired_ERneg = [[9, 10, 11, 12, 13, 14, 15, 16, 17], [24, 25, 26, 27, 28, 29, 30, 31, 32]]
 
# Fill class with ER+ matched samples 
i = 0  # sample counter 

while i < len(paired_ERpos[0]): 
    name = 'S' + str(i + 1) + '_ER+/Healthy'  # meaningful name for column header 
    ratio.addSamples(name, ge3716.getRatio(paired_ERpos[1][i], paired_ERpos[0][i]))
    logratio.addSamples(name, ge3716.getLogRatio(paired_ERpos[1][i], paired_ERpos[0][i]))
    i += 1 
    
i = 0
while i < len(paired_ERneg[0]): 
    name = 'S' + str(i + 1) + '_ER-/Healthy'  # meaningful name for column header 
    ratio.addSamples(name, ge3716.getRatio(paired_ERneg[1][i], paired_ERneg[0][i]))
    logratio.addSamples(name, ge3716.getLogRatio(paired_ERneg[1][i], paired_ERneg[0][i]))
    i += 1     

values = logratio.matrix[:] # this will give all values
plt.hist(values.ravel(), bins=50)
plt.show()
# 
# sdict={} #dictionary for gene: no. of significant samples
# #set up gene dictionary
# genes = logratio.getGenes()
# for gene in genes: #fill sdict with 0 so can add counter to them
#     sdict[gene] = 0
# #Z-score calculation for each sample
# for #loop through samples to get zscore
#     zscores=logratio.getZScore(sample)
# #iterate the dictionary to identify probes
# for key in zscores.iterkeys():
#     if #Key condition(Zscore greater than 2 or less than -2)
# sdict[key] +=1 #add to sample count
# #display significant genes
# for key in sdict:
# if #Key condition (at least 11 sample pairs)
# #print something