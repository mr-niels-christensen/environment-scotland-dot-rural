import logging
import webapp2
from rdflib import Graph
from rdflib_appengine.ndbstore import NDBStore
from time import time
from dot.rural.sepake.crawl import CrawlOrder, GRAPH_ID

class QueryJson(webapp2.RequestHandler):
    def get(self):
        logging.debug('Responding to {}'.format(self.request.get('name')))
        begin = time()
        #Access-Control-Allow-Origin: *
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/sparql-results+json; charset=utf-8'
        self.response.write(query(self.request.get('query'),
                                  self.request.get('name')))
        
        logging.debug('Responded to {} in {:.3f} seconds'.format(self.request.get('name'), time() - begin))

application = webapp2.WSGIApplication([
    ('''/sparql/current/query\.json.*''', QueryJson),
    ('''/crawl\.order.*''', CrawlOrder),
], debug=True) #debug=true means stack traces in browser

def query(q, name):
    store = NDBStore(identifier = GRAPH_ID, configuration = {'log' : True})
    store.log(name)
    try:
        response = Graph(store = store).query(q).serialize(format='json')
        return response
    finally:
        store.flush_log(logging.DEBUG)
    
