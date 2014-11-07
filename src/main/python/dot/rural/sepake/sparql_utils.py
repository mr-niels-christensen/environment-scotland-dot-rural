'''
Created on 20 Oct 2014

@author: s05nc4
'''

from dot.rural.sepake.csv_to_rdf import CSV
from rdflib.namespace import FOAF, XSD
from dot.rural.sepake.ontology import SEPAKE, PROV
from rdflib import RDF, RDFS
from rdflib.plugins.sparql.parser import parseUpdate
from rdflib.plugins.sparql.algebra import translateUpdate
import logging
import time

_PERCENTAGES = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 101]

def copy(src_graph, dest_store):
    start = time.time()
    length = len(src_graph)
    logging.info('Storing %d triples...' % length)
    checkpoints = [((x * length) / 100, '%0d%%' % x) for x in _PERCENTAGES]
    total = 0
    for triple in src_graph:
        try:
            dest_store.add(triple)
        except Exception as e:
            logging.warn('Failed to add %s: %s' % (triple, e))
        total += 1
        if total > checkpoints[0][0]:
            logging.debug('%s, %d seconds' % (checkpoints[0][1], time.time() - start))
            checkpoints = checkpoints[1:]
    logging.info('Done')

def expand_and_parse(template_func):
    '''Decorates a function which returns a Python format string.
       The format string must be SPARQL update with namespaces referenced dict-style like this:
       "INSERT {{ ?x <{rdfs.label}> "Hello" }} WHERE {{ ?x <{rdf.type}> <{sepake.HelloType}> }}"
       The decorated function will expand namespaces and return a preparsed SPARQL update.
    '''
    def expanded():
        template = template_func()
        updateString = template.format(csv = CSV,
                                       xsd = XSD,
                                       rdf = RDF, 
                                       rdfs = RDFS, 
                                       prov = PROV, 
                                       foaf = FOAF,
                                       sepake = SEPAKE)
        return translateUpdate(parseUpdate(updateString), None, {})
    return expanded
