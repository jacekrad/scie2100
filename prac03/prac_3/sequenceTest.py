'''
Created on 08/04/2014

@author: s4361277
'''
import unittest

from sequence import *

class SequenceTest(unittest.TestCase):


    def setUp(self):
        self.seqA = Sequence('THISLINE', Protein_Alphabet, name='SeqA')
        self.seqB = Sequence('ISALIGNED', Protein_Alphabet, name='SeqB')
        self.smat = readSubstMatrix('blosum62.matrix', Protein_Alphabet)



    def tearDown(self):
        pass

    def testGlobalAlignment_gap8_test(self):
        aln_global_8 = alignGlobal(self.seqA, self.seqB, self.smat, -8)
        expected1 = aln_global_8.seqs[0].getSeqString()
        expected2 = aln_global_8.seqs[1].getSeqString()
        self.assertEquals("THISLINE-", expected1, expected1)
        self.assertEquals("ISALIGNED", expected2, expected2)
        
    def testGlobalAlignment_gap4_test(self):
        aln_global_4 = alignGlobal(self.seqA, self.seqB, self.smat, -4)        
        expected1 = aln_global_4.seqs[0].getSeqString()
        expected2 = aln_global_4.seqs[1].getSeqString()
        self.assertEquals("THIS-LI-NE-", expected1, expected1)
        self.assertEquals("--ISALIGNED", expected2, expected2)

    def testLocalAlignment_gap8_test(self):
        aln_local_8 = alignLocal(self.seqA, self.seqB, self.smat, -8)
        expected1 = aln_local_8.seqs[0].getSeqString()
        expected2 = aln_local_8.seqs[1].getSeqString()
        self.assertEquals("SLI-NE", expected1, expected1)
        self.assertEquals("ALIGNE", expected2, expected2)        
        
    def testLocalAlignment_gap4_test(self):
        aln_local_4 = alignLocal(self.seqA, self.seqB, self.smat, -4)
        expected1 = aln_local_4.seqs[0].getSeqString()
        expected2 = aln_local_4.seqs[1].getSeqString()
        self.assertEquals("IS-LI-NE", expected1, expected1)
        self.assertEquals("ISALIGNE", expected2, expected2)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()