'''
Created on 2 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph
from rdflib_appengine.ndbstore import NDBStore
from dot.rural.sepake.sparql_utils import copy_graph_to_graph, copy_graphs_to_graph
import logging
import webapp2

GRAPH_ID = 'current'

class CrawlOrder(webapp2.RequestHandler):
    def get(self):
        if self.request.get('type') == 'pure.projects.aberdeen':
            load_pure_data()
        elif self.request.get('type') == 'ukeof':
            load_ukeof_data()
        elif self.request.get('type') == 'self':
            rewrite()
        elif self.request.get('type') == 'pure.oai':
            pass
        else:
            raise Exception('Unknown type: %s' % self.request.get('type'))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Load succeeded')

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
    
def graph():
    return Graph(store = NDBStore(identifier = GRAPH_ID))
