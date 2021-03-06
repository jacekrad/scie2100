'''
Created on 15/04/2014

@author: s4361277
'''
from sequence import *

alignment = readClustalFile("myAlign.aln", DNA_Alphabet)
pwm = PWM(alignment, start=18, end=29)
print pwm

sequences = readFastaFile("motifSearch.fasta", DNA_Alphabet)

for sequence in sequences:
    results = pwm.search(sequence)
    print sequence.name, results
