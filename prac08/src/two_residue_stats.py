'''
Created on 25/05/2014

@author: jacekrad
'''
from sequence import *

class Stats():
    
    def __init__(self):
        self.counts = {}
        self.alphaalpha = {}
        self.alphaalpha_prob = {}
        for first in Protein_Alphabet:
            for second in Protein_Alphabet:
                self.counts.update({first + second: 0})
                self.alphaalpha.update({first + second: 0})

    def add_residue_pair(self, first_residue, second_residue):
        key = first_residue + second_residue
        self.counts.update({key:self.counts.get(key) + 1})
    
    def add_alpha_alpha(self, first_residue, second_residue):
        key = first_residue + second_residue
        self.alphaalpha.update({key:self.alphaalpha.get(key) + 1})
        

proteins = readFastaFile("prot2.fa", Protein_Alphabet)
structures = readFastaFile("sstr3.fa", DSSP3_Alphabet)


protein_index = 0
st = Stats()

for protein in proteins:
    structure = structures[protein_index]
    for i in range(0, len(structure.sequence) - 1):
        residue_structure1 = structure.sequence[i]
        residue_structure2 = structure.sequence[i + 1]
        st.add_residue_pair(protein.sequence[i], protein.sequence[i + 1])        
        if "H" == residue_structure1 and "H" == residue_structure2:
            st.add_alpha_alpha(protein.sequence[i], protein.sequence[i + 1])
    protein_index += 1
print st.alphaalpha
print st.counts