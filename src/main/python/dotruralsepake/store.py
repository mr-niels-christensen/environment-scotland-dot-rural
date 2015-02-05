'''
Created on 4 Feb 2015

@author: Niels Christensen
'''
from rdflib_appengine.ndbstore import NDBStore
from dotruralsepake.rdf.ontology import SEPAKE

def connect(identifier):
    '''Encapsulates common configuration for Graphs stored in NDB
       @param identifier : ID of the stored Graph to access, example: "default"
       @return: An NDBStore for accessing the given Graph
    '''
    return NDBStore(identifier = identifier, 
                    configuration = {'no_of_shards_per_predicate_dict': {SEPAKE.htmlDescription: 16}})
