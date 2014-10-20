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
