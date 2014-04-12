'''
Created on 08/04/2014

@author: s4361277
unit tests:
prac 3
questions 1 & 2
'''
import unittest

from sequence import Sequence, Protein_Alphabet, readSubstMatrix, alignGlobal, alignLocal

class SequenceTest(unittest.TestCase):

    def setUp(self):
        self.seqA = Sequence("THISLINE", Protein_Alphabet, name="SeqA")
        self.seqB = Sequence("ISALIGNED", Protein_Alphabet, name="SeqB")
        self.blosum62_matrix = readSubstMatrix("blosum62.matrix", Protein_Alphabet)

    def tearDown(self):
        pass

    def testQuestion1_8(self):
        """ test question 1; global alignment with a gap penalty of -8 """ 
        aln_global_8 = alignGlobal(self.seqA, self.seqB, self.blosum62_matrix, -8)
        expected1 = aln_global_8.seqs[0].getSeqString()
        expected2 = aln_global_8.seqs[1].getSeqString()
        self.assertEquals("THISLINE-", expected1)
        self.assertEquals("ISALIGNED", expected2)
        
    def testQuestion1_4(self):
        """ test question 1; global alignment with a gap penalty of -4 """         
        aln_global_4 = alignGlobal(self.seqA, self.seqB, self.blosum62_matrix, -4)        
        expected1 = aln_global_4.seqs[0].getSeqString()
        expected2 = aln_global_4.seqs[1].getSeqString()
        self.assertEquals("THIS-LI-NE-", expected1)
        self.assertEquals("--ISALIGNED", expected2)

    def testQuestion2_8(self):
        """ test question 2; local alignment with a gap penalty of -8 """         
        aln_local_8 = alignLocal(self.seqA, self.seqB, self.blosum62_matrix, -8)
        expected1 = aln_local_8.seqs[0].getSeqString()
        expected2 = aln_local_8.seqs[1].getSeqString()
        self.assertEquals("SLI-NE", expected1)
        self.assertEquals("ALIGNE", expected2)        
        
    def testQuestion2_4(self):
        """ test question 2; local alignment with a gap penalty of -4 """         
        aln_local_4 = alignLocal(self.seqA, self.seqB, self.blosum62_matrix, -4)
        expected1 = aln_local_4.seqs[0].getSeqString()
        expected2 = aln_local_4.seqs[1].getSeqString()
        self.assertEquals("IS-LI-NE", expected1)
        self.assertEquals("ISALIGNE", expected2)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()