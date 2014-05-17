'''
Created on 13/05/2014

@author: jacekrad
'''
from sequence import *

fasta_files = ["Genome1.fasta", "Genome2.fasta", "Genome3.fasta"]
    
def get_gc_count(sequence):
    return sequence.count('G') + sequence.count('C')

def get_gc_fraction(sequence):
    return round(float(get_gc_count(sequence)) / len(sequence), 2)

def get_mean(values):
    return round(float(sum(values)) / len(values), 2)

def get_standard_deviation(values):
    vals = []
    mean = get_mean(values)
    for i in range(len(values)):
        vals.append((values[i] - mean) ** 2)
    standard_deviation = math.sqrt((1 / float(len(values))) * sum(vals))
    return round(standard_deviation, 2)

#dictionary in which we'll save the contigs
contigs = {}
 
for fasta_file in fasta_files:
    contig_list = []
    contigs.update({fasta_file:contig_list})
    sequences = readFastaFile(fasta_file, DNA_Alphabet)
    for sequence in sequences:
        contig_list.append(get_gc_fraction(sequence.sequence))
    mean = get_mean(contig_list)
    standard_deviation = get_standard_deviation(contig_list)
    upper_bound = mean + (2 * standard_deviation)
    lower_bound = mean - (2 * standard_deviation)
    print fasta_file, ": ", mean, standard_deviation, upper_bound, lower_bound
