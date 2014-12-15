import logging
import webapp2
from time import time
from dotruralsepake.rdf.query import SPARQLQueryResolver
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
        resolver = SPARQLQueryResolver(graphid)
        if querySource == 'dynamic':
            result = resolver.dynamic(**self.request.GET)
        else:
            result = resolver.predefined(**self.request.GET)
        self.response.write(result.serialize(format='json'))        
        logging.debug('Responded to {} in {:.3f} seconds'.format(self.request.get('name'), time() - begin))
        


