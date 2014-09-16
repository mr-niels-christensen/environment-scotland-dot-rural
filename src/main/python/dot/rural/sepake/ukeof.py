'''
Created on 16 Sep 2014

@author: s05nc4
'''

import csv
import urllib2

def stats(rows):
    acc = dict()
    for row in rows:
        for key in row:
            if key not in acc:
                acc[key] = set()
            acc[key].add(row[key])
    for key in acc:
        if len(acc[key]) > 20:
            print '%s: %d values' % (key, len(acc[key]))
        else:
            print '%s: %s' % (key, acc[key])

def sample(rows, key, value, n=10):
    print '%s=%s' % (key, value)
    for row in [row for row in rows if row[key] == value][:n]:
        print row

def simplify(row):
    row['label'] = row['Title']
    del row['Title']
    row['comment'] = row['Description']
    if len(row['Objectives']) > 0:
        row['comment']  += '\nObjectives: ' + row['Objectives']
    if len(row['Reasons for collection']) > 0:
        row['comment']  += '\nReasons for collection: ' + row['Reasons for collection']
    del row['Description']
    del row['Objectives']
    del row['Reasons for collection']
    del row['GMES codings']
    del row['GEOSS codings']
    del row['ECV codings']
    del row['Legal background']
    return row
    
if __name__ == '__main__':
    rows = [simplify(row) for row in csv.DictReader(urllib2.urlopen('https://catalogue.ukeof.org.uk/api/documents?format=csv'))]
    stats(rows)
    sample(rows, 'Type', 'Activity')
    sample(rows, 'Type', 'Facility')
    sample(rows, 'Type', 'Network')
    sample(rows, 'Type', 'Programme')
    