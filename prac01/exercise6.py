'''
Created on 29/03/2014

@author: jacekrad
'''

import sequence as seq
import os.path as path
import util

""" filenames where we save the results from question 5 & 6 respectively """
ex5_filename = "sigpep_at.fa"
ex6_filename = "lipmet_at.fa"

""" for both questions 5 and 6 we check if the fasta file already exists 
    and only do the searches and obtain sequences if false 
    this way we can rerun the program quickly without rebuilding the 
    fasta file each and every time
"""

util.searchAndSave("signal+peptide+AND+organism:Arabidopsis+thaliana[3702]+" 
                    + "AND+length:[100+TO+*]", ex5_filename)

util.searchAndSave("Lipid+metabolism+AND+organism:3702+AND+fragment:no+"
                    + "AND+length:[100+TO+*]", ex6_filename)
