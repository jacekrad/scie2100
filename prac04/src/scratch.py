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

start_time = time.time()
tripletAlignGlobal(seqA1, seqB1, seqC1, matrix, -1)
end_time = time.time()
print("Elapsed time was %g seconds" % (end_time - start_time))


start_time = time.time()
tripletAlignGlobal(seqA2, seqB2, seqC2, matrix, -1)
end_time = time.time()
print("Elapsed time was %g seconds" % (end_time - start_time))

multi_align_sequences = readFastaFile("multiAlign.fasta", DNA_Alphabet)

start_time = time.time()
alignment = runClustal(multi_align_sequences)
end_time = time.time()
print("Elapsed time was %g seconds" % (end_time - start_time))

alignment.writeClustal("multiAlign.aln")

alignment.writeHTML("alignment.html")

#question 5
motif_sequences = readFastaFile("motifSequences.fasta", DNA_Alphabet)

motif_alignment = runClustal(motif_sequences)

motif_alignment.writeClustal("myAlign.aln")

motif_alignment.writeHTML("myAlign.html")


#qeuestion 8
regexp = Regexp(".TA[AG]")
results = regexp.search("CTAGAGCGCTAAGCCGA")
print results



print "done"