'''
Created on 15/04/2014

@author: s4361277
'''
from sequence import *

alignment = readClustalFile("myAlign.aln", DNA_Alphabet)
pwm = PWM(alignment, start=19, end=28)
print pwm

# strict regular expression is closer to the consensus sequences
# but does allow for some flexibility
strict_regexp = Regexp("CTAT[AT]{3}TAG")

# flexible regular expression is more flexible than the strict regexp
# and allows for more alternative letter.  This regular expression should 
# produce more matches.
flexi_regexp = Regexp("[CT]TA[TA]{4}TA[GA\-]")

sequences = readFastaFile("motifSearch.fasta", DNA_Alphabet)

for sequence in sequences:
    # result = flexi_regexp.search(sequence)
    pwm_results = pwm.search(sequence)
    strict_regexp_results = strict_regexp.search(sequence)
    flexi_regexp_results = flexi_regexp.search(sequence)
    print
    print "-------------------------", sequence.name, "------------------------------"
    print "REGEXP Strict :", strict_regexp_results
    print "REGEXP Flexi  :", flexi_regexp_results
    print "PWM           :", pwm_results
