import urllib, urllib2
import os
from time import sleep
import stats
from StringIO import StringIO
import gzip

""" This module is collection of functions for accessing the EBI REST web services,
    including sequence retrieval, searching, gene ontology, BLAST and ClustalW.
    The class EBI takes precautions taken as to not send too many requests when
    performing BLAST and ClustalW queries. 
    
    See 
    http://www.ebi.ac.uk/Tools/webservices/tutorials/01_intro and
    http://www.ebi.ac.uk/Tools/webservices/tutorials/02_rest
    http://www.ebi.ac.uk/Tools/webservices/tutorials/06_programming/python/rest/urllib
    """

__ebiUrl__ =        'http://www.ebi.ac.uk/Tools/'               # Use UQ mirror when available
__ebiGOUrl__ =      'http://www.ebi.ac.uk/QuickGO/'             # Use UQ mirror when available
__uniprotUrl__ =    'http://www.uniprot.org/'                   # 

def fetch(entryId, dbName='uniprotkb', format='fasta'):
    """
    Retrieve a single entry from a database
    entryId: ID for entry e.g. 'P63166' or 'SUMO1_MOUSE' (database dependent; examples for uniprotkb)
    dbName: name of database e.g. 'uniprotkb' or 'pdb' or 'refseqn'; see http://www.ebi.ac.uk/Tools/dbfetch/dbfetch/dbfetch.databases for available databases
    format: file format specific to database e.g. 'fasta' or 'uniprot' for uniprotkb (see http://www.ebi.ac.uk/Tools/dbfetch/dbfetch/dbfetch.databases)
    See http://www.ebi.ac.uk/Tools/dbfetch/syntax.jsp for more info re URL syntax
    """
     # Construct URL
    url = __ebiUrl__ + 'dbfetch/dbfetch?style=raw&db=' + dbName + '&format=' + format + '&id=' + entryId
    # Get the entry
    try:
        data = urllib2.urlopen(url).read()
        if data.startswith('ERROR'):
            raise RuntimeError(data)
        return data
    except urllib2.HTTPError, ex:
        raise RuntimeError(ex.read())

def search(query, dbName='uniprot', format='list', limit=100):
    """
    Retrieve multiple entries matching query from a database currently only via UniProtKB
    query: search term(s) e.g. 'organism:9606+AND+antigen'
    dbName: name of database e.g. 'uniprot', "refseq:protein", "refseq:pubmed"
    format: file format e.g. 'list', 'fasta' or 'txt'
    limit: max number of results (specify None for all results)
    See http://www.uniprot.org/faq/28 for more info re UniprotKB's URL syntax
    See http://www.ncbi.nlm.nih.gov/books/NBK25499/ for more on NCBI's E-utils
    """
    if dbName.startswith('uniprot'):
        # Construct URL
        if limit == None: # no limit to number of results returned
            url = __uniprotUrl__ + dbName + '/?format=' + format + '&query=' + query
        else:
            url = __uniprotUrl__ + dbName + '/?format=' + format + '&limit=' + str(limit) + '&query=' + query
        # Get the entries
        try:
            data = urllib2.urlopen(url).read()
            if format == 'list':
                return data.splitlines()
            else:
                return data
        except urllib2.HTTPError, ex:
            raise RuntimeError(ex.read())
    elif dbName.startswith('refseq'):
        dbs = dbName.split(":")
        if len(dbs) > 1:
            dbName = dbs[1]
        base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        url = base + "esearch.fcgi?db=" + dbName + "&term=" + query + "&retmax=" + str(limit)
        # Get the entries
        try:
            data = urllib2.urlopen(url).read()
            words = data.split("</Id>")
            words = [w[w.find("<Id>")+4:] for w in words[:-1]]
            if format == 'list':
                return words
            elif format == 'fasta' and len(words) > 0:
                url = base + "efetch.fcgi?db=" + dbName + "&rettype=fasta&id="
                for w in words:
                    url += w + ","
                data = urllib2.urlopen(url).read()
                return data
            else:
                return ''
        except urllib2.HTTPError, ex:
            raise RuntimeError(ex.read())
    return

authorised_database_tag = {9606:  ['Homo sapiens', 'ACC', 'ID'],
                           3702:  ['Arabidopsis thaliana', 'TAIR_ID'],
                           4932:  ['Saccharomyces cerevisiae', 'SGD_ID', 'CYGD_ID'],
                           10090: ['Mus musculus', 'MGI_ID']}
      
def idmap(identifiers, frm='ACC', to='P_REFSEQ_AC', format='tab', reverse=False):
    """
    Map identifiers between databases (based on UniProtKB; see http://www.uniprot.org/faq/28)
    identifiers: a list of identifiers (list of strings)
    frm: the tag/abbreviation for the identifier FROM which to idmap
    to: the tag/abbreviation for the identifier TO which to idmap
    format: the results format to use 
    reverse: reverse the returned mapping key (to) -> value (from)
    Returns a dictionary with key (from) -> value (to)
    Set reverse to True if dictionary should contain the reverse mapping, useful if the mapping is non-unique
    """
    url = __uniprotUrl__ + 'mapping/'
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
        'format' : format,
        'query' : query
    }
    if len(query) > 0:
        request = urllib2.Request(url, urllib.urlencode(params))
        response = urllib2.urlopen(request).read()
        d = dict()
        for row in response.splitlines()[1:]:
            pair = row.split('\t')
            if not reverse:
                d[pair[0]] = pair[1]
            else:
                d[pair[1]] = pair[0]
        return d
    else:
        return dict()
    
"""
Gene Ontology service (QuickGO)
http://www.ebi.ac.uk/QuickGO/WebServices.html
Note that this service can be slow for queries involving a large number of entries.
"""

def getGOReport(positives, background = None, database = 'UniProtKB'):
    """ Generate a complete GO term report for a set of genes (positives).
        Each GO term is also assigned an enrichment p-value (on basis of background, if provided).
        Returns a list of tuples (GO_Term_ID[str], Foreground_no[int], Term_description[str]) with no background, OR
        (GO_Term_ID[str], E-value[float], Foreground_no[int], Background_no[int], Term_description[str]). 
        E-value is a Bonferroni-corrected p-value.
        """
    pos = set(positives)
    fg_map = getGOTerms(pos, database)
    fg_list = []
    for id in fg_map:
        for t in fg_map[id]:
            fg_list.append(t)
    bg_map = {}
    bg_list = []
    neg = set()
    if background != None:
        neg = set(background).difference(pos)
        bg_map = getGOTerms(neg, database)
        for id in bg_map:
            for t in bg_map[id]:
                bg_list.append(t)
    term_set = set(fg_list)
    term_cnt = {}

    nPos = len(pos)
    nNeg = len(neg)
    if background == None:
        for t in term_set:
            term_cnt[t] = fg_list.count(t)
        sorted_cnt = sorted(term_cnt.items(), key=lambda v: v[1], reverse=True)
    else: # a background is provided
        for t in term_set:
            fg_hit = fg_list.count(t)
            bg_hit = bg_list.count(t)
            fg_nohit = nPos - fg_hit
            bg_nohit = nNeg - bg_hit
            term_cnt[t] = (fg_hit, fg_hit + bg_hit, stats.getFETpval(fg_hit, bg_hit, fg_nohit, bg_nohit, False))
        sorted_cnt = sorted(term_cnt.items(), key=lambda v: v[1][2], reverse=False)

    ret = []
    for t in sorted_cnt:
        defin = getGODef(t[0])
        if background != None:
            ret.append((t[0], t[1][2] * len(term_set), t[1][0], t[1][0]+t[1][1], defin['name']))
        else:
            ret.append((t[0], t[1], defin['name']))
    return ret
    
def getGODef(goterm):
    """
    Retrieve information about a GO term
    goterm: the identifier, e.g. 'GO:0002080'
    """
     # Construct URL
    url = __ebiGOUrl__ + 'GTerm?format=obo&id=' + goterm
    # Get the entry: fill in the fields specified below
    try:
        entry={'id': None, 'name': None, 'def': None}
        data = urllib2.urlopen(url).read()
        for row in data.splitlines():
            index = row.find(':')
            if index > 0 and len(row[index:]) > 1:
                field = row[0:index].strip()
                value = row[index+1:].strip(' "') # remove spaces and quotation marks
                if field in entry.keys():         # check if we need this field
                    if entry[field] == None:      # check if not yet assigned
                        entry[field] = value
        return entry
    except urllib2.HTTPError, ex:
        raise RuntimeError(ex.read())

def getGOTerms(genes, database='UniProtKB', completeAnnot = False):
    """
    Retrieve all GO terms for a given set of genes (or single gene).
    database: use specified database, e.g. 'UniProtKB', 'UniGene', or 'Ensembl'
    The result is given as a map (key=gene name, value=list of unique terms) OR
    in the case of a single gene as a list of unique terms.
    If completeAnnot is True (default is False) then the above "terms" is the first element 
    in a tuple with (gene-terms-map, gene-taxon-id).
    """
    if type(genes) != list and type(genes) != set and type(genes) != tuple:
        genes = [genes]
    termsmap = dict()
    taxonmap = dict()
    uri_string = 'GAnnotation?format=tsv&gz&db=' + database + '&protein='
    # build queries (batches of genes)
    queryLength = 2000
    queries = []
    query = None
    for gene in genes:
        if query == None:
            query = gene
        elif len(query) < queryLength:
            query += ','+gene
        else:
            queries.append(query)
            query = gene
    if query != None:
        queries.append(query)
    # execute queries, each involving a number of genes
    for query in queries:
        # Construct URL
        url = __ebiGOUrl__ + uri_string + query
        # Get the entry: fill in the fields specified below
        try:
            urlreq = urllib2.Request(url)
            urlreq.add_header('Accept-encoding', 'gzip')
            response = urllib2.urlopen(urlreq)
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                data = f.read()
            else:
                data = response.read()
            for row in data.splitlines()[1:]:  # we ignore first (header) row
                values = row.split('\t')
                if len(values) >= 7:
                    key = values[1]
                    if termsmap.has_key(key):
                        termsmap[key].add(values[6])
                    else:
                        termsmap[key] = set([values[6]])
                        taxonmap[key] = int(values[4])
        except urllib2.HTTPError, ex:
            raise RuntimeError(ex.read())
    if completeAnnot:
        if len(genes) == 1:
            if len(termsmap) == 1: 
                return (termsmap[genes[0]], taxonmap[genes[0]])
            else:
                return (set(), None) 
        else:
            return (termsmap, taxonmap)
    else:
        if len(genes) == 1:
            if len(termsmap) == 1: 
                return termsmap[genes[0]]
            else:
                return set()
        else:
            return termsmap

def getGenes(goterms, database='UniProtKB', taxo=None):
    """
    Retrieve all genes/proteins for a given set of GO terms (or single GO term).
    database: use specified database, e.g. 'UniProtKB', 'UniGene', or 'Ensembl'
    taxo: use specific taxonomic identifier, e.g. 9606 (human)
    The result is given as a map (key=gene name, value=list of unique terms) OR
    in the case of a single gene as a list of unique terms.
    """
    if type(goterms) != list and type(goterms) != set and type(goterms) != tuple:
        goterms = [goterms]
    map = dict()
    if taxo == None:
        uri_string = 'GAnnotation?format=tsv&db=' + database + '&term='
    else:
        uri_string = 'GAnnotation?format=tsv&db=' + database + '&tax=' + str(taxo) + '&term='
    for goterm in goterms:
        genes = set()
        # Construct URL
        url = __ebiGOUrl__ + uri_string + goterm.strip()
        # Get the entry: fill in the fields specified below
        try:
            data = urllib2.urlopen(url).read()
            for row in data.splitlines()[1:]:  # we ignore first (header) row
                values = row.split('\t')
                if len(values) >= 7:
                    genes.add(values[1])
            map[goterm] = list(genes)
        except urllib2.HTTPError, ex:
            raise RuntimeError(ex.read())
    if len(goterms) == 1:
        return map[goterms[0]]
    else:
        return map


class EBI(object):
    
    __email__ =         'anon@uq.edu.au'                            # to whom emails about jobs should go
    __ebiServiceUrl__ = 'http://www.ebi.ac.uk/Tools/services/rest/' # Use UQ mirror when available
    __checkInterval__ = 2                                           # how long to wait between checking job status

    def __init__(self, service=None):
        """ Initialise service session. 
        service: presently, ncbiblast and clustalw2 are supported. Use None (default) for fetch/idmap jobs.
        """
        self.service = service
        self.lockFile = '%s.lock' % service
    
    def createLock(self):
        """ Create a lock file to prevent submission of more than 1 job
        at a time by a single user. """
        fh = open(self.lockFile, 'w')
        fh.write(self.jobId)
        fh.close()
    
    def removeLock(self):
        """ Remove the lock file. """
        os.remove(self.lockFile)
    
    def isLocked(self):
        """ Check if there is a lock on this service. If there is, check if
        the job is complete, and if so remove the lock. Return True if still
        locked and False if not. """
        if os.path.exists(self.lockFile):
            fh = open(self.lockFile, 'r')
            jobId = fh.read()
            fh.close()
            status = self.status(jobId)
            if status == 'RUNNING':
                self.jobId = jobId
                return True
            else:
                self.removeLock()
                return False
        else:
            return False
    
    """
    BLAST and CLUSTALW services
    """
    
    def run(self, params):
        """ Submit a job to the given service with the given parameters, given
        as a dictionary. Return the jobId. """
        if self.service == None:
            raise RuntimeError('No service specified')
        if self.isLocked():
            raise RuntimeError("""You currently have a %s job running. You must
                                  wait until it is complete before submitting another job. Go to 
                                  %sstatus/%s to check the status of the job.""" % (self.service, self.__ebiServiceUrl__, self.jobId))
        url = self.__ebiServiceUrl__ + self.service + '/run/'
        # ncbiblast database parameter needs special handling
        if self.service == 'ncbiblast':
            databaseList = params['database']
            del params['database']
            databaseData = ''
            for db in databaseList:
                databaseData += '&database=' + db
            encodedParams = urllib.urlencode(params)
            encodedParams += databaseData
        else:
            encodedParams = urllib.urlencode(params)
        print url
        self.jobId = urllib2.urlopen(url, encodedParams).read()
        self.createLock()
        return self.jobId
    
    def status(self, jobId=None):
        """ Check the status of the given job (or the current job if none is
        specified), and return the result. """
        if jobId is None:
            jobId = self.jobId
        url = self.__ebiServiceUrl__ + self.service + '/status/%s' % jobId
        status = urllib2.urlopen(url).read()
        return status
    
    def resultTypes(self):
        """ Get the available result types. Will only work on a finished job. """
        url = self.__ebiServiceUrl__ + self.service + '/resulttypes/%s' % self.jobId
        resultTypes = urllib2.urlopen(url).read()
        return resultTypes
    
    def result(self, resultType):
        """ Get the result of the given job of the specified type. """
        url = self.__ebiServiceUrl__ + self.service + '/result/%s/%s' % (self.jobId, resultType)
        try:
            result = urllib2.urlopen(url).read()
            if resultType == 'error':
                raise RuntimeError('An error occurred: %s' % result)
        except urllib2.HTTPError:
            if resultType == 'error':
                raise RuntimeError('An unknown error occurred while processing the job (check your input)')
            else:
                self.result('error')
        return result
    
    def submit(self, params, resultTypes):
        """ Submit a new job to the service with the given parameters. 
        Return the output in the specified format. """
        params['email'] = self.__email__
        self.run(params)
        print 'Submitted new', self.service, 'job, jobId:', self.jobId
        print 'Please be patient while the job is completed'
        status = 'RUNNING'
        observe = 0
        while status == 'RUNNING':
            observe = observe + 1
            status = self.status()
            sleep(self.__checkInterval__)
        if status != 'FINISHED':
            raise RuntimeError('An error occurred and the job could not be completed')
        print 'Job complete.'
        self.removeLock()
        if type(resultTypes) != list:
            resultTypes = [resultTypes]
        results = []
        for resultType in resultTypes:
            results.append(self.result(resultType))
        if len(results) == 1:
            return results[0]
        else:
            return results

if __name__=='__main__':
    # Examples
    #seq = fetch('NC_004952', 'refseqn', 'fasta')
    #print seq
    #rows = search('organism:10090+AND+Sumo', 'uniprot', format = 'list') # find proteins in mouse (taxonomic id 10090) that match Sumo
    #print rows
    rows = search('CYP1A1[Gene]+AND+Cavia+Cobaya+[Organism]', 'refseq:protein', format = 'fasta') # find proteins in NCBI's refseq (note different query syntax)
    #print rows
    print idmap(rows[1:10])
    #mygo = getGOTerms(['Q9SJN0','P63166'])
    #mygo = getGOReport(['P20719','P63166','Q9SJN0',])
    #print mygo#['P63166']    # all terms associated with one of the genes
    #print getGODef('GO:0002080')['name']
    #print getGenes(['GO:0002080'], taxo=9606)
