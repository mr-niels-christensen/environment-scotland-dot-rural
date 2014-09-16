'''
Created on 16 Sep 2014

@author: s05nc4
'''

import csv
import urllib2

    
if __name__ == '__main__':
    for row in csv.DictReader(urllib2.urlopen('https://catalogue.ukeof.org.uk/api/documents?format=csv')):
        print row
