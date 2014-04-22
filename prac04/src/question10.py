'''
Created on 15/04/2014

@author: s4361277
'''
from sequence import *

alignment = readClustalFile("myAlign.aln", DNA_Alphabet)
pwm = PWM(alignment, start=20, end=29)
print pwm
strict_regexp = Regexp("[CT]A[TA]{5}AG")
flexi_regexp = Regexp("[CT]A[TA]{5}A")

sequences = readFastaFile("motifSearch.fasta", DNA_Alphabet)

for sequence in sequences:
    #result = flexi_regexp.search(sequence)
    results = pwm.search(sequence)
    print sequence.name, results


# #qeuestion 8
# regexp = Regexp(".TA[AG]")
# results = regexp.search("CTAGAGCGCTAAGCCGA")
# print results



print "done"