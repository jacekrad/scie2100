'''
Created on 13/05/2014

@author: jacekrad
'''
from sequence import *

fasta_files = ["Genome1.fasta", "Genome2.fasta", "Genome3.fasta"]
gc_counts = {}

for fasta_file in fasta_files:
    print "======================================================================="
    print fasta_file
    sequences = readFastaFile(fasta_file, DNA_Alphabet)
    genome_total = 0
    genome_gc_count = 0 
    for sequence in sequences:
        total = 0
        gc_count = 0
        for letter in sequence.sequence:
            total += 1
            if letter == 'G' or letter == "C":
                gc_count += 1
        print sequence.name, "%.4f" % (float(gc_count) / float(total))
        genome_total += total
        genome_gc_count += gc_count
    print fasta_file, " total:", (float(genome_gc_count) / float(genome_total))