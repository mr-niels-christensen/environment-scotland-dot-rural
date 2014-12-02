import logging
import webapp2
from rdflib import Graph
from rdflib_appengine.ndbstore import NDBStore
from time import time
from dot.rural.sepake.crawl import route

class _QueryJson(webapp2.RequestHandler):
    def get(self, graphid):
        logging.debug('Responding to {}'.format(self.request.get('name')))
        begin = time()
        #Access-Control-Allow-Origin: *
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/sparql-results+json; charset=utf-8'
        self.response.write(query(graphid,
                                  self.request.get('query'),
                                  self.request.get('name')))
        
        logging.debug('Responded to {} in {:.3f} seconds'.format(self.request.get('name'), time() - begin))

application = webapp2.WSGIApplication([
    webapp2.Route(r'/sparql/<graphid>/query.json', handler=_QueryJson, name='sparql'),
    route(),
], debug=True) #debug=true means stack traces in browser

def query(graphid, q, name):
    store = NDBStore(identifier = graphid, configuration = {'log' : True})
    store.log(name)
    try:
        response = Graph(store = store).query(q).serialize(format='json')
        return response
    finally:
        store.flush_log(logging.DEBUG)
    
