'''
Created on 30/03/2014

@author: jacekrad
'''

import os.path as path
import sequence as seq


def searchAndSave(searchString, filename):
    """ convenince function to search database and save
        results to a FASTA file.  If a file of that name
        already exists then the whole process is skipped
        
        searchString - this is what is being searched for
        filename - name of the file where to save the results
    """ 
    if not(path.isfile(filename)):
        sequences = []
    
        """ set of ids returned as part of the protein """
        ids = seq.searchSequences(searchString)

        print "Processing ", len(ids), " sequences ..."
        """ iterate over the ids and for each fetch the record
            from the database and append it to ex5_sequences
        """
        for seq_id in ids:
            print "Fetching sequence: ", seq_id
            sequences.append(seq.getSequence(seq_id))
            """  save the completed list of sequences to a FASTA file """
            seq.writeFastaFile(filename, sequences)
    else:
        print filename, " exists. skipping."