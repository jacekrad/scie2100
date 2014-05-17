import unittest
import question1 as q1

class Q1Test(unittest.TestCase):
    
    data1 = [1, 2, 3, 4, 5]
    data2 = [1, 2, 3, 4, 5, 6]
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__mean__1(self):
        self.assertEquals(3, q1.get_mean(self.data1), "")
        
    def test__mean__2(self):
        self.assertEquals(3.5, q1.get_mean(self.data2), "")
        
    def test__standard_deviation__1(self):
        self.assertEquals(1.41, q1.get_standard_deviation(self.data1), "")    

    def test__standard_deviation__2(self):
        self.assertEquals(1.71, q1.get_standard_deviation(self.data2), "")    
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
