'''
Created on 2 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph
from rdflib_appengine.ndbstore import NDBStore
from dotruralsepake.rdf.utils import copy_graph_to_graph, copy_graphs_to_graph
import logging
import webapp2
from dotruralsepake.harvest.pure_oai import PUREOAIHarvester
from dotruralsepake.harvest.pure_details import PureRESTPublicationHarvester

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
    from dotruralsepake.harvest.pure_projects import university_of_aberdeen
    copy_graph_to_graph(university_of_aberdeen(), _graph(graphid))
    
def _load_ukeof_data(graphid):
    logging.info('Loading and processing data from UKEOF...')
    from dotruralsepake.harvest.ukeof import ukeof_graphs
    copy_graphs_to_graph(ukeof_graphs(), _graph(graphid))

def _crawl_pure_oai(graphid, location, pureset):
    tmp = Graph()
    for papers in PUREOAIHarvester(location, pureset):
        tmp += papers
        logging.debug('Found {} triples from OAI'.format(len(papers)))
    g = _graph(graphid)
    g += tmp

def _crawl_pure_details(graphid):
    g = _graph(graphid)
    tmp = Graph()
    for details in PureRESTPublicationHarvester(g):
        tmp += details
    g += tmp

_ACTIONS = { 'pure.projects.aberdeen' : _load_pure_data,
             'ukeof' :                  _load_ukeof_data,
             'pure.oai' :               _crawl_pure_oai,
             'pure.details' :           _crawl_pure_details,
            }
