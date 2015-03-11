'''
Created on 2 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph
from rdflib_appengine.ndbstore import NDBStore
import logging
import webapp2
from dotruralsepake.harvest.pure_oai import PURE_OAI_CODE_URI, PUREOAIHarvester
from dotruralsepake.harvest.pure_details import details_iterator_generator
from dotruralsepake.harvest.pure_projects import PURE_PROJECTS_CODE_URI, pure_projects_task_from_url
from dotruralsepake.harvest.nerc import NERC_CODE_URI, nerc_task_from_url
from dotruralsepake.harvest.ukeof import UKEOFActivityHarvester
import urllib2
from dotruralsepake.store import connect
from random import shuffle
from dotruralsepake.rdf.utils import prepareQuery
import datetime

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
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('{} working on /harvest/{} ...\n'.format(datetime.datetime.utcnow(), action))
        if action == 'seed':
            self._harvest_seed(**self.request.GET)
        else:
            iterator = self._get_iterator()
            self._harvest(iterator)
        self.response.write('{} OK, action completed\n'.format(datetime.datetime.utcnow()))

    def _get_iterator(self):
        tasks = [_NERC_TASK_BUILDER.build,
                 _PURE_PROJECTS_TASK_BUILDER.build,
                 _PURE_OAI_TASK_BUILDER.build,
                 details_iterator_generator]
        shuffle(tasks) #Shuffle randomly to avoid running a single failing task repeatedly
        for iterator_builder in tasks:
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

class SingleUriTaskBuilder(object):
    def __init__(self, codeURI, url_to_iterator_fun):
        self._query = _TASK.replace('?codeURI', '<{}>'.format(codeURI))
        self._url_to_iterator_fun = url_to_iterator_fun

    def build(self, graph):
        try:
            result = graph.query(prepareQuery(self._query))
            task = result.__iter__().next()
            logging.debug(task['pureurl'])
            return self._url_to_iterator_fun(task['pureurl'])
        except StopIteration:
            return None

_TASK = '''
PREFIX sepake: <http://dot.rural/sepake/>
PREFIX sepakecode: <http://dot.rural/sepake/code>
SELECT ?pureurl
WHERE {
    ?pureurl sepake:wasDetailedByCode ?codeURI .
    FILTER NOT EXISTS {?pureurl sepake:wasDetailedAtTime ?sometime}
}
LIMIT 1
'''

_NERC_TASK_BUILDER = SingleUriTaskBuilder(NERC_CODE_URI, nerc_task_from_url)
_PURE_PROJECTS_TASK_BUILDER = SingleUriTaskBuilder(PURE_PROJECTS_CODE_URI, pure_projects_task_from_url)
_PURE_OAI_TASK_BUILDER = SingleUriTaskBuilder(PURE_OAI_CODE_URI, PUREOAIHarvester)