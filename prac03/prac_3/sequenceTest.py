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

    def testGlobalAlignment_gap8(self):
        aln_global_8 = alignGlobal(self.seqA, self.seqB, self.smat, -8)
        
    def testGlobalAlignment_gap4(self):
        aln_global_4 = alignGlobal(self.seqA, self.seqB, self.smat, -4)        

    def testLocalAlignment_gap8(self):
        aln_local_8 = alignLocal(self.seqA, self.seqB, self.smat, -8)
        
    def testLocalAlignment_gap4(self):
        aln_local_4 = alignLocal(self.seqA, self.seqB, self.smat, -4)
        print aln_local_4
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()