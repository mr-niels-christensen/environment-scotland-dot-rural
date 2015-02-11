'''
Created on 20 Oct 2014


@author: Niels Christensen

'''

from dotruralsepake.rdf.ontology import SEPAKECODE
import logging
from dotruralsepake.rdf.ontology import PROV

from rdflib.namespace import RDF, RDFS, DC
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
    link = URIRef(xml_graph.value(subject = item, predicate = URIRef('#link') / RDF.value))
    triples = [(link, RDF.type, SEPAKE.NERCDataSet)]
    triples.append((link, 
                    RDFS.label, 
                    xml_graph.value(subject = item, 
                                    predicate = URIRef('#title') / RDF.value)))
    triples.append((link, 
                    SEPAKE.htmlDescription, 
                    xml_graph.value(subject = item, 
                                    predicate = URIRef('#description') / RDF.value)))
    pubDate = datetime.strptime(xml_graph.value(subject = item, 
                                predicate = URIRef('#pubDate') / RDF.value), '%a, %d %b %Y %X GMT')
    triples.append((link, 
                    DC.issued, 
                    Literal(pubDate)))
    return triples
