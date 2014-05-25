import stats

class GODB(object):

    def __init__(self, module):
        self.index = __import__(module)

    def find_terms(self, gene):
        """Return all of the GO terms associated with a certain gene"""
        try:
            return set(self.index.gene2go[gene])
        except KeyError:
            # no entry in the GO database for the gene, try gene symbol instead
            try:
                gene_sym = self.index.sym2id[gene]
                return set(self.index.gene2go[gene_sym])
            except KeyError:
                return set()
            

    def find_genes(self, term):
        """Return all of the genes annotated with a certain GO term"""
        try:
            return set(self.index.go2gene[term])
        except KeyError:
            return set()

    def get_gene_background_set(self):
        return set(self.index.gene2go.keys())

    def get_GO_description(self, term):
        return self.index.goterm[term]

    def get_GO_term_overrepresentation(self, pos_entries, bg_entries = None, evalThreshold = None):

        if bg_entries == None:
            bg_entries = self.index.gene2go.keys()
        bg_entries = set(bg_entries)
        pos_entries = set(pos_entries)
        neg_entries = bg_entries - pos_entries

        # Obtain GO terms for each element in our positive and negative sets    
        pos_terms = [self.find_terms(e) for e in pos_entries]
        neg_terms = [self.find_terms(e) for e in neg_entries]
    
        # Collect all relevant GO terms (those found via the positives)
        allPos = set()
        for terms in pos_terms:
            allPos |= terms
    
        # Collect the other GO terms (those found via the negatives)
        all = set(allPos)
        for terms in neg_terms:
            all |= terms
    
        nTerms = len(all)

        # For each term, use Fisher's exact test to establish whether there is
        # a significant difference between occurrence of a term in each set
        allHits = {}
        for seek in allPos:
            pos_in, pos_out, neg_in, neg_out = 0, 0, 0, 0
            for terms in pos_terms:
                if seek in terms:
                    pos_in += 1
                else:
                    pos_out += 1
            for terms in neg_terms:
                if seek in terms:
                    neg_in += 1
                else:
                    neg_out += 1
            p_value = stats.getFETpval(pos_in, neg_in, pos_out, neg_out, left=False)
            # Correct for multiple hypothesis testing
            e_value = p_value * nTerms
            if (evalThreshold == None or evalThreshold >= e_value):
                allHits[seek] = e_value
        return allHits


""" Below is code that will be run if the module is "run",
    and not just "loaded".
"""
if __name__=='__main__':
    pos = [
           'FCP1',
           'YPL106C',    
           'YOL081W',    
           'YOR027W',    
           'YOR299W',    
           'YNL006W',    
           'YNL007C',    
           'YLL039C',    
           'YLR216C']
    godb = GODB('yeast_go')
    terms = godb.find_terms('FCP1')
    print 'FCP1 terms are', terms
    print 'Positives are:', pos
    print 'Genes annotated with GO:0030188:', godb.find_genes('GO:0030188')
    overlap = set(pos) - godb.find_genes('GO:0030188')
    print len(overlap), 'genes overlap'
    r = godb.get_GO_term_overrepresentation(pos, evalThreshold = 1.0)
    for row in r:
        print row, r[row]
        
    
