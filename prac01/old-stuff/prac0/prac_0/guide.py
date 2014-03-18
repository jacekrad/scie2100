###################################################
# This module is a supplement to the Python guide #
# Version 1.02  (18/2/2013)                        #
###################################################
''' 
This module contains code for that can help solving bioinformatics problems.
See the accompanying Python guide for more explanations and examples. 

Alphabet is a class that defines valid symbols that we then use to make up valid 
biological sequences. Note that we also define variables corresponding to 
DNA, RNA and Protein sequences that can be used directly.

Sequence defines basic parts and operations on biological sequences. 

Alignment defines an alignment of sequences (how symbols in different sequences line 
up when placed on-top). Alignment methods should generate instances of this class.

SubstMatrix defines a substitution matrix, i.e. a scoring system for performing 
alignments. You can read these from files or construct them manually.

GeneProfile defines parts and operations for gene expression profiles. Essentially, 
the class will help to index expression data by gene name (rows) and by sample name (columns).

There are several methods not tied to a particular class because they construct new instances, 
e.g. reading from file, retrieving from the internet, creating an alignment from sequences etc.

You need to have numpy installed (see http://www.numpy.org/). 
Should work with Python v2.6-2.7 (see http://www.python.org/). 
Has not been written to work with Python v3 and later--but this should be easy to do.
The code may contain bugs--please report to m.boden@uq.edu.au
'''

import math, numpy, urllib, urllib2


class Alphabet():
    """ A minimal class for alphabets """
    def __init__(self, symbolString):
        self.symbols = symbolString
    def __len__(self):              # implements the "len" operator, e.g. "len(Alphabet('XYZ')" results in 3
        return len(self.symbols)
    def __contains__(self, sym):    # implements the "in" operator, e.g. "'A' in Alphabet('ACGT')" results in True 
        return sym in self.symbols
    def __iter__(self):             # method that allows us to iterate over all symbols, e.g. "for sym in Alphabet('ACGT'): print sym" prints A, C, G and T on separate lines
        tsyms = tuple(self.symbols)
        return tsyms.__iter__()
""" Below we declare alphabet variables that are going to be available when 
this module is imported """ 
DNA_Alphabet = Alphabet('ACGT')
RNA_Alphabet = Alphabet('ACGU')
Protein_Alphabet = Alphabet('ACDEFGHIKLMNPQRSTVWY')
Protein_wX = Alphabet('ACDEFGHIKLMNPQRSTVWYX')
Hydrophobic_Alphabet=Alphabet('VILMCWFAYHTSPG') 

class Sequence():
    """ A biological sequence class. Stores the sequence itself, 
        the alphabet and a name. 
        Usage:
        >>> seq1 = Sequence('ACGGGAGAGG', DNA_Alphabet, 'ABC')
        >>> print seq1
        ABC: ACGGGAGAGG
        >>> 'C' in seq1
        True
        >>> for sym in seq1:
        ...     print sym
        """
    def __init__(self, sequence, alphabet, name = '', gappy = False):
        """ Construct a sequence from a string, an alphabet (gappy or not) and a name.
            The parameter gappy is for sequences when used in alignments. """
        for sym in sequence:
            if not sym in alphabet and (sym != '-' or not gappy):  # error check: bail out
                raise RuntimeError('Invalid symbol: ' + sym)
        self.sequence = sequence
        self.alphabet = alphabet
        self.name = name
        self.gappy = gappy
    def __len__(self):      # the "len" operator
        return len(self.sequence)
    def __iter__(self):     # method that allows us to iterate over a sequence
        tsyms = tuple(self.sequence)
        return tsyms.__iter__()
    def __contains__(self, item):   # test for membership (the "in" operator)
        for sym in self.sequence:
            if sym == item:
                return True
        return False
    def __getitem__(self, ndx):     # [ndx] operator (retrieve a specified index (or a "slice" of indices) of the sequence data.
        return self.sequence[ndx]
    def writeFasta(self):
        """ Write one sequence in FASTA format to a string and return it. """
        fasta = '>' + self.name + '\n'
        data = self.sequence
        nlines = (len(self.sequence) - 1) / 60 + 1
        for i in range(nlines):
            lineofseq = ''.join(data[i*60 : (i+1)*60]) + '\n'
            fasta += lineofseq
        return fasta
    def __str__(self):      # "pretty" print sequence
        str = self.name + ': '
        for sym in self:
            str += sym
        return str
    def count(self, findme):
        """ Get the number of occurrences of specified symbol """
        cnt = 0
        for sym in self.sequence:
            if findme == sym:
                cnt = cnt + 1
        return cnt
    def find(self, findme):
        """ Find the position of the specified symbol or sub-sequence """
        return self.sequence.find(findme)

class Alignment():
    """ A sequence alignment class. Stores two or more sequences of equal length where
    one symbol is gap '-'. The number of columns in the alignment is given by alignlen. 
    Example usage:
    >>> seqs = [Sequence('THIS-LI-NE', Protein_Alphabet, gappy = True), Sequence('--ISALIGNED', Protein_Alphabet, gappy = True)]
    >>> print Alignment(seqs)
     THIS-LI-NE-
     --ISALIGNED """
    def __init__(self, seqs):
        self.alignlen = -1
        self.seqs = seqs
        for s in seqs:
            if self.alignlen == -1:
                self.alignlen = len(s)
            elif self.alignlen != len(s):
                raise RuntimeError("Alignment invalid")
    def __str__(self):    
        string = ''
        namelen = 0
        for seq in self.seqs:
            namelen = max(len(seq.name), namelen)
        for seq in self.seqs:
            string += seq.name.ljust(namelen+1)
            for sym in seq:
                string += sym
            string += '\n'
        return string


def scoreAlignment(aln, substmat = None, gap = -1):
    """Score an alignment (aln) using a substitution matrix (substmat).
       If the alignment consists of more than two sequences, the minimum
       score of each column is used.
       If substmat is not specified (None), the count of matches is returned.
    """
    nseqs = len(aln.seqs)
    total = 0
    for pos in range(aln.alignlen):
        min = None
        for i in range(nseqs):
            for j in range(i+1, nseqs):
                gap_here = aln.seqs[i][pos] == '-' or aln.seqs[j][pos] == '-'
                score = 0
                if substmat == None:
                    if aln.seqs[i][pos] == aln.seqs[j][pos]:
                        score = 1
                else: # we have a substitution matrix 
                    if gap_here:
                        score = gap
                    else:
                        score = substmat.get(aln.seqs[i][pos], aln.seqs[j][pos])
                if min == None:
                    min = score
                elif min > score:
                    min = score
        total += min
    return total

class SubstMatrix():
    """ Create a substitution matrix for an alphabet.
    Example usage:
    >>> sm = SubstMatrix(DNA_Alphabet)
    >>> for a in DNA_Alphabet:
    ...     for b in DNA_Alphabet:
    ...         if a > b:
    ...             sm.set(a, b, -1)
    ...         elif a == b:
    ...             sm.set(a, b, +1)
    ...
    >>> print sm
    A   1 
    C  -1   1 
    G  -1  -1   1 
    T  -1  -1  -1   1 
        A   C   G   T
    >>> sm.get('C', 'T')
    -1
    """
    def __init__(self, alphabet, scoremat = None):
        self.scoremat = scoremat or {}      # start with empty dictionary
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

"""
Below are some useful methods for loading data from strings and files.
Recognize the FASTA and Clustal formats (nothing fancy). 
"""
def readFastaString(string, alphabet):
    """ Read the given string as FASTA formatted data and return the list of
    sequences contained within it. """
    seqlist = []    # list of sequences contained in the string 
    seqname = None  # name of *current* sequence 
    seqdata = []    # sequence data for *current* sequence
    for line in string.splitlines():    # read every line
        if len(line) == 0:              # ignore empty lines
            continue
        if line[0] == '>':  # start of new sequence            
            if seqname:     # check if we've got one current
                current = Sequence(''.join(seqdata), alphabet, seqname)
                seqlist.append(current)
            # now collect data about the new sequence
            seqname = line[1:].split()[0] # skip first char
            seqdata = []
        else:               # we assume this is (more) data for current
            cleanline = line.split()
            for thisline in cleanline:
                seqdata.extend(tuple(thisline.strip('*')))
    # we're done reading the file, but the last sequence remains
    if seqname:
        lastseq = Sequence(''.join(seqdata), alphabet, seqname)
        seqlist.append(lastseq)
    return seqlist

def readFastaFile(filename, alphabet):
    """ Read the given FASTA formatted file and return the list of sequences 
    contained within it. """
    fh = open(filename)
    data = fh.read()
    fh.close()
    seqlist = readFastaString(data, alphabet)
    return seqlist

def writeFastaFile(filename, seqs):
    """ Write the specified sequences to a FASTA file. """
    fh = open(filename, 'w')
    for seq in seqs:
        fh.write(str(seq))
    fh.close()
    
def readClustalString(string, alphabet):
    """ Read a ClustalW2 alignment in the given string and return as an
    Alignment object. """
    seqs = {} # sequence data
    for line in string.splitlines():
        if line.startswith('CLUSTAL') or line.startswith('STOCKHOLM') \
           or line.startswith('#'):
            continue
        if len(line.strip()) == 0:
            continue
        if line[0] == ' ' or '*' in line or ':' in line:
            continue
        sections = line.split()
        name, seq = sections[0:2]
        if seqs.has_key(name):
            seqs[name] += seq
        else:
            seqs[name] = seq
    sequences = []
    for name, seq in seqs.items():
        sequences.append(Sequence(seq, alphabet, name, gappy = True))
    return Alignment(sequences)

def readClustalFile(filename, alphabet):
    """ Read a ClustalW2 alignment file and return an Alignment object
    containing the alignment. """
    fh = open(filename)
    data = fh.read()
    fh.close()
    aln = readClustalString(data, alphabet)
    return aln

class GeneProfile():
    """ A class for gene expression data.
    Example usage:
    >>> gp = GeneProfile('MyMicroarray', ['Exp1', 'Exp2'])
    >>> gp['gene1'] = [0.1, 0.5]
    >>> gp['gene2'] = [2, 1]
    >>> gp.getSample('Exp2')
    {'gene1': [0.5], 'gene2': [1.0]}
    """
    def __init__(self, dataset_name='', sample_names=[], profiles = None):
        """ Create a gene profile set. """
        self.name = dataset_name
        self.samples = sample_names
        self.genes = profiles or {} # dictionary for storing all gene--measurement pairs
    def __setitem__(self, name, probevalues):
        if len(probevalues) == len(self.samples):
            self.genes[name] = [float(y) for y in probevalues]
        else:
            raise RuntimeError('Invalid number of measurements for probe ' + name)
    def __getitem__(self, name):
        return self.genes[name]
    def getSorted(self, index, descending=True):
        """Get a list of (gene, value) tuples in descending order by value"""
        key_fn = lambda v: v[1][index]
        return sorted(self.genes.items(), key=key_fn, reverse=descending)
    def addSample(self, sample_name, sample_dict):
        """Add a sample to the current data set.
           sample_dict is a dictionary with the same keys as the current gene set.
           Only values for genes in the current set will be added. """
        self.headers.extend(sample_name)
        if not self.genes:
            self.genes = sample_dict
        else:
            for gene in self.genes:
                values = sample_dict[gene]
                if values:
                    self.genes[gene].extend([float(y) for y in values])
                else:
                    self.genes[gene].extend([0.0 for _ in sample_name])
        return self.genes
    def getSample(self, sample_name):
        """Construct a gene dictionary including only named samples. """
        mygenes = {}
        if isinstance(sample_name, str):    # a single sample-name
            mysamples = [sample_name]
        else:                               # a list of sample-names
            mysamples = sample_name         
        for gene in self.genes:
            mygenes[gene] = []
            for name in mysamples:
                mygenes[gene].append(self.genes[gene][self.samples.index(name)])
        return mygenes
    def getRatio(self, sample1, sample2):
        """Get the ratio of two samples in the data set. """
        mygenes = {}
        index1 = self.samples.index(sample1)
        index2 = self.samples.index(sample2)
        for gene in self.genes:
            mygenes[gene] = []
            mygenes[gene].append(self.genes[gene][index1] / self.genes[gene][index2])
        return mygenes
    def __str__(self):
        """ Display data as a truncated GEO SOFT file named filename. """
        line = '^DATASET = ' + self.dataset + '\n'
        line += '!dataset_table_begin\nID_REF\t'
        for header in self.headers:
            line += header + '\t'
        line += '\n'
        for gene in self.genes:
            line += gene + '\t'
            values = self.genes[gene]
            for value in values:
                line += format(value, '5.3f') + '\t'
            line += '\n'
        line += '!dataset_table_end\n'
    def writeGeoFile(self, filename):
        fh = open(filename, 'w')
        fh.write(str(self))
        fh.close()

def getLog(genedict, base=2):
    """Get the log-transformed value of a sample/column. """
    mygenes = {}
    for gene in genedict:
        mygenes[gene] = []
        for sample in genedict[gene]:
            mygenes[gene].append(math.log(sample, base))
    return mygenes

def readGeoFile(filename, id_column = 0):
    """ Read a Gene Expression Omnibus SOFT file. """
    dataset = None
    fh = open(filename, "rU")
    manylines = fh.read()
    fh.close()
    data_rows = False  # Indicates whether we're reading the data section or metadata
    name = 'Unknown'
    cnt_data = 0
    for line in manylines.splitlines():
        if line.startswith('^DATASET'):
            name = line.split('= ')[1]
            continue
        data_rows = line.startswith('!dataset_table_begin')
        data_rows = not line.startswith('!dataset_table_end')
        if len(line.strip()) == 0 or line.startswith('!') or line.startswith('#') or line.startswith('^'):
            continue
        if data_rows:
            cnt_data += 1
            if (cnt_data == 1):  # First line contains the headers
                headers = line.split('\t')
                dataset = GeneProfile(name, headers[2:])  # Create the data set
                continue
            ignore = (dataset == None)  # ignore the row if the dataset is not initialised
            id = line.split('\t')[id_column]
            values = []
            cnt_word = 0
            for word in line.split('\t'):
                cnt_word += 1
                if cnt_word <= (id_column + 1): # ignore the gene names
                    continue
                if word == 'null':
                    ignore = True # ignore gene if a value is null
                    continue
                try:
                    values.append(float(word))
                except:  # ignore values that are not "float"
                    continue
            if not ignore:
                dataset[id] = tuple(values)
    print 'Data set %s contains %d genes' % (name, len(dataset.genes))
    return dataset

"""
Web service methods that find data in online databases. 
Our implementations are mainly serviced by EBI.
"""
def getSequence(entryId, dbName, alphabet):
    """ Retrieve a single entry from a database
    entryId: ID for entry e.g. 'P63166' or 'SUMO1_MOUSE'
    dbName: name of db e.g. 'uniprotkb', 'pdb' or 'refseqn'.
    See: http://www.uniprot.org/faq/28. """
    url = 'http://www.ebi.ac.uk/Tools/dbfetch/dbfetch?style=raw&db=' +\
    dbName + '&format=fasta&id=' + entryId
    try:
        data = urllib2.urlopen(url).read()
        return readFastaString(data, alphabet)[0]
    except urllib2.HTTPError, ex:
        raise RuntimeError(ex.read())

def searchSequences(query, dbName):
    """
    Retrieve multiple entries matching query from a database currently only via UniProtKB
    query: search term(s) e.g. 'organism:9606+AND+antigen'
    dbName: name of database e.g. 'uniprot', "refseq:protein", "refseq:pubmed"
    See http://www.uniprot.org/faq/28 for more info re UniprotKB's URL syntax
    See http://www.ncbi.nlm.nih.gov/books/NBK25499/ for more on NCBI's E-utils
    """
    if dbName.startswith('uniprot'):
        # Construct URL
        url = 'http://www.uniprot.org/' + dbName + '/?format=list&query=' + query
        # Get the entries
        try:
            data = urllib2.urlopen(url).read()
            return data.splitlines()
        except urllib2.HTTPError, ex:
            raise RuntimeError(ex.read())
    elif dbName.startswith('refseq'):
        dbs = dbName.split(":")
        if len(dbs) > 1:
            dbName = dbs[1]
        base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        url = base + "esearch.fcgi?db=" + dbName + "&term=" + query
        # Get the entries
        try:
            data = urllib2.urlopen(url).read()
            words = data.split("</Id>")
            words = [w[w.find("<Id>")+4:] for w in words[:-1]]
            return words
        except urllib2.HTTPError, ex:
            raise RuntimeError(ex.read())
    return

def idmap(identifiers, frm='ACC', to='P_REFSEQ_AC'):
    """
    Map identifiers between databases (based on UniProtKB; 
    see http://www.uniprot.org/faq/28)
    identifiers: a list of identifiers (list of strings)
    frm: the abbreviation for the identifier FROM which to idmap
    to: the abbreviation for the identifier TO which to idmap
    Returns a dictionary with key (from) -> value (to) """
    url = 'http://www.uniprot.org/mapping/'
    # construct query by concatenating the list of identifiers
    if isinstance(identifiers, str):
        query = identifiers.strip()
    else: # assume it is a list of strings
        query = ''
        for id in identifiers:
            query = query + id.strip() + ' '
        query = query.strip() # remove trailing spaces
    params = {
        'from' : frm,
        'to' : to,
        'format' : 'tab',
        'query' : query
    }
    if len(query) > 0:
        request = urllib2.Request(url, urllib.urlencode(params))
        response = urllib2.urlopen(request).read()
        d = dict()
        for row in response.splitlines()[1:]:
            pair = row.split('\t')
            d[pair[0]] = pair[1]
        return d
    else:
        return dict()

"""
Gene Ontology services.
See http://www.ebi.ac.uk/QuickGO/WebServices.html for more info
"""
def getGODef(goterm):
    """
    Retrieve information about a GO term
    goterm: the identifier, e.g. 'GO:0002080'
    """
    # Construct URL
    url = 'http://www.ebi.ac.uk/QuickGO/GTerm?format=obo&id=' + goterm
    # Get the entry: fill in the fields specified below
    try:
        entry={'id': None, 'name': None, 'def': None}
        data = urllib2.urlopen(url).read()
        for row in data.splitlines():
            index = row.find(':')
            if index > 0 and len(row[index:]) > 1:
                field = row[0:index].strip()
                value = row[index+1:].strip(' "') # remove spaces
                if field in entry.keys():         # check if we need field
                    if entry[field] == None:      # check if assigned
                        entry[field] = value
        return entry
    except urllib2.HTTPError, ex:
        raise RuntimeError(ex.read())

def getGOTerms(genes, db='UniProtKB'):
    """
    Retrieve all GO terms for a given set of genes (or single gene).
    db: use specified database, e.g. 'UniProtKB', 'UniGene', 
    or 'Ensembl'.
    The result is given as a map (key=gene name, value=list of unique 
    terms) OR in the case of a single gene as a list of unique terms.
    """
    if type(genes) != list and type(genes) != set and type(genes) != tuple:   
        genes = [genes]  # if 'genes' is a single gene, we make a single item list
    map = dict()
    uri = 'http://www.ebi.ac.uk/QuickGO/GAnnotation?format=tsv&db='+db+'&protein='
    for gene in genes:
        terms = set()  # empty result set
        url = uri + gene.strip() # Construct URL
        try: # Get the entry: fill in the fields specified below
            data = urllib2.urlopen(url).read()
            for row in data.splitlines()[1:]:  # we ignore header row
                values = row.split('\t')
                if len(values) >= 7:
                    terms.add(values[6]) # add term to result set
            map[gene] = list(terms)      # make a list of the set
        except urllib2.HTTPError, ex:
            raise RuntimeError(ex.read())
    if len(genes) == 1:
        return map[genes[0]]
    else:
        return map

def getGenes(goterms, db='UniProtKB', taxo=None):
    """
    Retrieve all genes/proteins for a given set of GO terms 
    (or single GO term).
    db: use specified database, e.g. 'UniProtKB', 'UniGene', 
    or 'Ensembl'
    taxo: use specific taxonomic identifier, e.g. 9606 (human)
    The result is given as a map (key=gene name, value=list of unique 
    terms) OR in the case of a single gene as a list of unique terms.
    """
    if type(goterms) != list and type(goterms) != set and type(goterms) != tuple:
        goterms = [goterms]
    map = dict()
    if taxo == None:
        uri = 'http://www.ebi.ac.uk/QuickGO/GAnnotation?format=tsv&db='+db+'&term='
    else:
        uri = 'http://www.ebi.ac.uk/QuickGO/GAnnotation?format=tsv&db='+db+'&tax='+\
        str(taxo)+'&term='
    for goterm in goterms:
        genes = set()   # start with empty result set
        url = uri + goterm.strip() # Construct URL
        try: # Get the entry: fill in the fields specified below
            data = urllib2.urlopen(url).read()
            for row in data.splitlines()[1:]:  # we ignore first (header) row
                values = row.split('\t')
                if len(values) >= 7:
                    genes.add(values[1])  # add gene name to result set
            map[goterm] = list(genes)
        except urllib2.HTTPError, ex:
            raise RuntimeError(ex.read())
    if len(goterms) == 1:
        return map[goterms[0]]
    else:
        return map
    
