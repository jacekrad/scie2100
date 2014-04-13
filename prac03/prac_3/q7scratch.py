from sequence import *

HQ659871_1 = getSequence("HQ659871.1", "genbank")
JX416721_1 = getSequence("JX416721.1", "genbank")

mat = readSubstMatrix("dna.matrix", DNA_Alphabet)

aln1 = alignGlobal(HQ659871_1, JX416721_1, mat, -2)
aln1.writeHTML("alignment1.html")

aln1 = alignGlobal(HQ659871_1, JX416721_1, mat, -4)
aln1.writeHTML("alignment2.html")
