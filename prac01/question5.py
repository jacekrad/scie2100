'''
Created on 30/03/2014

Assessment question 5
Exercises 8 & 9

@author: jacekrad
'''

import sequence as seq
from collections import Counter
from webservice import *

sequences = seq.readFastaFile("mystery1.fa")

all_ids = []

""" for all the IDs in the sequences found in mystery1.fa get a ID mapping
    from P_REFSEQ_AC to ACC and for each IS in the map (dictionary) add it to
    the list of all IDs
"""
for sequence in sequences:
    ids = idmap(sequence.name, 'P_REFSEQ_AC', 'ACC')
    for value in ids.values():
        all_ids.append(value)


""" get a list of unique IDs from all the IDs """
unique_ids = list(set(all_ids))

combined_GOterms = []

for unique_id in unique_ids:
    for term in getGOTerms(unique_id):
        combined_GOterms.append(term)

""" utilise python's collection.Counter, a hashable object counting class """
counter = Counter(combined_GOterms)

""" print the results in a format that is easily imported into a spreadsheet 
"""
print "Top 5 Gene Ontology terms found.  Format is:"
print "Term ID;Name;Frequency;Description"
for term, count in counter.most_common(5):
    defs = getGODef(term)
    print defs.get("id"), ";", defs.get("name"), ";", count, ";", defs.get("def")
