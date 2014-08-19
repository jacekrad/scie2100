'''
Created on 23/02/2014

This is my rewrite of the guide.py file for the purpose of learning python and understanding
the code contained in guide.py
in many cases the code is rewritten verbatim, in some it is modified so I can better understand it

the original was written by Dr Mikael Boden

@author: jacekrad
'''

if __name__ == '__main__':
    pass
print("Hello World")

import Tkinter

top = Tkinter.Tk()

a=33

button = Tkinter.Button(top, text=a, command=exit)
button.pack()

if a>10:
    button["text"] ='greater than 10'
else:
    button.config(text='NOT greater than 10')
    
top.mainloop()

#====================================================================
# defines an alphabet of symbols
# a sequence container
#====================================================================
class Alphabet():
    
    ''' assuming this is like a constructor '''
    def __init__(self, symbolString):
        self.symbols = symbolString
        
    ''' __len__ seems like some sort of built in mechanism '''   
    def __len__(self):
        return len(self.symbols)
    
    ''' implements the in operator.  must be another built in mechanism 
        yet the method is executed when the in operator is used'''
    def __contains__(self, symbol):
        return symbol in self.symbols
    
    ''' return the symbols iterator '''
    def __iter__(self):
        tsyms = tuple(self.symbols)
        return tsyms.__iter__()
        ''' the code below would not work as a string does not have a __iter__() method '''
        #return self.symbols.__iter__()
        
    ''' simple dump of the alphabet one symbol per line '''    
    def show(self):
        for sym in alpha:
            print "symbol: ", sym
    

#====================================================================
#
# Biological sequence
#
#====================================================================
class Sequence():
    
    #----------------------------------------------------------------
    # constructor
    #    sequence -
    #    alphabet -
    #    name     -
    #    gappy    - 
    #----------------------------------------------------------------
    def __init__(self, sequence, alphabet, name='', gappy = False):
        
        self.sequence = sequence
        self.alphabet=alphabet
        self.name = name
        self.gappy = gappy
        
        self.__error_check()
        
    #----------------------------------------------------------------
    # so far my understanding tells me that this is a private method 
    # check that symbol is in the alphabet and raise exception if not
    #----------------------------------------------------------------
    def __error_check(self):
        for symbol in self.sequence:
            if not symbol in self.alphabet and (symbol != '-' or not self.gappy):
                raise RuntimeError("invalid symbol: " + symbol)
            

    #----------------------------------------------------------------            
    # the len operator
    #----------------------------------------------------------------            
    def __len__(self):
        return len(self.sequence)
    
    #----------------------------------------------------------------
    # return sequence iterator 
    # let's try something fancy
    #----------------------------------------------------------------
    def __iter__(self):
        return tuple(self.sequence).__iter__()
    
    #----------------------------------------------------------------
    # implement the 'in' operator 
    #----------------------------------------------------------------
    def __contains__(self, item):
        for symbol in self.sequence:
            if symbol == item:
                return True
            else:
                return False
            
    #----------------------------------------------------------------
    # this may be another one of those special methods for containers .... ?????
    # should the index range be checked????
    #----------------------------------------------------------------
    def __getitem__(self, index):
        return self.sequence[index]
        
    #----------------------------------------------------------------
    # write FASTA
    # i renamed the method as I think 'get' is a more appropriate name
    # I don't understand this join stuff so for now just copied verbatim
    #----------------------------------------------------------------
    def get_fasta(self):
        fasta = '>' + self.name + '\n'
        data = self.sequence
        nlines = (len(self.sequence) - 1) / 60 + 1
        for i in range(nlines):
            lineofseq = ''.join(data[i*60 : (i+1)*60]) + '\n'
            fasta += lineofseq
        return fasta                
            
    #----------------------------------------------------------------
    # this seems to be equivalent of Java's toString()
    #----------------------------------------------------------------
    def __str__(self):
        string = self.name + ": "
        for symbol in self:
            string += symbol
        return string
    
    #----------------------------------------------------------------
    # return the number of time the symbol occurs in this sequence
    #----------------------------------------------------------------
    def get_symbol_count(self, findme):
        count = 0
        for symbol in self.sequence:
            if findme == symbol:
                count += 1
        return count
    
    #----------------------------------------------------------------
    # get position of the symbol/sequence in this Sequence
    # what's with this fucking naming convention ... python sux
    #----------------------------------------------------------------
    def find(self, findme):
        return self.sequence.find(findme)
        
alpha = Alphabet('ABCDEFG')
alpha.show()

      
    
    
    
    
    