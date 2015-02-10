'''
Created on 20 Oct 2014


@author: Niels Christensen

'''

from dotruralsepake.rdf.ontology import SEPAKECODE
from rdflib import RDF, RDFS, URIRef, Literal
import logging
from dotruralsepake.rdf.ontology import PROV


from rdflib.namespace import RDF
from rdflib import URIRef, Literal
from dotruralsepake.rdf.ontology import SEPAKE
from dotruralsepake.rdf.xml_to_rdf import XMLGraph
from datetime import datetime
import urllib2

NERC_CODE_URI = 'http://dot.rural/sepake/codeNercRSS'

def nerc_task_from_url(url):
    yield [(URIRef(url), SEPAKE.wasDetailedAtTime, Literal(datetime.utcnow()))]
    xml_input = urllib2.urlopen(url, timeout = 30)
    xml_graph = XMLGraph(xml_input)
    for item in xml_graph.objects(URIRef('#rss/channel'), URIRef('#item')):
        yield _triples_for(item, xml_graph)

def _triples_for(item, xml_graph):
    link = xml_graph.value(subject = item, predicate = URIRef('#link')/RDF.value)
    return [(link, RDF.type, SEPAKE.NERCDataSet)]