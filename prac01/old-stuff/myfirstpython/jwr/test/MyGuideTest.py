'''
Created on 02/03/2014

@author: jacekrad
'''
import unittest
from jwr.MyGyuide import Alphabet, Sequence
from twisted.names.dns import DNAME

#-----------------------------------------------------------------------------        
# test class for Alphabet
#-----------------------------------------------------------------------------        
class AlphabetTest(unittest.TestCase):
    
    def setUp(self):
        self.alphabet = Alphabet("ABCDEFG")

    def tearDown(self):
        pass

    # test __contains__ for a letter in alphabet
    def test__contains__1(self):
        self.assertTrue("A" in self.alphabet, "A should be in the alphabet")

    # test __contains__ for letter NOT in alphabet
    def test__contains__2(self):
        self.assertFalse("Z" in self.alphabet, "Z should NOT be in the alphabet")
        
#-----------------------------------------------------------------------------        
# test class for Sequence
#-----------------------------------------------------------------------------        
class SequenceTest(unittest.TestCase):
    
    def setUp(self):
        self.DNA_alphabet = Alphabet("ACTG")
        self.sequence = Sequence('ACCTTTGGGG', self.DNA_alphabet, "SEQ")
    
    def tearDown(self):
        pass

    def test__str__(self):
        self.assertEqual("SEQ: ACCTTTGGGG", self.sequence.__str__(), "failed")
        
    def test_get_symbol_count(self):
        self.assertEqual(4, self.sequence.get_symbol_count('G'), "failed")
        self.assertEqual(3, self.sequence.get_symbol_count('T'), "failed")
        
    def test_find(self):
        self.assertEqual(6, self.sequence.find("G"), "failed")
        self.assertEqual(6, self.sequence.find("GGGG"), "failed")
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()