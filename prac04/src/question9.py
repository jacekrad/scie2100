'''
Created on 15/04/2014

@author: s4361277
'''
from sequence import *
import time

#question 5
# motif_sequences = readFastaFile("motifSequences.fasta", DNA_Alphabet)
# 
# motif_alignment = runClustal(motif_sequences)
# 
# motif_alignment.writeClustal("myAlign.aln")
# 
# motif_alignment.writeHTML("myAlign.html")

alignment = readClustalFile("myAlign.aln", DNA_Alphabet)
pwm = PWM(alignment, start=10, end=20)
print pwm
strict_regexp = Regexp("[CT]A[TA]{5}AG")
flexi_regexp = Regexp("[CT]A[TA]{5}A")

sequences = readFastaFile("motifSearch.fasta", DNA_Alphabet)

for sequence in sequences:
    #result = flexi_regexp.search(sequence)
    results = pwm.search(sequence)
    print results


# #qeuestion 8
# regexp = Regexp(".TA[AG]")
# results = regexp.search("CTAGAGCGCTAAGCCGA")
# print results



print "done"