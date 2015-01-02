'''
Created on 15 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph, URIRef
from rdflib_appengine.ndbstore import NDBStore
import logging
from dotruralsepake.metrics.metrics import register_query

class SPARQLQueryExecutor(object):
    def __init__(self, resolver, graphid):
        self._store = NDBStore(identifier = graphid, configuration = {'log' : False})
        self._resolver = resolver
        
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
        try:
            bindings = {key : URIRef(kwargs[key]) for key in kwargs}
            response = Graph(store = self._store).query(self._resolver.resolve(queryUrl), initBindings = bindings)
            register_query(queryUrl, bindings, self._resolver)
            if response.type == 'CONSTRUCT': #These cannot be JSON-serialized so we extract the data with a SELECT
                g = Graph()
                g += response
                response = g.query("SELECT ?s ?p ?o WHERE {?s ?p ?o}")
            return response
        finally:
            self._store.flush_log(logging.DEBUG)
            
