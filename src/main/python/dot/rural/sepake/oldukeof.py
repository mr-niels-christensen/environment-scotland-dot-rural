'''
Created on 16 Sep 2014

@author: s05nc4
'''

import csv
import urllib2
import pprint
from rdflib import Graph, Literal,  Namespace, RDF, RDFS, URIRef
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
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

def _activity(row):
    return URIRef(row['Link to full record'])

def _org(row):
    _SEPAKE.term('ukoef-org#%s' % urllib2.quote(row['Lead organisation']))

def _comment(row):
    comment = row['Description']
    if len(row['Objectives']) > 0:
        comment += '\nObjectives: ' + row['Objectives']
    if len(row['Reasons for collection']) > 0:
        comment += '\nReasons for collection: ' + row['Reasons for collection']
    return Literal(comment)

def _or_None(f):
    return lambda value: None if len(value) == 0 else f(value)

def _get(key):
    return _convert(key, Literal)

def _convert(key, f):
    return lambda row: _or_None(f)(row.get(key, None))

def _const(value):
    return lambda _ : value

_TRIPLES_FOR_ROW = [(_activity, RDF.type, _const(_SEPAKE.project)),
                    (_activity, RDFS.label, _get('Title')),
                    (_activity, RDFS.comment, _comment),
                    (_activity, _PROV.startedAtTime, _convert('Lifespan start', _date_literal)),
                    (_activity, _PROV.endedAtTime, _convert('Lifespan end', _date_literal)),
                    (_activity, FOAF.homepage, _activity),
                    (_org, _SEPAKE.owns, _activity),
                    (_org, RDFS.label, _get('Lead organisation')),
                    ]

class UKEOFtoRDF:
    '''Class for creating RDF triples from UKEOF rows.
    '''
    def __init__(self):
        self._graph = Graph()
        
    def flush(self, other):
        #TODO Use += but it does not seem to work unless context_aware...which does not seem to work with Fuseki
        print 'Flushing...'
        for triple in self._graph:
            print '.',
            other.add(triple)
        print 'Flushed'
    
    def dump(self):
        print self._graph.serialize(format='turtle')
    
    def add_rows(self, rows):
        for row in rows:
            if row['Type'] == 'Activity':
                self._add_activity(row)
    
    def _add_activity(self, row):
        for (sf, p, of) in _TRIPLES_FOR_ROW:
            (s, o) = (sf(row), of(row))
            if not None in [s, p, o]:
                self._graph.add((s, p, o))
    
if __name__ == '__main__':
    rows = [row for row in csv.DictReader(urllib2.urlopen('https://catalogue.ukeof.org.uk/api/documents?format=csv'))]
    g = UKEOFtoRDF()
    g.add_rows(rows)
    #remote = SPARQLUpdateStore(context_aware = False)
    #remote.open(("http://localhost:3030/ds/query", "http://localhost:3030/ds/update"))
    #g.flush(remote)
    for row in rows:
        _simplify(row)
    _stats(rows)
    _sample(rows, 'Type', 'Activity')
    