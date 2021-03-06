"""
Module *** sequence ***

This module depends on the following modules

symbol -- defines an alphabet
prob -- defines structures to hold probabilities (prob also depends on symbol) 

This module incorporates classes for

Sequence -- names and defines a sequence of symbols; computes various transformations and pairwise alignments
Alignment -- defines a multiple sequence alignment; computes stats for use in substitution matrices
SubstMatrix -- substitution matrix class to support alignment methods
Regexp -- defines patterns as regular expressions for textual pattern matching in sequences
PWM -- defines a weight matrix that can score any site in actual sequences 

Incorporates methods for loading and saving files relevant to the above (e.g. FASTA, ALN, substitution matrices)
and methods for retrieving relevant data from web services 
"""

import string, sys, re, math, os, array
import numpy
from webservice import *
from symbol import *
from prob import *

# Sequence ------------------

class Sequence(object):
    """ A biological sequence. Stores the sequence itself (as a compact array), 
    the alphabet (i.e., type of sequence it is), and optionally a name and further 
    information. """
    
    sequence = None # The array of symbols that make up the sequence 
    alphabet = None # The alphabet from which symbols come
    name =     None # The name (identifier) of a sequence
    info =     None # Other information (free text; e.g. annotations)
    length =   None # The number of symbols that the sequence is composed of
    gappy =    None # True if the sequence has "gaps", i.e. positions that represent deletions relative another sequence
    
    def __init__(self, sequence, alphabet = None, name = '', info = '', gappy = False):
        """ Create a sequence with the sequence data. Specifying the alphabet,
        name and other information about the sequence are all optional.
        The sequence data is immutable (stored as a string).
        Example:
        >>> myseq = Sequence('MVSAKKVPAIAMSFGVSF')
        will create a sequence with no name, and assign one of the predefined
        alphabets on the basis of what symbols were used.
        >>> myseq.alphabet.symbols
        will output the standard protein alphabet:
        ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q',
        'R', 'S', 'T', 'V', 'W', 'Y'] """
        
        try: # convert sequence data into a compact array representation
            self.sequence = array.array('c', ''.join([s.upper() for s in sequence]))
        except TypeError:
            raise RuntimeError('Sequence data is not specified correctly: must be iterable')
        
        # Assign an alphabet
        self.alphabet = None
        if not alphabet is None:
            for sym in self.sequence:
                if not sym in alphabet and (sym != '-' or not gappy):  # error check: bail out
                    raise RuntimeError('Invalid symbol: %c in sequence %s' % (sym, name))
            self.alphabet = alphabet
        else:
            for alphaName in preferredOrder:
                alpha = predefAlphabets[alphaName]
                valid = True
                for sym in self.sequence:
                    if not sym in alpha and (sym != '-' or not gappy):  
                        valid = False
                        break
                if valid:
                    self.alphabet = alpha
                    break
            if self.alphabet is None:
                raise RuntimeError('Could not identify alphabet from sequence: %s' % name)
        
        # Store other information
        self.name = name
        self.info = info
        self.length = len(self.sequence)
        self.gappy = gappy
        
    def __len__(self):
        """ Defines what the "len" operator returns for an instance of Sequence, e.g.
        >>> seq = Sequence('ACGGTAGGA', DNA_Alphabet)
        >>> print len(seq)
        9
        """
        return len(self.sequence)

    def __str__(self):
        """ Defines what should be printed when the print statement is used on a Sequence instance """
        str = self.name + ': '
        for sym in self:
            str += sym
        return str
    
    def __iter__(self):
        """ Defines how a Sequence should be "iterated", i.e. what its elements are, e.g.
        >>> seq = new Sequence('AGGAT', DNA_Alphabet)
        >>> for sym in seq:
                print sym
        will print A, G, G, A, T (each on a separate row)
        """ 
        tsyms = tuple(self.sequence)
        return tsyms.__iter__()
    
    def __contains__(self, item):
        """ Defines what is returned when the "in" operator is used on a Sequence, e.g.
        >>> seq = Sequence('ACGGTAGGA', DNA_Alphabet)
        >>> print 'T' in seq
        True
            which is equivalent to 
        >>> print seq.__contains__('T')
        True
        >>> print 'X' in seq
        False
        """ 
        for sym in self.sequence:
            if sym == item:
                return True
        return False
        
    def __getitem__(self, ndx):
        """ Retrieve a specified index (or a "slice" of indices) of the sequence data.
            Calling self.__getitem__(3) is equivalent to self[3] 
        """
        if type(ndx) is slice:
            return self.sequence[ndx].tostring()
        else:
            return self.sequence[ndx]
        
    def writeFasta(self):
        """ Write one sequence in FASTA format to a string and return it. """
        fasta = '>' + self.name + ' ' + self.info + '\n'
        data = self.sequence.tostring()
        nlines = (len(self.sequence) - 1) / 60 + 1
        for i in range(nlines):
            lineofseq = ''.join(data[i*60 : (i+1)*60]) + '\n'
            fasta += lineofseq
        return fasta
    
    def count(self, findme = None):
        """ Get the number of occurrences of specified symbol findme OR
            if findme = None, return a dictionary of counts of all symbols in alphabet """
        if findme != None:
            cnt = 0
            for sym in self.sequence:
                if findme == sym:
                    cnt = cnt + 1
            return cnt
        else:
            symbolCounts = {}
            for symbol in self.alphabet:
                symbolCounts[symbol] = self.count(symbol)
            return symbolCounts

    def find(self, findme):
        """ Find the position of the specified symbol or sub-sequence """
        return self.sequence.tostring().find(findme)

"""
Below are some useful methods for loading data from strings and files.
Recognize the FASTA format (nothing fancy). 
"""
def readFasta(string, alphabet = None):
    """ Read the given string as FASTA formatted data and return the list of
    sequences contained within it. """
    seqlist = []    # list of sequences contained in the string 
    seqname = None  # name of *current* sequence 
    seqinfo = None
    seqdata = []    # sequence data for *current* sequence
    for line in string.splitlines():    # read every line
        if len(line) == 0:              # ignore empty lines
            continue
        if line[0] == '>':  # start of new sequence            
            if seqname:     # check if we've got one current
                try:
                    current = Sequence(seqdata, alphabet, seqname, seqinfo)
                    seqlist.append(current)
                except RuntimeError as errmsg:
                    print "Error for sequence %s: %s" % (seqname, errmsg)
            # now collect data about the new sequence
            seqinfo = line[1:].split() # skip first char
            if len(seqinfo) > 0:
                parsed = parseDefline(seqinfo[0])
                seqname = parsed[0]
                seqinfo = line[1:]
            else:
                seqname = ''
                seqinfo = ''
            seqdata = []
        else:               # we assume this is (more) data for current
            cleanline = line.split()
            for thisline in cleanline:
                seqdata.extend(tuple(thisline.strip('*')))
    # we're done reading the file, but the last sequence remains
    if seqname:
        try:
            lastseq = Sequence(seqdata, alphabet, seqname, seqinfo)
            seqlist.append(lastseq)
        except RuntimeError as errmsg:
            print "Error for sequence %s: %s" % (seqname, errmsg)
    return seqlist

def parseDefline(string):
    """ Parse the FASTA defline (see http://en.wikipedia.org/wiki/FASTA_format)
        GenBank, EMBL, etc                gi|gi-number|gb|accession|locus
        SWISS-PROT, TrEMBL                sp|accession|name
        ...
        Return a tuple with 
        [0] primary search key, e.g. UniProt accession, Genbank GI
        [1] secondary search key, e.g. UniProt name, Genbank accession 
        [2] source, e.g. 'sp' (SwissProt/UniProt), 'tr' (TrEMBL), 'gb' (Genbank)
    """
    if len(string) == 0: return ('', '', '', '')
    s = string.split()[0]
    if re.match("sp\|[A-Z][A-Z0-9]{5}\|\S+", s):            arg = s.split('|');  return (arg[1], arg[2], arg[0], '')
    elif re.match("tr\|[A-Z][A-Z0-9]{5}\|\S+", s):          arg = s.split('|');  return (arg[1], arg[2], arg[0], '')
    elif re.match("gi\|[0-9]*\|gb|emb|dbj\|\S+\|\S+", s):   arg = s.split('|');  return (arg[1], arg[3], arg[2], arg[4])
    elif re.match("refseq\|\S+\|\S+", s):                   arg = s.split('|');  return (arg[1], arg[2], arg[0], '')
    else: return (s, '', '', '')

def readFastaFile(filename, alphabet = None):
    """ Read the given FASTA formatted file and return the list of sequences 
    contained within it. Note that if no alphabet is specified, it will take a 
    separate guess for each sequence. """
    fh = open(filename)
    seqlist = []
    batch = '' # a batch of rows including one or more complete FASTA entries
    rowcnt = 0 
    for row in fh:
        row = row.strip()
        if len(row) > 0:
            if row.startswith('>') and rowcnt > 0:
                more = readFasta(batch, alphabet)
                if len(more) > 0:
                    seqlist.extend(more)
                batch = ''
                rowcnt = 0
            batch += row + '\n'
            rowcnt += 1
    if len(batch) > 0:
        more = readFasta(batch, alphabet)
        if len(more) > 0:
            seqlist.extend(more)
    fh.close()
    return seqlist

def writeFastaFile(filename, sequences):
    """ Write the specified sequences to a FASTA file. """
    fh = open(filename, 'w')
    for seq in sequences:
        fh.write(seq.writeFasta())
    fh.close()
    
def getMarkov(sequences, order = 0):
    """ Retrieve the Markov stats for a set of sequences. """
    myseqs = sequences
    if sequences is Sequence:
        myseqs = list([sequences])
    myalpha = None
    for seq in myseqs:
        if myalpha == None:
            myalpha = seq.alphabet
        else:
            if seq.alphabet != myalpha:
                raise RuntimeError('Sequence ' + seq.name + ' uses an invalid alphabet ')
    jp = Joint([myalpha for _ in range(order + 1)])
    for seq in myseqs:
        for i in range(len(seq) - order):
            sub = seq[i:i + order + 1]
            jp.observe(sub)
    return jp

def getCount(sequences, findme = None):
    if findme != None:
        cnt = 0
        for seq in sequences:
            cnt += seq.count(findme)
        return cnt
    else: 
        if len(sequences) > 0:
            alpha = sequences[0].alphabet
            patcnt = {}
            for a in alpha:
                patcnt[a] = getCount(sequences, a)
        return patcnt
    
# Alignment ------------------

class Alignment():
    """ A sequence alignment class. Stores two or more sequences of equal length where
    one symbol is gap '-' 
    Example usage:
    >>> sequences = [Sequence('THIS_LI_NE', Protein_Alphabet, gappy = True), Sequence('--ISALIGNED', Protein_Alphabet, gappy = True)]
    >>> print Alignment(sequences)
     THIS-LI-NE-
     --ISALIGNED """
    
    alignlen = None
    sequences = None
    alphabet = None
    
    def __init__(self, sequences):
        self.alignlen = -1
        self.seqs = sequences
        self.alphabet = None
        for s in sequences:
            if self.alignlen == -1:
                self.alignlen = len(s)
            elif self.alignlen != len(s):
                raise RuntimeError("Alignment invalid: different lengths")
            if self.alphabet != None and self.alphabet != s.alphabet:
                raise RuntimeError("Alignment invalid: different alphabets")
            self.alphabet = s.alphabet

    def getnamelen(self):
        namelen = 0
        for seq in self.seqs:
            namelen = max(len(seq.name), namelen)
        return namelen
    
    def __str__(self):    
        string = ''
        namelen = self.getnamelen()
        for seq in self.seqs:
            string += seq.name.ljust(namelen+1)
            for sym in seq:
                string += sym
            string += '\n'
        return string

    def writeClustal(self, filename = None):
        """ Write the alignment to a string or file using the Clustal file format. """
        symbolsPerLine = 60
        maxNameLength =  self.getnamelen() + 1
        string = ''
        wholeRows = self.alignlen / symbolsPerLine
        for i in range(wholeRows):
            for j in range(len(self.seqs)):
                string += self.seqs[j].name.ljust(maxNameLength) + ' '
                string += self.seqs[j][i*symbolsPerLine:(i+1)*symbolsPerLine] + '\n'
            string += '\n'
        # Possible last row
        lastRowLength = self.alignlen - wholeRows*symbolsPerLine
        if lastRowLength > 0:
            for j in range(len(self.seqs)):
                if maxNameLength > 0:
                    string += self.seqs[j].name.ljust(maxNameLength) + ' '
                string += self.seqs[j][-lastRowLength:] + '\n'
        if filename != None:
            fh = open(filename, 'w')
            fh.write('CLUSTAL W (1.83) multiple sequence alignment\n\n\n') # fake header so that clustal believes it
            fh.write(string)
            fh.close()
        return string
    
    def getProfile(self, pseudo = 0.0):
        """ Determine the probability matrix from the alignment, assuming
        that each position is independent of all others. """
        p = IndepJoint([self.alphabet for _ in range(self.alignlen)], pseudo)
        for seq in self.seqs:
            p.observe(seq)
        return p 
        
    def calcBackground(self):
        """ Count the proportion of each amino acid's occurrence in the
            alignment, and return as a probability distribution. """
        p = Distrib(self.alphabet)
        for seq in self.alignments:
            for sym in seq:
                if sym in self.alphabet: # ignore "gaps"
                    p.observe(sym)
        return p
    
    def writeHTML(self, filename = None):
        """ Generate HTML that displays the alignment in color. 
            Requires that the alphabet is annotated with the label 'html-color' (see Sequence.annotateSym)
            and that each symbol maps to a text string naming the color, e.g. 'blue'
        """
        html = '''<html><head><meta content="text/html; charset=ISO-8859-1" http-equiv="Content-Type">\n<title>Sequence Alignment</title>\n</head><body><pre>\n'''
        maxNameLength =  self.getnamelen()
        html += ''.ljust(maxNameLength) + ' '
        for i in range(self.alignlen - 1):
            if (i+1) % 10 == 0:
                html += str(i/10+1)[-1]
            else:
                html += ' '
        html += '%s\n' % (self.alignlen)
        if self.alignlen > 10:
            html += ''.ljust(maxNameLength) + ' '
            for i in range(self.alignlen - 1):
                if (i+1) % 10 == 0:
                    html += '0'
                else:
                    html += ' '
            html += '\n'
        for seq in self.seqs:
            html += seq.name.ljust(maxNameLength) + ' '
            for sym in seq:
                color = self.alphabet.getAnnotation('html-color', sym)
                if not color:
                    color = 'white'
                html += '<font style="BACKGROUND-COLOR: %s">%s</font>' % (color, sym)
            html += '\n'
        html += '</pre></body></html>'
        if filename:
            fh = open(filename, 'w')
            fh.write(html)
            fh.close()
        return html

def readClustal(string, alphabet):
    """ Read a ClustalW2 alignment in the given string and return as an
    Alignment object. """
    sequences = {} # sequence data
    for line in string.splitlines():
        if line.startswith('CLUSTAL') or line.startswith('STOCKHOLM') \
           or line.startswith('#'):
            continue
        if len(line.strip()) == 0:
            continue
        if line[0] == ' ' or '*' in line or ':' in line:
            continue
        sections = line.split()
        name, seqstr = sections[0:2]
        if sequences.has_key(name):
            sequences[name] += seqstr
        else:
            sequences[name] = seqstr
    sequences = []
    for name, seqstr in sequences.items():
        sequences.append(Sequence(seqstr, alphabet, name, gappy = True))
    return Alignment(sequences)

def readClustalFile(filename, alphabet):
    """ Read a ClustalW2 alignment file and return an Alignment object
    containing the alignment. """
    fh = open(filename)
    data = fh.read()
    fh.close()
    aln = readClustal(data, alphabet)
    return aln

# Substitution Matrix ------------------

class SubstMatrix():
    
    def __init__(self, alphabet, scoremat = {}):
        self.scoremat = scoremat
        self.alphabet = alphabet

    def _getkey(self, sym1, sym2):
        """ Construct canonical (unordered) key for two symbols """
        if sym1 <= sym2:
            return tuple([sym1, sym2])
        else:
            return tuple([sym2, sym1])
        
    def set(self, sym1, sym2, score):
        """ Add a score to the substitution matrix """
        self.scoremat[self._getkey(sym1, sym2)] = score
        
    def get(self, sym1, sym2):
        return self.scoremat[self._getkey(sym1, sym2)]
        
    def __str__(self):
        symbols = self.alphabet.symbols # what symbols are in the alphabet
        i = len(symbols)
        string = ''
        for a in symbols:
            string += a + ' '
            for b in symbols[:len(symbols)-i+1]:
                score = self.scoremat[self._getkey(a, b)]
                if score != None:
                    string += str(score).rjust(3) + ' '
                else:
                    string += "?".rjust(3) + ' '
            string += '\n'
            i -= 1
        string += '    ' + '   '.join(self.alphabet.symbols)
        return string

    def writeFile(self, filename):
        """ Write this substitution matrix to the given file. """
        fh = open(filename, 'w')
        file = ''
        for key in self.scoremat:
            file += ''.join(key) + ': ' + str(self.scoremat[key]) + '\n'
        fh.write(file)
        fh.close()


def readSubstMatrix(filename, alphabet):
    """ Read in the substitution matrix stored in the given file. """
    mat = SubstMatrix(alphabet)
    fh = open(filename, 'r')
    data = fh.read()
    fh.close()
    lines = data.splitlines()
    for line in lines:
        if len(line.strip()) == 0:
            continue
        symbols, score = line.split(':')
        score = int(score)
        mat.set(symbols[0], symbols[1], score)
    return mat

# Motifs -------------------

class Regexp(object):
    
    """ A class that defines a sequence pattern in terms of a
    given regular expression, with . indicating any symbol and square brackets
    indicating a selection. See standard regexp definitions for more. """
    
    def __init__(self, pattern):
        """ Create a new consensus sequence with the given pattern. """
        try:
            self.pattern = pattern
            self.regex = re.compile(pattern)
        except:
            raise RuntimeError('invalid consensus sequence given: %s' % pattern)
    
    def __str__(self):
        return self.pattern
    
    def search(self, sequence):
        """ Find matches to the motif in the specified sequence. Returns a list
        of triples, of the form (position, matched string, score). Note that
        the score is always 1.0 because a consensus sequence either matches
        or doesn't. """
        if not type(sequence) is Sequence:
            sequence = Sequence(sequence)
        sequenceString = sequence[:]
        
        results = []
        for match in self.regex.finditer(sequenceString):
            results.append((match.start(), match.group(), 1.0))
        return results

class PWM(object):
    
    """ A position weight matrix. """
    
    def __init__(self, foreground, background = None, start = 0, end = None):
        """ Create a new PWM from the given probability matrix/ces.
        foreground: can be either a list of Distrib's or an instance of IndepJoint.
        Specify only a section of the matrix to use with start and end. """
        if isinstance(foreground, IndepJoint):
            foreground = foreground.store
        self.start = start
        self.end = end or len(foreground)
        self.length = self.end - self.start
        self.alphabet = foreground[self.start].alpha
        if False in [ col.alpha == self.alphabet for col in foreground[self.start + 1 : self.end] ]:
            raise RuntimeError("All positions need to be based on the same alphabet")
        self.symbols = self.alphabet.symbols
        # Set foreground probabilities from given alignment
        self.m = numpy.zeros((len(self.symbols), self.length))
        self.fg = foreground[self.start:self.end]
        self.bg = background or Distrib(self.alphabet, 1.0) # specified background or uniform
        if not self.alphabet == self.bg.alpha:
            raise RuntimeError("Background needs to use the same alphabet as the foreground")
        p = self.bg.prob()
        for i in range(self.length):
            q = self.fg[i].prob()
            for j in range(len(self.alphabet)):
                self.m[j][i] = self.logme(q[j], p[j]) 
    
    def getRC(self, swap = [('A', 'T'), ('C', 'G')] ):
        """ Get the reverse complement of the current PWM.
            Use for DNA sequences with default params.
        """
        new_fg = self.fg[::-1]  # backwards
        for s in swap:
            new_fg = [d.swapxcopy(s[0], s[1]) for d in new_fg]
        return PWM(new_fg, self.bg)
        
    MIN_VALUE = 0.00000000001
    
    def logme(self, fg, bg):
        if fg > self.MIN_VALUE and bg > self.MIN_VALUE:
            ratio = fg / bg
            return math.log(ratio)
        # if not, one of fg and bg is practically zero
        if fg > self.MIN_VALUE: # bg is zero 
            return math.log(fg / self.MIN_VALUE)
        else: # fg is zero
            return math.log(self.MIN_VALUE)
        
    def getMatrix(self):
        return self.m
                
    def display(self, format = 'COLUMN'):
        if format == 'COLUMN':
            print " \t%s" % (' '.join(" %5d" % (i + 1) for i in range(self.length)))
            for j in range(len(self.alphabet)):
                print "%s\t%s" % (self.alphabet[j], ' '.join("%+6.2f" % (y) for y in self.m[j]))
        elif format == 'JASPAR':
            for j in range(len(self.alphabet)):
                print "%s\t[%s]" % (self.alphabet[j], ' '.join("%+6.2f" % (y) for y in self.m[j]))

    def search(self, sequence, lowerBound=0):
        """ Find matches to the motif in a specified sequence. Returns a list
        of  results as triples: (position, matched string, score). 
        The optional argument lowerBound specifies a lower bound on reported
        scores. """
        results = []
        for i in range(len(sequence)-self.length+1):
            subseq = sequence[i:i + self.length]
            ndxseq = [ self.alphabet.index(sym) for sym in subseq ]
            score = 0.0
            for w in range(len(ndxseq)):
                score += self.m[ ndxseq[w] ][ w ] 
            if score > lowerBound:
                results.append((i, subseq, score))
        return results

    def maxscore(self, sequence):
        """ Find matches to the motif in a specified sequence. 
            Returns the maximum score found in the sequence and its index as a tuple:
            (maxscore, maxindex) """
        maxscore = None
        maxindex = None
        for i in range(len(sequence)-self.length+1):
            subseq = sequence[i:i + self.length]
            ndxseq = [ self.alphabet.index(sym) for sym in subseq ]
            score = 0.0
            for w in range(len(ndxseq)):
                score += self.m[ ndxseq[w] ][ w ] 
            if maxscore == None:
                maxscore = score
                maxindex = i
            elif maxscore < score:
                maxscore = score
                maxindex = i
        return (maxscore, maxindex)

# Web Service Functions -------------------

def getSequence(id, database = 'uniprotkb', start=None, end=None):
    """ Get the sequence identified by the given ID from the given database
    (e.g. 'uniprotkb', 'refseqn' or 'refseqp'), and return it as a Sequence
    object. An error is caused if the sequence ID is not found. If start and
    end are given, then only that section of the sequence is returned. 
    Note: more flexible search options are supported by using webservice.fetch
    directly."""
    fastaData = fetch(id, database)
    try:
        seq = readFasta(fastaData)[0]
    except RuntimeError, IndexError:
        raise RuntimeError('An error occurred while retrieving the specified sequence: %s (maybe the ID doesn\'t exist)' % id)
    return Sequence(seq[start:end], seq.alphabet, seq.name, seq.info)

def searchSequences(query, database='uniprot'):
    """ Search for sequences matching the given query in the given database
    (must be 'uniprot'), and return a list of sequence IDs. """
    ids = search(query, limit = None)
    return ids

def runClustal(sequences, method='slow'):
    """ Run a ClustalW 2 alignment of the given list of Sequence objects.
    Return an Alignment object. Method should be one of 'fast' or 'slow'. """
    alpha = None
    for seq in sequences:
        if alpha == None:
            alpha = seq.alphabet
        elif alpha != seq.alphabet:
            raise RuntimeError("Invalid alphabet: " + str(seq.alphabet) + ". Not compatible with " + str(alpha))
    serviceName = 'clustalw2'
    resultType = 'aln-clustalw'
    fastaSeqs = ''.join([seq.writeFasta() for seq in sequences])
    params = {'alignment': method.lower(), 'sequence': fastaSeqs}
    service = EBI(serviceName)
    result = service.submit(params, resultType)
    alignment = readClustal(result, alpha)
    return alignment

def createTree(alignment, type):
    """ Run a ClustalW 2 phylogeny tree creation of either a 'Neighbour-joining'
    or 'UPGMA' type tree from the given multiple sequence Alignment object. """
    if not type in ['Neighbour-joining', 'UPGMA']:
        raise RuntimeError('type must be either \'Neighbour-joining\' or \'UPGMA\'.')
    serviceName = 'clustalw2_phylogeny'
    resultType = 'tree'
    output = 'dist'
    clustalAln = alignment.writeClustal()
    params = {'tree': output, 'sequence': clustalAln, 'clustering': type, 'tossgaps': 'true'}
    service = EBI(serviceName)
    tree = service.submit(params, resultType)
    return tree

def runBLAST(sequence, program='blastp', database='uniprotkb', exp='1e-1'):
    """ Run a BLAST search of nucleotide mouse databases using the given
    sequence as a query. Return a list of matched sequence IDs, in descending
    order of similarity to query sequence. 
    program: either blastn (nucleotide) or blastp (protein)
    database: many available, e.g. uniprotkb, pdb (protein); em_rel, nrnl1 (EMBL nucleotide, non-redundant resp)
        (for protein see http://www.ebi.ac.uk/Tools/sss/ncbiblast/help/index-protein.html#database)
        (for nucleotide see http://www.ebi.ac.uk/Tools/sss/ncbiblast/help/index-nucleotide.html#database)
    exp: E-value threshold (select only hits that have a better E-value than this)
    """
    if sequence.alphabet == predefAlphabets['DNA']:
        stype = 'dna'
    elif sequence.alphabet == predefAlphabets['RNA']:
        stype = 'rna'
    else:
        stype = 'protein'
    serviceName = 'ncbiblast'
    resultTypes = ['ids', 'out'] # request 
    fastaSeq = sequence.writeFasta()
    databases = [database]
    params = {'program': program, 'database': databases, 'sequence': fastaSeq,
              'stype': stype, 'exp': exp}
    service = EBI(serviceName)
    idsData, output = service.submit(params, resultTypes)
    ids=[]
    for id in idsData.splitlines():
        if len(id) > 0:
            ids.append(id.split(':')[1])
    return ids
