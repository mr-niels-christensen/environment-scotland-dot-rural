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

_ACTIONS = {f.__module__.split('.')[-1] : f for f in [pureOaiPublicationSetHarvester,
                                                      PureRESTPublicationHarvester,
                                                      iterator]}

class _HarvestHandler(webapp2.RequestHandler):
    def get(self, action):
        if 'adminconsolecustompage' in self.request.GET:
            logging.debug('Activated from Admin console')
            del self.request.GET['adminconsolecustompage']
        self.graph = Graph(store = NDBStore(identifier = self.request.GET['graphid']))
        del self.request.GET['graphid']
        if action in _ACTIONS:
            self._harvest(action, _ACTIONS[action])
        else:
            method = getattr(self, '_harvest_' + action.replace('.', '_'))
            method(**self.request.GET)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('OK')
    
    def _harvest(self, action, f):
        tmp = Graph()
        for triples in f(self.graph):
            tmp += triples
            logging.debug('Found {} triples from {}'.format(len(triples), action))
        self.graph += tmp
        
    def _harvest_seed(self, path, host = None):
        if host is None:
            host = self.request.host_url
        url = '{}{}'.format(host, path)
        tmp = Graph()
        sparql_txt = urllib2.urlopen(url, timeout = 10).read()
        tmp.update(sparql_txt)
        self.graph += tmp
    
    def _harvest_ukeof_activities(self):
        tmp = Graph()
        for activityinfo in UKEOFActivityHarvester():
            tmp += activityinfo
        logging.debug('Found {} triples from UKEOF'.format(len(tmp)))
        self.graph += tmp

