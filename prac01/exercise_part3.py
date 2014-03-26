'''
Created on 26/03/2014

@author: s4361277
'''
from sequence import  *
import webservice as ws

q9_seqs = readFastaFile("mystery1.fa") # protein alphabet

all_ids=[]
for s in q9_seqs:
    ids=idmap(seq.name, P_ref.seq, 'ACC')
    
    for value in ids.values()
        all_ids.append(value)
    all_ids  = self(all_ids)
    all_ids = list(all_ids)
    
    
    
    
    for ids in all_idsterm = getGOTerms(ids)
    
    
    
    
    
    print s.name
    
    
    
    go_terms = ws.getGOTerms(s.name)