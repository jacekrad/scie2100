'''
Created on 27/05/2014

@author: s4361277
'''
from sequence import *
from go import * 

godb = GODB("yeast_go")

R = godb.get_GO_term_overrepresentation(pos, evalThreshhold=1.0)
for row in R:
    print row, r[row]
