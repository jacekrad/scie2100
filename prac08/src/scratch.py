'''
Created on 20/05/2014

@author: s4361277
'''
from sequence import *
from symbol import *
from sstruct import *

proteins = readFastaFile("prot2.fa", Protein_Alphabet)
structures =  readFastaFile("sstr3.fa", DSSP3_Alphabet)

myprot = Sequence('PNKRKGFSEGLWEIENNPTVKASGY', Protein_Alphabet, '2NLU_r76')
myprot = Sequence("SEQSICQARAAVMVYDDANKKWVPAGGSTGFSRVHIYHHTGNNTFRVVGRKIQDHQVVINCAIPKGLKYNQATQTFHQWRDARQVYGLNFGSKEDANVFASAMMHALEVLN", Protein_Alphabet, "1EVH")
alpha = getScores(myprot, 0)
calls_a1 = markCountAbove(alpha, width = 6, call_cnt = 4)


alpha = getScores(myprot, 0)
beta = getScores(myprot, 1)

calls_a1 = markCountAbove(alpha, width = 6, call_cnt = 4)
calls_a2 = extendDownstream(alpha, calls_a1, width = 4)
calls_a3 = extendUpstream(alpha, calls_a2, width = 4)

calls_b1 = markCountAbove(beta, width = 5, call_cnt = 3)
calls_b2 = extendDownstream(beta, calls_b1, width = 4)
calls_b3 = extendUpstream(beta, calls_b2, width = 4)

avg_a = calcRegionAverage(alpha, calls_a3)
avg_b = calcRegionAverage(beta, calls_b3)

diff_a = [avg_a[i] - avg_b[i] for i in range(len(avg_a))]
diff_b = [avg_b[i] - avg_a[i] for i in range(len(avg_a))]

calls_a4 = checkSupport(calls_a3, diff_a)
calls_b4 = checkSupport(calls_b3, diff_b)

print myprot
print "     ", makesstr(calls_a4, 'H')
print "     ", makesstr(calls_b4, 'E')

