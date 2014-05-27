'''
Created on 27/05/2014

@author: s4361277
'''
from sequence import *

yeast_prom = readFastaFile("yeast_promoters.fa", DNA_Alphabet)

z = readMultiCount("abf1.jaspar")
abf1_pwm = PWM(z)


bind_map = {}
for s in yeast_prom: #yeast_prom is an array of sequences
    if abf1_pwm.maxscore(s)[0] > -24 and abf1_pwm.maxscore(s)[0] < -23.4:
        bind_map[s.name] = abf1_pwm.maxscore(s)[0] # save score only
scores = []
for s in bind_map.keys():
    if bind_map[s] != None:
        scores.append(bind_map[s])
print len(scores), " scrores"
import numpy as np
import matplotlib.pyplot as plt
hist, bins = np.histogram(scores, bins=50)
width = 0.7 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center', width=width)
plt.show()

print bind_map.keys()
# provide gene list from bind_map