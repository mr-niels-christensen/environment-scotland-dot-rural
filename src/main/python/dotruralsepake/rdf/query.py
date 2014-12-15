'''
Created on 15 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph, URIRef
from rdflib_appengine.ndbstore import NDBStore
import logging
import urllib2

class SPARQLQueryResolver(object):
    def __init__(self, graphid):
        self._store = NDBStore(identifier = graphid, configuration = {'log' : True})
        
    def dynamic(self, name = None, query = None):
        assert name is not None, 'name parameter required'
        assert query is not None, 'query parameter required'
        self._store.log(name)
        try:
            response = Graph(store = self._store).query(query)
            return response
        finally:
            self._store.flush_log(logging.DEBUG)
            
    def predefined(self, queryUrl = None, **kwargs):
        assert queryUrl is not None, 'queryUrl parameter required'
        self._store.log(queryUrl)
        sparql_txt = urllib2.urlopen(queryUrl, timeout = 5)
        try:
            bindings = {key : URIRef(value) for (key, value) in kwargs if key != 'query'}
            response = Graph(store = self._store).query(sparql_txt, initBindings = bindings)
            return response
        finally:
            self._store.flush_log(logging.DEBUG)