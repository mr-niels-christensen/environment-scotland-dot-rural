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
    '''Reads an RSS feed from NERC and describes the found datasets as triples.
       @param url The RSS feed url as a string, i.e. 'http://data-search.nerc.ac.uk/search/full/catalogue.rss?'+parameters
       @return This function is a generator yielding lists of triples
    '''
    #Timestamp marking that this task has been executed
    yield [(URIRef(url), SEPAKE.wasDetailedAtTime, Literal(datetime.utcnow()))]
    xml_input = urllib2.urlopen(url, timeout = 30)
    xml_graph = XMLGraph(xml_input)
    #Loop over each item in the RSS feed:
    for item in xml_graph.objects(URIRef('#rss/channel'), URIRef('#item')):
        text_link = xml_graph.value(subject = item, predicate = URIRef('#link') / RDF.value)
        url_link = URIRef(text_link)
        yield list(_triples_for_rss_item(item, url_link, xml_graph))

def _triples_for_rss_item(item, link, xml_graph):
    yield (link, RDF.type, SEPAKE.NERCDataSet)
    yield (link, RDFS.label, 
           xml_graph.value(subject = item, 
                           predicate = URIRef('#title') / RDF.value))
    yield (link, SEPAKE.htmlDescription, 
           xml_graph.value(subject = item, 
                           predicate = URIRef('#description') / RDF.value))
    #Example date from the RSS feed: 'Wed, 21 Jan 2015 00:00:00 GMT'
    text_date = xml_graph.value(subject = item, 
                                predicate = URIRef('#pubDate') / RDF.value)
    python_datetime = datetime.strptime(text_date, '%a, %d %b %Y %X GMT')
    yield (link, DC.issued, Literal(python_datetime))
