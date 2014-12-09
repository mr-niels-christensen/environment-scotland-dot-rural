import logging
import webapp2
from rdflib import Graph
from rdflib_appengine.ndbstore import NDBStore
from time import time
'''
Created on 8 Dec 2014

@author: s05nc4
'''

def route():
    return webapp2.Route(r'/sparql/<graphid>/query.json', handler=_QueryJson, name='sparql')

class _QueryJson(webapp2.RequestHandler):
    def get(self, graphid):
        logging.debug('Responding to {}'.format(self.request.get('name')))
        begin = time()
        #Access-Control-Allow-Origin: *
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/sparql-results+json; charset=utf-8'
        self.response.write(_query(graphid,
                                  self.request.get('query'),
                                  self.request.get('name')))
        
        logging.debug('Responded to {} in {:.3f} seconds'.format(self.request.get('name'), time() - begin))

def _query(graphid, q, name):
    store = NDBStore(identifier = graphid, configuration = {'log' : True})
    store.log(name)
    try:
        response = Graph(store = store).query(q).serialize(format='json')
        return response
    finally:
        store.flush_log(logging.DEBUG)
    


