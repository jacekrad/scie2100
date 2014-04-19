'''
Created on 15/04/2014

@author: s4361277
'''
from sequence import *
import time

seqA1 = Sequence("AGCGCGATTATATAAGACGGACGGCTAAAG")
seqB1 = Sequence("AGCGGATATTTATATCGCACGACGACTACG")
seqC1 = Sequence("GGATCGATTATATAGCCTGGACGAGACATG")


seqA2 = Sequence("AGCGCGATTATATAAGACGGACGAGACGACAGCGCGATAGACGAGACGGACGAGACGACT")
seqB2 = Sequence("GGATCGATTATATAGCCTGGACGAGACATGGGATCGAAGACGACCTGGACGAGACATGAC")
seqC2 = Sequence("AGCGGATATTTATATCGCACGACGACTACGAGCGGAAGACGAGTTTCGCACGACACTACG")

matrix = readSubstMatrix("dna.matrix", DNA_Alphabet)

print "pairwise align of short sequences (Q1)"
start_time = time.time()
alignGlobal(seqA1, seqB1, matrix, -1)
end_time = time.time()
print("Elapsed time was %g seconds" % (end_time - start_time))

print "triplet align of short sequences (Q1) ..."
start_time = time.time()
tripletAlignGlobal(seqA1, seqB1, seqC1, matrix, -1)
end_time = time.time()
print("Elapsed time was %g seconds" % (end_time - start_time))

print "triplet align of long sequences (Q2) ..."
start_time = time.time()
tripletAlignGlobal(seqA2, seqB2, seqC2, matrix, -1)
end_time = time.time()
print("Elapsed time was %g seconds" % (end_time - start_time))

# the following code provides a more detailed analysis of algorithm time
# the output was use to genmerate a comparison graph of expected vs real
# execution times

print "triplet align: time vs sequence length (Q2) ..."
sequence_string_fragment_1 = "AGCGCGATTATATAAGACGGACGGCTAAAG"
sequence_string_fragment_2 = "AGCGGATATTTATATCGCACGACGACTACG"
sequence_string_fragment_3 = "GGATCGATTATATAGCCTGGACGAGACATG"

sequence_string_1 = "" 
sequence_string_2 = ""
sequence_string_3 = ""

for length_multiplier in range(1, 11):
    sequence_string_1 += sequence_string_fragment_1
    sequence_string_2 += sequence_string_fragment_2
    sequence_string_3 += sequence_string_fragment_3
    start_time = time.time()
    tripletAlignGlobal(Sequence(sequence_string_1), Sequence(sequence_string_2), 
                        Sequence(sequence_string_3), matrix, -1)
    end_time = time.time()
    # output produced can be redirected into a CSV file
    print length_multiplier, ",", end_time - start_time