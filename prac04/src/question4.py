'''
Created on 15/04/2014

@author: s4361277
'''
from sequence import *
import time

multi_align_sequences = readFastaFile("multiAlign.fasta", DNA_Alphabet)

start_time = time.time()
alignment = runClustal(multi_align_sequences)
end_time = time.time()
print("Elapsed time was %g seconds" % (end_time - start_time))

alignment.writeClustal("multiAlign.aln")
alignment.writeHTML("alignment.html")
