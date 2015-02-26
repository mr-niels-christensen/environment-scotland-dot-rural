import logging
import webapp2
from time import time
from dotruralsepake.rdf.query import SPARQLQueryExecutor
import urllib2
from google.appengine.api import memcache

'''
Created on 8 Dec 2014

@author: s05nc4
'''

def route():
    return webapp2.Route(r'/sparql/<graphid>/<querySource:(dynamic|predefined)>.json', handler=_SPARQLHandler, name='sparql')

class _SPARQLHandler(webapp2.RequestHandler):
    def get(self, graphid, querySource):
        begin = time()
        #Access-Control-Allow-Origin: *
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/sparql-results+json; charset=utf-8'
        resolver = SPARQLQueryExecutor(SPARQLQueryResolver(self.request.host_url), graphid)
        if querySource == 'dynamic':
            result = resolver.dynamic(**self.request.GET)
        else:
            result = resolver.predefined(**self.request.GET)
        self.response.write(result.serialize(format='json'))        
        logging.debug('Responded to {} in {:.3f} seconds'.format(self.request.get('name'), time() - begin))
        
class SPARQLQueryResolver(object):
    def __init__(self, host_url):
        self._host_url = host_url
        
    def resolve(self, queryUrl):
        full_url = '{}{}'.format(self._host_url, queryUrl)
        memcache_key = '_QueryPrepareAndCache.{}'.format(full_url)
        sparql_txt = memcache.get(memcache_key)
        if sparql_txt is not None:
            return sparql_txt
        sparql_txt = urllib2.urlopen(full_url, timeout = 5).read()
        memcache.add(memcache_key, sparql_txt, 86400)
        return sparql_txt
