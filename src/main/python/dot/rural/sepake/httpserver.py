import logging
import webapp2
from rdflib import Graph
from appengine.ndbstore import NDBStore
from dot.rural.sepake.sparql_utils import copy_graph_to_graph, copy_graphs_to_graph
from time import time

_GRAPH_ID = 'current'

class QueryJson(webapp2.RequestHandler):
    def get(self):
        begin = time()
        #Access-Control-Allow-Origin: *
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/sparql-results+json; charset=utf-8'
        self.response.write(query(self.request.get('query'),
                                  self.request.get('name')))
        logging.debug('Responded to %s in %f seconds' % (self.request.get('name'), time() - begin))

class CrawlOrder(webapp2.RequestHandler):
    def get(self):
        #load_pure_data()
        load_ukeof_data()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Load succeeded')

application = webapp2.WSGIApplication([
    ('''/sparql/current/query\.json.*''', QueryJson),
    ('''/crawl.order''', CrawlOrder),
], debug=True) #debug=true means stack traces in browser

def load_pure_data():
    logging.info('Loading and processing data from PURE...')
    from dot.rural.sepake.pure import university_of_aberdeen
    copy_graph_to_graph(university_of_aberdeen(), graph())
    
def load_ukeof_data():
    logging.info('Loading and processing data from UKEOF...')
    from dot.rural.sepake.ukeof import ukeof_graphs
    (length, graphs) = ukeof_graphs()
    copy_graphs_to_graph(length, graphs, graph())
    
def update(q):
    graph().update(q)
    
def query(q, name):
    try:
        return graph().query(q).serialize(format='json')
    except Exception as e:
        logging.warn('%s caused %s'.format(q, e))
        raise e
    
def graph():
    return Graph(store = NDBStore(identifier = _GRAPH_ID))

