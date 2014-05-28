'''
Created on 27/05/2014

@author: s4361277
'''
import stats
significance_level = 0.05
positives = set({"YPL106C", "YOL081W", "YOR027W", "YOR299W", "YNL006W", \
                 "YNL007C", "YLL039C", "YLR216C"})
has_property = set({"YER048C", "YIL016W", "YLR090W", "YOR027W", "YMR161W", \
                    "YNL064C", "YNL281W", "YDR214W", "YPL106C", "YNL007C", "YNL227C"})

a = len(positives.intersection(has_property))
b = 8 - a
c = 2
d = 14 - c

p_value = stats.getFETpval(a, b, c, d, left=False)

print "P value=", p_value

if p_value < significance_level:
    print "reject null hypothesis"
else:
    print "do not reject null hypothesis"