'''
Created on 2 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph
from rdflib_appengine.ndbstore import NDBStore
import logging
import webapp2
from dotruralsepake.harvest.pure_oai import oai_iterator_generator
from dotruralsepake.harvest.pure_details import details_iterator_generator
from dotruralsepake.harvest.pure_projects import rest_iterator_generator
from dotruralsepake.harvest.ukeof import UKEOFActivityHarvester
import urllib2
from dotruralsepake.store import connect

def route():
    return webapp2.Route(r'/harvest/<action>', handler=_HarvestHandler, name='harvest')

class _HarvestHandler(webapp2.RequestHandler):
    def get(self, action):
        if 'adminconsolecustompage' in self.request.GET:
            logging.debug('Activated from Admin console')
            del self.request.GET['adminconsolecustompage']
        self.graph = Graph(store = connect(identifier = self.request.GET['graphid']))
        del self.request.GET['graphid']
        assert action in ['seed', 'external']
        if action == 'seed':
            self._harvest_seed(**self.request.GET)
        else:
            iterator = self._get_iterator()
            self._harvest(iterator)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('OK')
    
    def _get_iterator(self):
        for iterator_builder in [rest_iterator_generator,
                                 oai_iterator_generator,
                                 details_iterator_generator,
                                 ]:
            iterator = iterator_builder(self.graph)
            if iterator is not None:
                return iterator
        return []
    
    def _harvest(self, iterator):
        tmp = Graph()
        for triples in iterator:
            tmp += triples
            logging.debug('Found {} triples'.format(len(triples)))
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

