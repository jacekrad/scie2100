'''
Created on 29/03/2014

@author: jacekrad
'''
import sequence as seq


ex5_filename = "sigpep_at.fa"
ex6_filename = "lipmet_at.fa"
ex7_filename = "ex7.fa"

""" read sequences from questions 5 & 6 into corresponding lists """ 
sequences_q5 = seq.readFastaFile(ex5_filename)
sequences_q6 = seq.readFastaFile(ex6_filename)

print "Q5 sequence has ", len(sequences_q5), " entries"
print "Q6 sequence has ", len(sequences_q6), " entries"

ids_q5 = []
ids_q6 = []
for sequence in sequences_q5:
    ids_q5.append(sequence.name)
for sequence in sequences_q6:
    ids_q6.append(sequence.name)
    
common_ids = set(ids_q5).intersection(set(ids_q6))

print len(common_ids), " common matches found"

""" save the common entries into a FASTA file as well as a dictionary
    of id:sequence object map
"""
result_sequences = []
result_dictionary = {}

for sequence in sequences_q5:
    if sequence.name in common_ids:
        result_sequences.append(sequence)
        result_dictionary[sequence.name] = sequence
        
seq.writeFastaFile(ex7_filename, result_sequences)
print "saved results to ", ex7_filename