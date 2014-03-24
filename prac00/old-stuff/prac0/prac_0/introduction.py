""" Welcome to introduction.py. This file contains a number of Python code
    examples from the Python reference guide, as well as some other code to
    get you started on practical 0.
    
    By the way, this is a comment which spans multiple lines. """

# Arithmetic
print 'Arithmetic examples:'
print 1/2
print float(1)/2

# Comparisons
print
print 'Comparison examples:'
print 1 > 2

# Variables
print
print 'Variable examples:'
a = 2
print a

# Strings
print
print 'String examples:'
dnaSeq = 'AGACGCGATGCGC'
print dnaSeq[::2]
print dnaSeq.count('A')
doubleQuotedString = "Note that double and single quotes both work."

# Lists
print
print 'List examples:'
mySeqs = ['AACGTCG', 'AGGGCCT', 'GGCGTAG']
print len(mySeqs)
mySeqs.reverse()
print mySeqs

# If
print
print 'If examples:'

seq = 'AGCU'
#seq = 'AGCT'
#seq = 'AGGCCAG'
if 'T' in seq:
    print 'The sequence is DNA.'
elif 'U' in seq:
    print 'The sequence is RNA.'
else:
    print "Can't tell what kind of sequence it is."

# While (this prints out every second symbol in the sequence)
print
print 'While loop examples:'

seq = 'AGGCTCG'
i = 0
while i < len(seq):
    if i % 2 == 0:
        print seq[i]
    i = i + 1

# For
print
print 'For loop examples:'

print 'The numbers 0 to 9:'
for i in range(10):
    print i

seq = 'AGCGCGATGCTGAG'
for symbol in seq:
    if symbol == 'A':
        print 'Found an adenine!'

# Arrays
print
print 'Array examples:'

import math

import numpy # Don't forget this line


matrix = numpy.zeros((2,2))
print matrix
matrix[1,1] = 10
print matrix

# Dictionaries
print
print 'Dictionary examples:'

nucleotides = {'A': 'adenine', 'G': 'guanine', 'C': 'cytosine', 'T': 'thymine'}
for base, name in nucleotides.items():
    print base, 'is for', name + '!'

# Standard Library
print
print 'Standard library examples:'

x = 7823.51
print math.cos(x)**2 + math.sin(x)**2, 'equals 1!'

# Functions
print
print 'Function examples:'

def reverseSequence(sequence):
    reverse = ''
    for symbol in sequence[::-1]:
        reverse += symbol
    return reverse
print reverseSequence('never odd or even')

# Classes
print
print 'Class examples:'

class MySequence:
    
    def __init__(self, sequence_as_string):
        self.sequence = sequence_as_string
    
    def getLength(self):
        return len(self.sequence)
    
    def countAdenine(self):
        return self.sequence.count('A')

mySeq = MySequence('AGCGCTAGATGC')
print 'Length:', mySeq.getLength()
print 'Adenine count:', mySeq.countAdenine()

exercise1_seq = "AAAACCTCTCTGTTCAGCACTTCCTCTCTCTTGGTCTGGTCTCAACGGTCACCATGGCGAGACCCTTGGAGGAGGCCCTGGATGTAATAGTGTCCACCTTCCACAAATACTCAGGCAACGAGGGTGACAAGTTCAAGCTGAACAAGACAGAGCTCAAGGAGCTACTGACCAGGGAGCTGCCTAGCTTCCTGGGGAGAAGGACAGACGAAGCTGCATTCCA"
exercise6_seq = "MHSSIVLATVLFVAIASASKTRELCMKSLEHAKVGTSKEAKQDGIDLYKHMFEHYPAMKKYFKHRENYTPADVQKDPFFIKQGQNILLACHVLCATYDDRETFDAYVGELMARHERDHVKVPNDVWNHFWEHFIEFLGSKTTLDEPTKHAWQEIGKEFSHEISHHGRHSVRDHCMNSLEYIAIGDKEHQKQNGIDLYKHMFEHYPHMRKAFKGRENFTKEDVQKDAFFVNKDTRFCWPFVCCDSSYDDEPTFDYFVDALMDRHIKDDIHLPQEQWHEFWKLFAEYLNEKSHQHLTEAEKHAWSTIGEDFAHEADKHAKAEKDHHEGEHKEEHH"
exercise9_seq = "GGCTAGAAGGATGGATGTTGTGAATGTTCCTGATGCAATGCAATCCTGTCACTAACATTAAAAACTTATCTTCCAACGCAAATCAAACGCCAAACAACCAACATAAAAGAACAAATGCTGCCTGCAAATCCACTCCCACATTGTCCGCTGTGGGTCCAGCTGCCGGGAAGGAGGCATAACCAGCTATCTTTGTGCTTCAGTGGGGCCTGGCTGGGTTTAGCTCAGGTGGTAACGATGCTCCCCCCGCGTGATATGGGATGAGAACTCGTACCTGTCCTGGCTGTGATAACCACACATGTTACACTCAAAGGGATCCCGAAAGCCATGGCAGCCATGGCAGCCCATGTGAATGGTATACATGACGTGATCCAGGAAGAGCACGCGGCAGTGTTCGCACTTGTACACCTTCAGCTGCTCGCCACTCGTGCTGACCACACGGAAGGCATCCTGCGAGTTCTCTGAGGCCGCCCTCAGCACCTCGTAGGCGCGCTGCTCCTCCTTGAGAGCCAGCCCATTGCGTGCATGCGGGTTGATGTGGTTGGTTAGGTAGATAAGGCCGCTGCGCTGTTCCTCCGCGTTGCTCTCTGTATCTGTGGAGTCTTGGCAGCTGTTGCTCGGGGAGGCCTCTCGCTCCGCTGACACAGACTTGGCCTTGGACAGCAGCAGCAAGTTATCCACGGCGTCCTGTGCTGAATGGTTGGACCGTGGGGGGCCATCTGAGGGGGGCTTGTGCAGCTGGTACATGGAGCTGATGACTGGCACCACCTCGGAGCTACCGGGGGGTGTCTGCACCAATGGGCGCAGGGACTCAGCCCCCAGGTAGTTGATGGCATTGTTGATGGCCTGGTCCATCACGTGGGATGTCATCATATCCTCCTTCTCATAGTTGGCACTGTCATAGGGCATGTCTGACAGGCACTTGTCTCCAAGAAATTTCTGAGGCATAGAGCTCTTACGTTTGGCGACATTGCTTGCCAGCCTGTCCAGGACAAGGGACCTCTCTGCTCCTATCTTGCACAGGTCTTCTGCCATCTCGTTGTGGTTAGTTTCTTCCTTAATGACTGGGCACACGCCCGGAAGGCCCATGCTTTCCAAGTAGTTGTGGCATCGCTCTTTATGCTCCTCTAAAGAGCTTCGCTGTTTATAGCTCCGGCCACAATATCCACATTTGTGAGGCTTACCAACGGAGTGCGTCCTCAGGTGGCCGGTGAGGGCGTCCCTCCGGCGGCAGGCATAGTTGCAAAGATGGCATTTGAAGGGCTTCTCACCCGAGTGCAGCTTGATGTGCCGCAGGAGGTTGCCTTTCTGGGTAAAGGAGGCCCCACACTGGTTGCACTGGAAAGGCCGTTCACCCATGCCTCGATCACTCTTGGAGTTCTGCTGTGCTCCAGAGGTAGTGGACAGGTCCTCAGGGACAGGCATGGGCTCATCCCCTTCATCTGGAGTGTCACTGACTGGGGGGCTCTCCTTTCCTGAAACTTGGGACATGTCTTGACCCTCATCGACATCCATTGTCTTCAGGTTATCAACAGACTTGTGCCTCCCCAAGG"


