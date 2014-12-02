'''
Created on 2 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph
from rdflib_appengine.ndbstore import NDBStore
from dot.rural.sepake.sparql_utils import copy_graph_to_graph, copy_graphs_to_graph
import logging
import webapp2
from dot.rural.sepake.oai import OAIHarvester

def route():
    return webapp2.Route(r'/crawl/<action>', handler=_CrawlHandler, name='crawl')

class _CrawlHandler(webapp2.RequestHandler):
    def get(self, action):
        _ACTIONS[action](**self.request.GET)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('OK')

def _graph(graphid):
    return Graph(store = NDBStore(identifier = graphid))

def _load_pure_data(graphid):
    logging.info('Loading and processing data from PURE...')
    from dot.rural.sepake.pure import university_of_aberdeen
    copy_graph_to_graph(university_of_aberdeen(), _graph(graphid))
    
def _load_ukeof_data(graphid):
    logging.info('Loading and processing data from UKEOF...')
    from dot.rural.sepake.ukeof import ukeof_graphs
    copy_graphs_to_graph(ukeof_graphs(), _graph(graphid))

def _crawl_pure_oai(graphid, location, pureset):
    crawler = OAIHarvester('http://{}/ws/oai?verb=ListRecords&set={}&metadataPrefix=oai_dc'.format(location, pureset))
    crawler.next()

_ACTIONS = { 'pure.projects.aberdeen' : _load_pure_data,
             'ukeof' :                  _load_ukeof_data,
             'pure.oai' :               _crawl_pure_oai,
            }
