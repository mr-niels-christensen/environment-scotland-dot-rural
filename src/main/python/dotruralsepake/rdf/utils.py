'''
Created on 20 Oct 2014

@author: s05nc4
'''

from dotruralsepake.rdf.csv_to_rdf import CSV
from rdflib.namespace import FOAF, XSD
from dotruralsepake.rdf.ontology import SEPAKE, PROV
from rdflib import RDF, RDFS, Graph, URIRef
from rdflib.plugins.sparql.parser import parseUpdate
from rdflib.plugins.sparql.algebra import translateUpdate
import logging
import time

_PERCENTAGES = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 101]

def copy_graph_to_graph(src_graph, dest_graph, use_multiadd = True):
    start = time.time()
    length = len(src_graph)
    logging.info('Storing %d triples...' % length)
    if use_multiadd:
        dest_graph += src_graph
        logging.debug('Done, storing took %f seconds' % (time.time() - start))
        return
    checkpoints = [((x * length) / 100, '%0d%%' % x) for x in _PERCENTAGES]
    total = 0
    for triple in src_graph:
        try:
            dest_graph.add(triple)
        except Exception as e:
            logging.warn('Failed to add %s: %s' % (triple, e))
        total += 1
        if total > checkpoints[0][0]:
            logging.debug('%s, %f seconds' % (checkpoints[0][1], time.time() - start))
            checkpoints = checkpoints[1:]
    logging.info('Done')

def copy_graphs_to_graph(src_graphs, dest_graph, use_multiadd = True):
    union_graph = Graph()
    for g in src_graphs:
        union_graph += g
    copy_graph_to_graph(union_graph, dest_graph, use_multiadd)

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

'''Used as a marker for members that are to be treated as RDF names.'''
RDF_NAME = object()

class _URIRefCreator(type):
    '''See http://eli.thegreenplace.net/2011/08/14/python-metaclasses-by-example/
       A metaclass is required in order to assign a static member of a class
       outside its definition.
       This metaclass transforms any static member that is equal to RDF_NAME
       into an rdflib.URIRef based on the static member's name.
    '''
    def __getattribute__(self, name):
        '''This method will be called when you access MYCLASS.MYSTATICMEMBER if
           MYCLASS.__metaclass__ == _URIRefCreator
        '''
        try:
            x = type.__getattribute__(self, name) #This is the default lookup operation
            if x is RDF_NAME: #Replace the dummy value with a URIRef based on name
                return URIRef(type.__getattribute__(self, 'BASE_URI') + name)
            else:
                return x
        except AttributeError:
            raise AttributeError('Attribute "%s" missing. You may want to add "%s = RDF_NAME" to your namespace class' % (name, name))
    
    def __str__(self):
        return type.__getattribute__(self, 'BASE_URI')
    
def namespace(base_uri, separator = '#'):
    '''Usage: @namespace('http://example.com')
              class MyClass:
                  myRdfName = RDF_NAME
        Transforms MyClass so that MyClass.myRdfName will equal
        URIRef('http://example.com#myRdfName')
    '''
    def class_rebuilder(cls):
        class NamespaceClass(cls):
            __metaclass__ = _URIRefCreator
            BASE_URI = base_uri + separator
        return NamespaceClass
    return class_rebuilder
