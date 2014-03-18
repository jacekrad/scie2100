"""
Amino Acids with abbreviations and letter:
Alanine         Ala     A 
Arginine        Arg     R 
Aspartate       Asp     D 
Asparagine      Asn     N 
Cysteine        Cys     C 
Glutamate       Glu     E 
Glutamine       Gln     Q 
Glycine         Gly     G 
Histidine       His     H 
Isoleucine      Ile     I
Leucine         Leu     L 
Lysine          Lys     K 
Methionine      Met     M 
Phenylalanine   Phe     F
Proline         Pro     P 
Serine          Ser     S 
Threonine       Thr     T 
Tryptophan      Trp     W 
Tyrosine        Tyr     Y 
Valine          Val     V

* is the "stop codon" indicating the end of translation.
"""
""" This is the standard code used by most organisms for translating DNA codons
    to amino acids. Slightly modified codes are used for example by mitochondria. """

standardTranslation = {
"TTT":"F", "TCT":"S", "TAT":"Y", "TGT":"C",
"TTC":"F", "TCC":"S", "TAC":"Y", "TGC":"C",
"TTA":"L", "TCA":"S", "TAA":"*", "TGA":"*",
"TTG":"L", "TCG":"S", "TAG":"*", "TGG":"W",
"CTT":"L", "CCT":"P", "CAT":"H", "CGT":"R",
"CTC":"L", "CCC":"P", "CAC":"H", "CGC":"R",
"CTA":"L", "CCA":"P", "CAA":"Q", "CGA":"R",
"CTG":"L", "CCG":"P", "CAG":"Q", "CGG":"R",
"ATT":"I", "ACT":"T", "AAT":"N", "AGT":"S",
"ATC":"I", "ACC":"T", "AAC":"N", "AGC":"S",
"ATA":"I", "ACA":"T", "AAA":"K", "AGA":"R",
"ATG":"M", "ACG":"T", "AAG":"K", "AGG":"R",
"GTT":"V", "GCT":"A", "GAT":"D", "GGT":"G",
"GTC":"V", "GCC":"A", "GAC":"D", "GGC":"G",
"GTA":"V", "GCA":"A", "GAA":"E", "GGA":"G",
"GTG":"V", "GCG":"A", "GAG":"E", "GGG":"G",
"---":"-"}

AA_1 = {
    'A': 'ALA',
    'B': 'ASX',
    'C': 'CYS',
    'D': 'ASP',
    'E': 'GLU',
    'F': 'PHE',
    'G': 'GLY',
    'H': 'HIS',
    'I': 'ILE',
    'K': 'LYS',
    'L': 'LEU',
    'M': 'MET',
    'N': 'ASN',
    'P': 'PRO',
    'Q': 'GLN',
    'R': 'ARG',
    'S': 'SER',
    'T': 'THR',
    'V': 'VAL',
    'W': 'TRP',
    'Y': 'TYR',
    'Z': 'GLX'
}

AA_3 = {
    'ALA': 'A',
    'ASX': 'B',
    'CYS': 'C',
    'ASP': 'D',
    'GLU': 'E',
    'PHE': 'F',
    'GLY': 'G',
    'HIS': 'H',
    'ILE': 'I',
    'LYS': 'K',
    'LEU': 'L',
    'MET': 'M',
    'ASN': 'N',
    'PRO': 'P',
    'GLN': 'Q',
    'ARG': 'R',
    'SER': 'S',
    'THR': 'T',
    'VAL': 'V',
    'TRP': 'W',
    'TYR': 'Y',
    'GLX': 'Z'
}

def getThreeLetterCode(aa):
    try:
        assert len(aa) == 1
        return AA_1[aa]
    except AssertionError:
        print "AA code has incorrect length; expected %d got %d" % (1, len(aa))
        raise
    except KeyError:
        print "Invalid amino acid three letter code"
        raise

def getSingleLetterCode(aa):
    try:
        assert len(aa) == 3
        return AA_3[aa]
    except AssertionError:
        print "AA code has incorrect length; expected %d got %d" % (3, len(aa))
        raise
    except KeyError:
        print "Invalid amino acid three letter code"
        raise

