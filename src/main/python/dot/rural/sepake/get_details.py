'''
Created on 4 Dec 2014

@author: Niels Christensen
'''
from dot.rural.sepake.xml_to_rdf import XMLGraph
import urllib2
import logging

_PREFIXES = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX sepake: <http://dot.rural/sepake/>
PREFIX sepake: <http://dot.rural/sepake/>
PREFIX sepakecode: <http://dot.rural/sepake/code>
PREFIX prov: <http://www.w3.org/ns/prov/>
PREFIX publication-base_uk: <http://atira.dk/schemas/pure4/model/template/abstractpublication/stable>
PREFIX publication-base_uk_hash: <http://atira.dk/schemas/pure4/model/template/abstractpublication/stable#>
'''

_TASKS = _PREFIXES + '''
SELECT ?sepakeuri ?pureurl
WHERE {
    ?sepakeuri sepake:wasDetailedByCode sepakecode:Pure.rest.publication .
    ?sepakeuri sepake:wasDetailedByData ?pureurl .
    FILTER NOT EXISTS {?sepakeuri sepake:wasDetailedAtTime ?sometime}
}
LIMIT 20
'''

_CONSTRUCT_PUBLICATION = _PREFIXES + '''
SELECT ?sepakeuri
WHERE {
    [] publication-base_uk_hash:includedOnStaffPages / rdf:value "true" .
}
'''

class PureRestPublicationHarvester(object):
    def __init__(self, graph):
        self._graph = graph
    
    def _next(self):
        for row in self._graph.query(_TASKS):
            xml_input = urllib2.urlopen(row['pureurl'], timeout=20)
            page = XMLGraph(xml_input)
            logging.debug('{} triples'.format(len(page)))
            for (s,p,o) in page:
                if p.find('includedOnStaffPages') >= 0:
                    logging.debug('{} {} {}'.format(s, p, o)) 
                    for (p1, o1) in page.predicate_objects(o):
                        logging.debug('{} {} {}'.format(o, p1, o1))
            for row in page.query(_CONSTRUCT_PUBLICATION, initBindings = {'sepakeuri' : row['sepakeuri']}):
                logging.debug(row)
            
