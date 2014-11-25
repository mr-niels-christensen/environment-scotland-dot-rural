import logging
import webapp2
from rdflib import Graph
from appengine.ndbstore import CoarseNDBStore
from dot.rural.sepake.sparql_utils import copy_graph_to_graph, copy_graphs_to_graph
from dot.rural.sepake.querylog import activate
from time import time

_GRAPH_ID = 'current'
activate()

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

class CrawlOrder(webapp2.RequestHandler):
    def get(self):
        if self.request.get('source') == 'pure':
            load_pure_data()
        elif self.request.get('source') == 'ukeof':
            load_ukeof_data()
        elif self.request.get('source') == 'self':
            rewrite()
        else:
            raise Exception('Unknown source: %s' % self.request.get('source'))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Load succeeded')

application = webapp2.WSGIApplication([
    ('''/sparql/current/query\.json.*''', QueryJson),
    ('''/crawl\.order.*''', CrawlOrder),
], debug=True) #debug=true means stack traces in browser

def load_pure_data():
    logging.info('Loading and processing data from PURE...')
    from dot.rural.sepake.pure import university_of_aberdeen
    copy_graph_to_graph(university_of_aberdeen(), graph())
    
def load_ukeof_data():
    logging.info('Loading and processing data from UKEOF...')
    from dot.rural.sepake.ukeof import ukeof_graphs
    copy_graphs_to_graph(ukeof_graphs(), graph())
    
def rewrite():
    tmp = Graph()
    g = graph()
    logging.debug('Reading...')
    tmp += g
    logging.debug('Writing...')
    g += tmp
    
def update(q):
    graph().update(q)
    
def query(q, name):
    store = CoarseNDBStore(identifier = _GRAPH_ID, configuration = {'log' : True})
    store.log(name)
    try:
        response = Graph(store = store).query(q).serialize(format='json')
        return response
    finally:
        store.flush_log(logging.DEBUG)
    
def graph():
    return Graph(store = CoarseNDBStore(identifier = _GRAPH_ID))
