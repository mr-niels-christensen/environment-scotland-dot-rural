'''
Created on 2 Dec 2014

@author: Niels Christensen
'''
from dotruralsepake.rdf.xml_to_rdf import XMLGraph
import urllib2
from rdflib.term import URIRef, Literal
from rdflib.plugins.sparql import prepareQuery
from urlparse import urlparse
from dotruralsepake.rdf.ontology import SEPAKE
from datetime import datetime
import logging

PURE_OAI_CODE_URI = 'http://dot.rural/sepake/codePureOaiPublicationSetHarvester'

_PATH_TO_RESUMPTION_TOKEN = URIRef(u'http://www.openarchives.org/OAI/2.0/#resumptionToken') / URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#value')

_CONSTRUCT_PAPERS = '''
PREFIX oai_hash: <http://www.openarchives.org/OAI/2.0/#>
PREFIX oai_dc_hash: <http://www.openarchives.org/OAI/2.0/oai_dc/#>
PREFIX dc_hash: <http://purl.org/dc/elements/1.1/#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX sepake: <http://dot.rural/sepake/>
PREFIX sepakecode: <http://dot.rural/sepake/code>
PREFIX prov: <http://www.w3.org/ns/prov/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
CONSTRUCT {
    ?sepakeuri rdf:type prov:Entity .
    ?sepakeuri sepake:htmlDescription ?description .
    ?sepakeuri sepake:wasDetailedByData ?pureurl .
    ?sepakeuri sepake:wasDetailedByCode sepakecode:PureRestPublication .
}
WHERE {
    ?record oai_hash:header / oai_hash:identifier / rdf:value ?identifier .
    ?record oai_hash:metadata / oai_dc_hash:dc / dc_hash:description / rdf:value ?description .
    ?record oai_hash:metadata / oai_dc_hash:dc / dc_hash:subject / rdf:value ?subject .
    BIND ( ( STRAFTER ( ?identifier, "/" ) ) AS ?uuid )
    BIND ( URI ( CONCAT (str ( sepake:PurePublication ), "#", ENCODE_FOR_URI( ?uuid ) ) ) AS ?sepakeuri )
    BIND ( puredomain: AS ?pd)
    BIND ( ( URI ( CONCAT ( STR( ?pd ), "ws/rest/publication?uuids.uuid=", ?uuid) ) ) AS ?pureurl )
    FILTER ( CONTAINS ( LCASE ( ?subject ), "environment" ) ) 
}
'''

class PUREOAIHarvester(object):
    def __init__(self, url):
        self._url = url
        self._original_url = url
        logging.debug(url)
        url_parsed = urlparse(url)
        self._location = url_parsed.netloc
        self._more = True
        self._query = prepareQuery(_CONSTRUCT_PAPERS, initNs={'puredomain' : URIRef('http://{}/'.format(self._location))})
        
    def _next(self):
        xml_input = urllib2.urlopen(self._url, timeout=20)
        page = XMLGraph(xml_input)
        self._handle_resumption_token(page)
        return page.query(self._query, initNs={'puredomain' : URIRef('http://{}/'.format(self._location))})

    def _handle_resumption_token(self, page):
        resumptionToken = list(page.objects(predicate = _PATH_TO_RESUMPTION_TOKEN))
        assert len(resumptionToken) <= 1, 'OAI page had {} resumptionTokens'.format(len(resumptionToken))
        if len(resumptionToken) == 0:
            self._more = False
            self._url = 'No more pages'
        else:
            self._more = True
            self._url = 'http://{}/ws/oai?verb=ListRecords&resumptionToken={}'.format(self._location, resumptionToken[0])
                    
    def __iter__(self):
        yield [(URIRef(self._original_url), SEPAKE.wasDetailedAtTime, Literal(datetime.utcnow()))]
        while (self._more):
            yield self._next()
