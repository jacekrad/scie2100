'''
Created on 29/03/2014

@author: jacekrad
'''

import sequence as seq
import os.path as path

q5_filename = "sigpep_at.fa"
q6_filename = "lipmet_at.fa"

""" for both questions 5 and 6 we check if the fasta file already exists 
    and only do the searches and obtain sequences if false 
    this is we can rerun the program quickly without rebuilding the 
    fasta file each and every time
"""

""" QUESTION 5 """
if not(path.isfile(q5_filename)):
    q5_sequences = []
    """ set of ids returned as part of the protein search in question 5 """
    q5_ids = seq.searchSequences("signal+peptide+AND+organism:Arabidopsis+thaliana[3702]+" 
                                 + "AND+length:[100+TO+*]")
    print "Processing ", len(q5_ids), " sequences ..."
    for seq_id in q5_ids:
        print "Fetching sequence: ", seq_id
        q5_sequences.append(seq.getSequence(seq_id))
    seq.writeFastaFile(q5_filename, q5_sequences)
else:
    print q5_filename, " exists. skipping."


""" QUESTION 6 """
if not(path.isfile(q6_filename)):
    q6_sequences = []
    """ set of ids returned as part of the question 6 search  """ 
    q6_ids = seq.searchSequences("Lipid+metabolism+AND+organism:3702+AND+fragment:no+"
                                 + "AND+length:[100+TO+*]")
    print "Processing ", len(q6_ids), " sequences ..."
    for seq_id in q6_ids:
        print "Fetching sequence: ", seq_id
        q6_sequences.append(seq.getSequence(seq_id))
    seq.writeFastaFile(q6_filename, q6_sequences)
else:
    print q6_filename, " exists. skipping."

