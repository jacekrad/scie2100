'''
Created on 07/05/2014

@author: s4361277
'''
from genome import *

ge3716 = readGEOFile("GDS3716.soft")

# question 1a

# get cancerous and healthe samples
# first ER+: GSM512557
# corresponding healthy: GSM512539
samples = ge3716.getSamples([ge3716.getHeaderIndex("GSM512557"), \
                             ge3716.getHeaderIndex("GSM512539")])

probes = []
probes.append(samples.get("204531_s_at"))
probes.append(samples.get("209969_s_at"))
probes.append(samples.get("211300_s_at"))

print "healthy\terplus\tratio\tlogratio"
for probe in probes:
    healthy = probe[1]
    erplus = probe[0]
    ratio = erplus / healthy
    logratio = math.log(ratio, 2)
    print healthy, erplus, ratio, logratio
 