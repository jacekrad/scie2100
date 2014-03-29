'''
Created on 29/03/2014

@author: jacekrad
'''
from sequence import *

some_sequence = Sequence("GATTACA", DNA_Alphabet, "my DNA")

# this will call the __len__() method
print len(some_sequence)

# this will call the __str__() method
print some_sequence

# this will call the __iter__() method
# note in the absence of __iter__() method the code below
# would implicitly call the __getitem__() method 
for symbol in some_sequence:
    print "Symbol: ", symbol
    
# this wall call the __contains__() method
if "A" in some_sequence:
    print "found A"

# this will call the __getitem__() method
print some_sequence[2:4]