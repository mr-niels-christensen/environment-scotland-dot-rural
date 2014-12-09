'''
Created on 2 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph
from rdflib_appengine.ndbstore import NDBStore
import logging
import webapp2
from dotruralsepake.harvest.pure_oai import PUREOAIHarvester
from dotruralsepake.harvest.pure_details import PureRESTPublicationHarvester
from dotruralsepake.harvest.pure_projects import PureRESTProjectHarvester
from dotruralsepake.harvest.ukeof import UKEOFActivityHarvester

def route():
    return webapp2.Route(r'/harvest/<action>', handler=_HarvestHandler, name='harvest')

class _HarvestHandler(webapp2.RequestHandler):
    def get(self, action):
        _ACTIONS[action](**self.request.GET)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('OK')

def _graph(graphid):
    return Graph(store = NDBStore(identifier = graphid))

def _harvest_pure_projects(graphid, location):
    tmp = Graph()
    for projectinfo in PureRESTProjectHarvester(location = location):
        tmp += projectinfo
        logging.debug('Found {} triples from PURE projects'.format(len(projectinfo)))
    g = _graph(graphid)
    g += tmp
    
def _harvest_ukeof_activities(graphid):
    tmp = Graph()
    for activityinfo in UKEOFActivityHarvester():
        tmp += activityinfo
    logging.debug('Found {} triples from UKEOF'.format(len(tmp)))
    g = _graph(graphid)
    g += tmp

def _harvest_pure_oai(graphid, location, pureset):
    tmp = Graph()
    for papers in PUREOAIHarvester(location, pureset):
        tmp += papers
        logging.debug('Found {} triples from OAI'.format(len(papers)))
    g = _graph(graphid)
    g += tmp

def _harvest_pure_details(graphid):
    g = _graph(graphid)
    tmp = Graph()
    for details in PureRESTPublicationHarvester(g):
        tmp += details
    g += tmp

_ACTIONS = { 'pure.projects' : _harvest_pure_projects,
             'ukeof' :         _harvest_ukeof_activities,
             'pure.oai' :      _harvest_pure_oai,
             'pure.details' :  _harvest_pure_details,
            }
