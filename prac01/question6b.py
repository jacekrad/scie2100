'''
Created on 30/03/2014

@author: jacekrad
'''

import sequence as seq
import util

q6b_filename="q6b.fasta"

util.searchAndSave("surface+protein+AND+organism:1280", q6b_filename)

sequences = seq.readFastaFile(q6b_filename)

print len(sequences), " total sequences"

matched_sequences = []
for sequence in sequences:
    if "RAFKPS" in str(sequence.sequence):
        matched_sequences.append(sequence)

""" print the final results """        
print len(matched_sequences), " matched sequences:"
for sequence in matched_sequences:
    print sequence