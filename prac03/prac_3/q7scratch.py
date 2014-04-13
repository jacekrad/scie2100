from sequence import *

seqA = getSequence("HQ659871.1", "genbank")
seqB = getSequence("JX416721.1", "genbank")

mat = readSubstMatrix("dna.matrix", DNA_Alphabet)

aln1 = alignGlobal(seqA, seqB, mat, -2)
aln1.writeHTML("alignment1.html")

aln1 = alignGlobal(seqA, seqB, mat, -4)
aln1.writeHTML("alignment2.html")
