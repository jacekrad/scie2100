'''
Created on 19/05/2014

@author: jacekrad
'''


genome1 = {"00680":86, "03010":59, "00230":36, "00240":35, "00860":24, \
           "00970":24, "00720":19, "00400":18, "02010":18, "00250":16}
genome2 = {"03010":53, "00230":51, "00190":43, "02020":40, "00240":37, \
           "00910":34, "02010":33, "00860":30, "00720":27, "00330":27}
genome3 = {"03010":49, "00230":47, "02010":40, "00240":38, "00860":32, \
           "00970":25, "00270":24, "00720":21, "00910":21, "00400":19}

genomes = [genome1, genome2, genome3]

scores = {}

for genome in genomes:
    for pathway in genome:
        score = genome.get(pathway)
        existing = scores.get(pathway)
        if existing == None:
            scores.update({pathway:score})
        else:
            scores.update({pathway:(existing + score)})
        
for key in scores:
    print scores.get(key), key