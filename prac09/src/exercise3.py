'''
Created on 27/05/2014

@author: s4361277
'''
from sequence import *

z = readMultiCount("abf1.jaspar")
pwm = PWM(z)
letters = ['A', 'C', 'G', 'T']
print pwm

print "PWM 10'th column"
for i in range(0, 4):
    print letters[i], pwm.m[i][9]

