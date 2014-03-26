'''
Created on 26/03/2014

@author: s4361277
'''
import sequence as seq

seq1 = seq.Sequence('AAAAAAGGGGG')
print seq1.alphabet

seq2 = seq.Sequence('AAAAAGGGUG')
print seq2.alphabet

seq3 = seq.Sequence('AWAAAAAAGGVG')
print seq3.alphabet

#seq4 = seq.Sequence('Z')
#print seq3.alphabet


rns1 = seq.getSequence('RNS1_ARATH', 'uniprot')
print rns1.count('S')

#

id5 = seq.searchSequences("signal+peptide+AND+organism:Arabidopsis+thaliana[3702]+AND+length:[100+TO+*]")
id6 = seq.searchSequences("Lipid+metabolism+AND+organism:3702+AND+fragment:no+AND+length:[100+TO+*]")

print "ID5: ", id5.__len__(), " ID6: ", id6.__len__()

to_be_written = []
ids = set(id5).intersection(set(id6))

print ids.__len__()
for i in ids:
    pass
    #s = seq.getSequence(i)
    #to_be_written.append(s)
    #print s
    # iteritems???
#seq.writeFastaFile("results.fasta", to_be_written)