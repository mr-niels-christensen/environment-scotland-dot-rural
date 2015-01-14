'''
Created on 2 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph
from rdflib_appengine.ndbstore import NDBStore
import logging
import webapp2
from dotruralsepake.harvest.pure_oai import pureOaiPublicationSetHarvester
from dotruralsepake.harvest.pure_details import PureRESTPublicationHarvester
from dotruralsepake.harvest.pure_projects import iterator
from dotruralsepake.harvest.ukeof import UKEOFActivityHarvester
import urllib2

def route():
    return webapp2.Route(r'/harvest/<action>', handler=_HarvestHandler, name='harvest')

class _HarvestHandler(webapp2.RequestHandler):
    def get(self, action):
        if 'adminconsolecustompage' in self.request.GET:
            logging.debug('Activated from Admin console')
            del self.request.GET['adminconsolecustompage']
        self.graph = Graph(store = NDBStore(identifier = self.request.GET['graphid']))
        del self.request.GET['graphid']
        method = getattr(self, '_harvest_' + action.replace('.', '_'))
        method(**self.request.GET)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('OK')
    
    def _harvest_seed(self, path, host = None):
        if host is None:
            host = self.request.host_url
        url = '{}{}'.format(host, path)
        tmp = Graph()
        sparql_txt = urllib2.urlopen(url, timeout = 10).read()
        tmp.update(sparql_txt)
        self.graph += tmp
    
    def _harvest_pure_projects(self):
        tmp = Graph()
        for projectinfo in iterator(self.graph):
            tmp += projectinfo
            logging.debug('Found {} triples from PURE projects'.format(len(projectinfo)))
        self.graph += tmp
        
    def _harvest_ukeof_activities(self):
        tmp = Graph()
        for activityinfo in UKEOFActivityHarvester():
            tmp += activityinfo
        logging.debug('Found {} triples from UKEOF'.format(len(tmp)))
        self.graph += tmp
    
    def _harvest_pure_oai(self):
        tmp = Graph()
        for papers in pureOaiPublicationSetHarvester(self.graph):
            tmp += papers
            logging.debug('Found {} triples from OAI'.format(len(papers)))
        self.graph += tmp
    
    def _harvest_pure_details(self):
        tmp = Graph()
        for details in PureRESTPublicationHarvester(self.graph):
            tmp += details
        self.graph += tmp

