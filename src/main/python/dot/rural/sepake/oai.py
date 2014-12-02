'''
Created on 2 Dec 2014

@author: Niels Christensen
'''
from dot.rural.sepake.xml_to_rdf import XMLGraph
import urllib2
import logging
from rdflib.term import URIRef

_PATH_TO_RESUMPTION_TOKEN = URIRef(u'http://www.openarchives.org/OAI/2.0/#resumptionToken') / URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#value')

class OAIHarvester(object):
    def __init__(self, location, pureset):
        self._location = location
        self._url = 'http://{}/ws/oai?verb=ListRecords&set={}&metadataPrefix=oai_dc'.format(self._location, pureset)
        self._more = True
        
    def next(self):
        logging.debug('GETting {}'.format(self._url))
        xml_input = urllib2.urlopen(self._url, timeout=20)
        page = XMLGraph(xml_input)
        logging.debug('{} triples found in OAI page'.format(len(page)))
        resumptionToken = list(page.objects(predicate = _PATH_TO_RESUMPTION_TOKEN))
        assert len(resumptionToken) <= 1, 'OAI page had {} resumptionTokens'.format(len(resumptionToken))
        if len(resumptionToken) == 0:
            logging.debug('No more OAI pages')
            logging.debug(page.serialize(format = 'n3'))
            self._more = False
        else:
            self._url = 'http://{}/ws/oai?verb=ListRecords&resumptionToken={}'.format(self._location, resumptionToken[0])
            
    def process_all(self):
        while (self._more):
            self.next()
