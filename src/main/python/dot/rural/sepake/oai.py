'''
Created on 2 Dec 2014

@author: Niels Christensen
'''
from dot.rural.sepake.xml_to_rdf import XMLGraph
import urllib2
import logging
from rdflib.term import URIRef

_PATH_TO_RESUMPTION_TOKEN = URIRef(u'http://www.openarchives.org/OAI/2.0/#resumptionToken') / URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#value')

_CONSTRUCT_PAPERS = '''
PREFIX oai_hash: <http://www.openarchives.org/OAI/2.0/#>
PREFIX oai_dc_hash: <http://www.openarchives.org/OAI/2.0/oai_dc/#>
PREFIX dc_hash: <http://purl.org/dc/elements/1.1/#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX sepake: <http://dot.rural/sepake/>
CONSTRUCT {
    ?sepakeuri dc:title ?title .
    ?sepakeuri dc:description ?description .
}
WHERE {
    ?record oai_hash:header / oai_hash:identifier / rdf:value ?identifier .
    ?record oai_hash:metadata / oai_dc_hash:dc / dc_hash:title / rdf:value ?title .
    ?record oai_hash:metadata / oai_dc_hash:dc / dc_hash:description / rdf:value ?description .
    BIND ( ( STRAFTER ( ?identifier, "/" ) ) AS ?uuid )
    BIND ( URI ( CONCAT (str ( sepake:PurePublication ), "#", ENCODE_FOR_URI( ?uuid ) ) ) AS ?sepakeuri )
}
'''

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
        for r in list(page.query(_CONSTRUCT_PAPERS))[0:100]:
            logging.debug('SPARQL gave {}'.format(r))
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
