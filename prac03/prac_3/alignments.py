'''
Created on 12/04/2014

@author: jacekrad
'''

from lxml import etree
import threading as thread
from sequence import *


class AlignmentCollection():
    '''
    simple collection of multiple alignments
    main purpose of this class is to allow us to compare multiple alignments
    with each other analysing gaps etc
    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        self.alignments = []
        
    def add_alignment(self, alignment):
        """ append an alignment to this collection """
        self.alignments.append(alignment)
        
    def toXML(self):
        """ return XML representation of this collection of alignments """
        xml = "<alignments name=\"" + self.name + "\">\n"
        for alignment in self.alignments:
            xml += alignment.toXML()
        xml += "</alignments>\n"
        return xml
    
    def dump_xml_and_html(self, prefix = "output"):
        """ dump raw XML representation of these alignments as well as 
        transformed into HTML output into files named by the prefix """
        xml_filename = prefix + ".xml"
        html_filename = prefix + ".html"
        xslt_filename = "alignments_html.xsl"
        
        # dump XML
        open(xml_filename, "w").write(self.toXML())
        
        #dump HTML
        open(html_filename, "w").write(self.transform(xml_filename, xslt_filename))
        
    
    def transform(self, xmlPath, xslPath):
        xslRoot = etree.fromstring(open(xslPath).read())
        transform = etree.XSLT(xslRoot)
        xmlRoot = etree.fromstring(open(xmlPath).read())
        transRoot = transform(xmlRoot)
        return etree.tostring(transRoot)


class AlignmentThread (thread.Thread):
    
    def __init__(self, seqA, seqB, matrix_filename, gap_penalty, alphabet =  DNA_Alphabet):
        thread.Thread.__init__(self)
        self.seqA = seqA
        self.seqB = seqB
        self.matrix = readSubstMatrix(matrix_filename, alphabet)
        self.gap_penalty = gap_penalty
        self.result_alignment =  None
    
    def run(self):
        print "Starting " + self.name
        self.result_alignment = alignGlobal(self.seqA, self.seqB, self.matrix, self.gap_penalty)
        print self.name, " completed"
