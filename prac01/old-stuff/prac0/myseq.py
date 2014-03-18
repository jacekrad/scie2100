class MySequence:

    DNA_alpha = 'ACGT'
    RNA_alpha = 'ACGU'
    Protein_alpha = 'ACDEFGHIKLMNPQRSTVWY'

    def __init__(self, biostr, alphabet):
        self.alphabet=alphabet
        self.sequence=biostr

    def getCount(self, ch):
        return self.sequence.count(ch)
    
    def getCounts(self):
        """ Determines the counts of all characters in the alphabet.
            Returns the counts as a dictionary, keyed by the character."""
        d = {}
        for ch in self.alphabet:
            d[ch] = self.getCount(ch)
        return d

    def checkAlphabet(self, alpha):
        for ch in alpha:
            if not ch in self.alphabet:
                return False
        return True
                
    def reverseComplement(self):
        if not self.checkAlphabet('ACGT'):
            return None
        newseq = ''
        c = {'A':'T','T':'A','C':'G','G':'C'}
        for ch in self.sequence[::-1]:
            newseq += c[ch]
        return MySequence(newseq, self.alphabet)

