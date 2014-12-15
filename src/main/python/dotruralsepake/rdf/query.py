'''
Created on 15 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph, URIRef
from rdflib_appengine.ndbstore import NDBStore
import logging
import urllib2

class SPARQLQueryResolver(object):
    def __init__(self, host_url, graphid):
        self._store = NDBStore(identifier = graphid, configuration = {'log' : True})
        self._host_url = host_url
        
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
        full_url = '{}{}'.format(self._host_url, queryUrl)
        self._store.log(full_url)
        sparql_txt = urllib2.urlopen(full_url, timeout = 5)
        try:
            bindings = {key : URIRef(kwargs[key]) for key in kwargs if key != 'query'}
            response = Graph(store = self._store).query(sparql_txt, initBindings = bindings)
            return response
        finally:
            self._store.flush_log(logging.DEBUG)