'''
Created on 16 Sep 2014

@author: s05nc4
'''

import csv
import urllib2

    
if __name__ == '__main__':
    acc = dict()
    for row in csv.DictReader(urllib2.urlopen('https://catalogue.ukeof.org.uk/api/documents?format=csv')):
        for key in row:
            if key not in acc:
                acc[key] = set()
            acc[key].add(row[key])
    for key in acc:
        if len(acc[key]) > 20:
            print '%s: %d values' % (key, len(acc[key]))
        else:
            print '%s: %s' % (key, acc[key])
            
