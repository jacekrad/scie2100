'''
Created on 18/03/2014

@author: jacekrad
'''
boolean = False
boolean = not(boolean)

print boolean

some_int = 2 / 3
print some_int 

some_float = 2.0 / 3
other_float = 2 / float(3)
print some_float, ':', other_float

some_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9, 'a'])
# print some_set.pop(), some_set.pop(), some_set.pop() #wtf???
print 'a' in some_set

# for loop
for counter in range(10):
    print counter

# while
while counter > 0:
    # print counter -= 1 # why this doesn't work
    counter -= 1
    print counter
    
some_list = [1, 2, 'v']
some_tuple = (1, 2, 'x', some_list)

for item in some_list:
    print item
    
print some_tuple

for i,c in [[1, 'I'], [2, 'II'], [3, 'III']]:
    print i, c
    
    