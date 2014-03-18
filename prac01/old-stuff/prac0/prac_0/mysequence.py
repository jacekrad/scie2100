'''
Created on 04/03/2014

@author: s4361277
'''

#from guide import Alphabet
import guide, translate

exercise1_seq = "AAAACCTCTCTGTTCAGCACTTCCTCTCTCTTGGTCTGGTCTCAACGGTCACCATGGCGAGACCCTTGGAGGAGGCCCTGGATGTAATAGTGTCCACCTTCCACAAATACTCAGGCAACGAGGGTGACAAGTTCAAGCTGAACAAGACAGAGCTCAAGGAGCTACTGACCAGGGAGCTGCCTAGCTTCCTGGGGAGAAGGACAGACGAAGCTGCATTCCA"
exercise6_seq = "MHSSIVLATVLFVAIASASKTRELCMKSLEHAKVGTSKEAKQDGIDLYKHMFEHYPAMKKYFKHRENYTPADVQKDPFFIKQGQNILLACHVLCATYDDRETFDAYVGELMARHERDHVKVPNDVWNHFWEHFIEFLGSKTTLDEPTKHAWQEIGKEFSHEISHHGRHSVRDHCMNSLEYIAIGDKEHQKQNGIDLYKHMFEHYPHMRKAFKGRENFTKEDVQKDAFFVNKDTRFCWPFVCCDSSYDDEPTFDYFVDALMDRHIKDDIHLPQEQWHEFWKLFAEYLNEKSHQHLTEAEKHAWSTIGEDFAHEADKHAKAEKDHHEGEHKEEHH"
exercise9_seq = "GGCTAGAAGGATGGATGTTGTGAATGTTCCTGATGCAATGCAATCCTGTCACTAACATTAAAAACTTATCTTCCAACGCAAATCAAACGCCAAACAACCAACATAAAAGAACAAATGCTGCCTGCAAATCCACTCCCACATTGTCCGCTGTGGGTCCAGCTGCCGGGAAGGAGGCATAACCAGCTATCTTTGTGCTTCAGTGGGGCCTGGCTGGGTTTAGCTCAGGTGGTAACGATGCTCCCCCCGCGTGATATGGGATGAGAACTCGTACCTGTCCTGGCTGTGATAACCACACATGTTACACTCAAAGGGATCCCGAAAGCCATGGCAGCCATGGCAGCCCATGTGAATGGTATACATGACGTGATCCAGGAAGAGCACGCGGCAGTGTTCGCACTTGTACACCTTCAGCTGCTCGCCACTCGTGCTGACCACACGGAAGGCATCCTGCGAGTTCTCTGAGGCCGCCCTCAGCACCTCGTAGGCGCGCTGCTCCTCCTTGAGAGCCAGCCCATTGCGTGCATGCGGGTTGATGTGGTTGGTTAGGTAGATAAGGCCGCTGCGCTGTTCCTCCGCGTTGCTCTCTGTATCTGTGGAGTCTTGGCAGCTGTTGCTCGGGGAGGCCTCTCGCTCCGCTGACACAGACTTGGCCTTGGACAGCAGCAGCAAGTTATCCACGGCGTCCTGTGCTGAATGGTTGGACCGTGGGGGGCCATCTGAGGGGGGCTTGTGCAGCTGGTACATGGAGCTGATGACTGGCACCACCTCGGAGCTACCGGGGGGTGTCTGCACCAATGGGCGCAGGGACTCAGCCCCCAGGTAGTTGATGGCATTGTTGATGGCCTGGTCCATCACGTGGGATGTCATCATATCCTCCTTCTCATAGTTGGCACTGTCATAGGGCATGTCTGACAGGCACTTGTCTCCAAGAAATTTCTGAGGCATAGAGCTCTTACGTTTGGCGACATTGCTTGCCAGCCTGTCCAGGACAAGGGACCTCTCTGCTCCTATCTTGCACAGGTCTTCTGCCATCTCGTTGTGGTTAGTTTCTTCCTTAATGACTGGGCACACGCCCGGAAGGCCCATGCTTTCCAAGTAGTTGTGGCATCGCTCTTTATGCTCCTCTAAAGAGCTTCGCTGTTTATAGCTCCGGCCACAATATCCACATTTGTGAGGCTTACCAACGGAGTGCGTCCTCAGGTGGCCGGTGAGGGCGTCCCTCCGGCGGCAGGCATAGTTGCAAAGATGGCATTTGAAGGGCTTCTCACCCGAGTGCAGCTTGATGTGCCGCAGGAGGTTGCCTTTCTGGGTAAAGGAGGCCCCACACTGGTTGCACTGGAAAGGCCGTTCACCCATGCCTCGATCACTCTTGGAGTTCTGCTGTGCTCCAGAGGTAGTGGACAGGTCCTCAGGGACAGGCATGGGCTCATCCCCTTCATCTGGAGTGTCACTGACTGGGGGGCTCTCCTTTCCTGAAACTTGGGACATGTCTTGACCCTCATCGACATCCATTGTCTTCAGGTTATCAACAGACTTGTGCCTCCCCAAGG"
DNA_alpha = 'ACGT'
RNA_alpha = 'ACGU'
Protein_alpha = 'ACDEFGHIKLMNPQRSTVWY'

def baseCounts(sequence):
    """Print base count in a given sequence."""
    aCount = 0;
    cCount = 0;
    gCount = 0;
    tCount = 0;
    for letter in sequence:
        if letter == "A":
            aCount += 1
        elif letter == "C":
            cCount += 1
        elif letter == "G":
            gCount += 1
        elif letter == "T":
            tCount += 1;
        else:
            print"invalid letter ", letter

    print "Base counts:"
    print "A: ", aCount
    print "C: ", cCount
    print "G: ", gCount
    print "T: ", tCount
            
def baseCounts2(sequence, alphabet):
    """Print base count in a give sequence based on the alphabet."""
    counts={} 
    for letter in alphabet:
        counts[letter]=sequence.count(letter)

    print "Base counts:"

    for letter in alphabet:
        print letter, ": ", counts[letter]
                        
                        
def baseCounts3(sequence, alphabet):
    """return base counts as a dictionary of letter:count pairs"""
    counts={} 
    for letter in alphabet:
        counts[letter]=sequence.count(letter)

    return counts

class MySequence():
    def __init__(self, sequence, alphabet):
        self.sequence = sequence
        self.alphabet = alphabet
        
    def getBaseCountsOld(self):
        counts={} 
        for letter in self.alphabet:
            counts[letter] = self.sequence.count(letter)
        return counts

    def getCount(self, letter):
        val  = self.sequence.count(letter)
        return val
        
    def getBaseCounts(self):
        counts={} 
        for letter in self.alphabet:
            counts[letter] = self.getCount(letter)
        return counts
    
    def getDNAComplementBase(self, letter):
        if letter == "A":
            return "T"
        elif letter == "T":
            return "A"
        elif letter == "C":
            return "G"
        elif letter == "G":
            return "C"
        else: # error condition
            return "*"
    
    def getReverseComplement(self):
        complementString = ""
        for letter in self.sequence[::-1]:
            complementString += self.getDNAComplementBase(letter)
        complement = MySequence(complementString, self.alphabet)
        return complement
        
    def translateDNA(self):
        i = 0
        aminoAcidSequence = "" 
        while i < len(self.sequence):
            codon = self.sequence[i:i+3]
            i += 3
            aminoAcidSequence += translate.standardTranslation.get(codon)
            #print "codon : ", codon, " aminoacid: " + translate.standardTranslation.get(codon)
        return aminoAcidSequence
    
    #-------------------------------------------------------------------------
    # translate DNA into aminoacid sequence
    #    reading frame - 0, 1 or 2
    #    reverse - boolean .  if true then translate reverse complement
    #-------------------------------------------------------------------------
    def translateDNA2(self, readingFrame, reverse):
        sequence = None
        if reverse:
            sequence = self.getReverseComplement()
        else:
            sequence = self
        i = readingFrame
        aminoAcidSequence = "" 
        while i < len(sequence.sequence):
            codon = sequence.sequence[i:i+3]
            i += 3
            result = translate.standardTranslation.get(codon)
            if result != None:
                aminoAcidSequence += result
                #print "codon : ", codon, " aminoacid: " + translate.standardTranslation.get(codon)
        return aminoAcidSequence
        
    def printCounts(self):        
        counts = self.getBaseCounts()
        for letter in self.alphabet:
            print letter, ": ", counts[letter]
                
#baseCounts(exercise1_seq)
#baseCounts2(exercise1_seq, DNA_alpha)
print "-----------------------------------"
#s = MySequence(exercise1_seq, DNA_alpha)
#print s.getCount("A")
#s = MySequence("AACCGGGGGGTTTTCATTAAA", DNA_alpha)
#print s.getReverseComplement().sequence
#print s.translateDNA2(0, False)
#print s.translateDNA2(0, True)
#print s.translateDNA2(1, True)

mouseSequence = MySequence(exercise9_seq, DNA_alpha)
aminoSequence = None
for frame in range(3):
    aminoSequence = mouseSequence.translateDNA2(frame, True)
    position = aminoSequence.find("M")
    if position != -1:
        print "Full Frame= ", frame, " ", aminoSequence[position:]
        print "Sequence  = ", frame, " ", aminoSequence[position:position+100]
