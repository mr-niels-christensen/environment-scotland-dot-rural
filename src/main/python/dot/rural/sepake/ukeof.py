'''
Created on 16 Sep 2014

@author: s05nc4
'''

import csv
import urllib2
import pprint
from rdflib import Graph, Literal,  Namespace, RDF, RDFS, URIRef
from rdflib.namespace import FOAF
import datetime

def _stats(rows):
    '''Reads a list of rows and prints out stats on the use of field
    '''
    acc = dict()
    total = 0
    for row in rows:
        total += 1
        for key in row:
            if key not in acc:
                acc[key] = set()
            acc[key].add(row[key])
    print 'Total number of rows: %d' % total
    for key in acc:
        if len(acc[key]) > 20:
            print '%s: %d values' % (key, len(acc[key]))
        else:
            print '%s: %s' % (key, acc[key])

def _sample(rows, key, value, n=2):
    '''Reads a list of rows and prints out sample row for which
       key is mapped to value.
    '''
    print '%s=%s' % (key, value)
    for row in [row for row in rows if row[key] == value][:n]:
        pprint.pprint(row)

def _simplify(row):
    '''Updates the given row.
       Removes the fields that are globally not in use.
       Centralizes other fields in RDF-friendly fields.
       @return: The updated row
    '''
    #Rename Title to label
    row['label'] = row['Title']
    del row['Title']
    #Collect free text descriptions in comment
    row['comment'] = row['Description']
    if len(row['Objectives']) > 0:
        row['comment']  += '\nObjectives: ' + row['Objectives']
    if len(row['Reasons for collection']) > 0:
        row['comment']  += '\nReasons for collection: ' + row['Reasons for collection']
    del row['Description']
    del row['Objectives']
    del row['Reasons for collection']
    #Remove unused fields
    del row['GMES codings']
    del row['GEOSS codings']
    del row['ECV codings']
    del row['Legal background']
    #Return the updated row (to allow use in list comprehension)
    return row

_SEPAKE = Namespace('http://dot.rural/sepake/')
_PROV  = Namespace('http://www.w3.org/ns/prov#')

def _date_literal(str_date):
    '''Converts a date from UKEOF into an rdflib Literal
    '''
    return Literal(datetime.datetime.strptime(str_date, '%Y-%m-%d').date())

class UKEOFtoRDF:
    '''Class for creating RDF triples from UKEOF rows.
    '''
    def __init__(self):
        self._graph = Graph()
        
    def flush(self):
        print self._graph.serialize(format='turtle')
    
    def add_activity(self, simple_row):
        activity = URIRef(simple_row['Link to full record'])
        self._graph.add((activity, RDF.type, _SEPAKE.project))
        self._graph.add((activity, RDFS.label, Literal(simple_row['label'])))
        self._graph.add((activity, RDFS.comment, Literal(simple_row['comment'])))
        self._graph.add((activity, _PROV.startedAtTime, _date_literal(simple_row['Lifespan start'])))
        self._graph.add((activity, _PROV.endedAtTime, _date_literal(simple_row['Lifespan end'])))
        self._graph.add((activity, FOAF.homepage, activity))
        org = _SEPAKE.term('ukoef-org#%s' % urllib2.quote(simple_row['Lead organisation']))
        self._graph.add((org, _SEPAKE.owns, activity))
        self._graph.add((org, RDFS.label, Literal(simple_row['Lead organisation'])))
    
if __name__ == '__main__':
    rows = [_simplify(row) for row in csv.DictReader(urllib2.urlopen('https://catalogue.ukeof.org.uk/api/documents?format=csv'))]
    g = UKEOFtoRDF()
    for simple_row in [row for row in rows if row['Type'] == 'Activity'][:1]:
        g.add_activity(simple_row)
    g.flush()
    _stats(rows)
    _sample(rows, 'Type', 'Activity')
    