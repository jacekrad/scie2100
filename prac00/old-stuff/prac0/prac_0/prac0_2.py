'''
Created on 11/03/2014

@author: s4361277
'''

import guide, mysequence

from guide import DNA_Alphabet

sequences = guide.readFastaFile("h1n1.fasta", guide.DNA_Alphabet)
print "found ", sequences.__len__(), " sequences"

# print sequence[0] 

# seq2 = guide.getSequence('L03547', "genbank", DNA_Alphabet)

# length =  seq2.__len__()


# print "A: ", float(seq2.count("A")) / length * 100.0 , "%"
# print "T: ", float(seq2.count("T")) / length * 100.0 , "%"
# print "G: ", float(seq2.count("G")) / length * 100.0 , "%"
# print "C: ", float(seq2.count("C")) / length * 100.0 , "%"


def multiSequenceBaseCount(sequences, alphabet):
    """performs a base count on a list of sequences."""
    # counts = {"A":0, "B":0, "C":0, "D":0}
    counts = {}
    for letter in alphabet:
        counts[letter] = 0
        
    for seq in sequences:
        for letter in alphabet:
            counts[letter] += seq.sequence.count(letter)  

    for letter in alphabet:
        print letter, ": ", counts[letter]

print sequences.__len__()

# mysequence.baseCounts2(sequences[0].sequence, guide.DNA_Alphabet)

# multiSequenceBaseCount(sequences, guide.DNA_Alphabet)

prot_ids = guide.searchSequences("organism:7227+AND+family:G-protein+coupled+receptor", "uniprot")

# prot_ids = guide.searchSequences("organism:7227", "uniprot")


print "Found ", prot_ids.__len__(), " sequences"

class AminoAcid():
    """represent an amino acid"""
    
    hydrophobic_codes = "AILFVPG"
    
    def __init__(self, amino_acid_code):
        self.code = amino_acid_code
    
    def is_hydrophobic(self):
        if self.code in self.hydrophobic_codes:
            return True
        else:
            return False


hydrophobic_count = 0
for prot_id in prot_ids:
    seq = guide.getSequence(prot_id, "uniprot", guide.Protein_wX)
    for amino_acid_code in seq.sequence:
        amino_acid = AminoAcid(amino_acid_code)
        if amino_acid.is_hydrophobic():
            hydrophobic_count += 1
