'''
Created on 02/03/2014

@author: jacekrad
'''
import unittest
from sequence import *


#-----------------------------------------------------------------------------        
# test class for Sequence
#-----------------------------------------------------------------------------        
class SequenceTest(unittest.TestCase):
    
    def setUp(self):
        self.alignment1 = readClustalFile("alignment1.aln", Protein_Alphabet)
        self.matrix1 = self.alignment1.calcSubstMatrix()
    
    def tearDown(self):
        pass

    def test__str__(self):
        print self.matrix1
        

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()