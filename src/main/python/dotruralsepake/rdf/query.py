'''
Created on 15 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph, URIRef
from rdflib_appengine.ndbstore import NDBStore
import logging
import urllib2
from google.appengine.api import memcache

class SPARQLQueryResolver(object):
    def __init__(self, host_url, graphid):
        self._store = NDBStore(identifier = graphid, configuration = {'log' : True})
        self._resolver = _QueryPrepareAndCache(host_url, self._store)
        
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
            response = Graph(store = self._store).query(self._resolver.query(queryUrl), initBindings = bindings)
            if response.type == 'CONSTRUCT':
                g = Graph()
                g += response
                response = g.query("SELECT ?s ?p ?o WHERE {?s ?p ?o}")
            return response
        finally:
            self._store.flush_log(logging.DEBUG)
            
class _QueryPrepareAndCache(object):
    def __init__(self, host_url, log_object):
        self._host_url = host_url
        self._log_object = log_object
        
    def query(self, queryUrl):
        full_url = '{}{}'.format(self._host_url, queryUrl)
        sparql_txt = memcache.get(full_url)
        self._log_object.log('Query {}: {}'.format(full_url, 'found in cache' if sparql_txt else 'not in cache, GETting...'))
        if sparql_txt is not None:
            return sparql_txt
        sparql_txt = urllib2.urlopen(full_url, timeout = 5).read()
        memcache.add(full_url, sparql_txt, 86400)
        return sparql_txt
