'''
Created on 27/05/2014

@author: s4361277
'''
from sequence import *

promoters = readFastaFile("yeast_promoters.fa", DNA_Alphabet)

print len(promoters), " promoters"
# http://rulai.cshl.edu/SCPD/