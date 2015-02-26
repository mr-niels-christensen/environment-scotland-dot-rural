'''
Created on 4 Feb 2015

@author: Niels Christensen
'''
from rdflib_appengine.ndbstore import NDBStore
from rdflib import Graph
from dotruralsepake.rdf.ontology import SEPAKE, SEPAKEMETRICS
import logging
from datetime import datetime

_STANDARD_CONFIGURATION = {'no_of_shards_per_predicate_dict': {SEPAKE.htmlDescription: 16,
                                                               SEPAKEMETRICS.focushit: 16},}

_A = NDBStore(identifier = 'A', configuration = _STANDARD_CONFIGURATION)
_B = NDBStore(identifier = 'B', configuration = _STANDARD_CONFIGURATION)

def connect(identifier):
    '''Encapsulates common configuration for Graphs stored in NDB
       @param identifier : ID of the stored Graph to access, example: "default"
       @return: An NDBStore for accessing the given Graph
    '''
    if identifier not in ['metrics', 'default', 'newdata']:
        logging.warn('Unexpected graph identifier: {}'.format(identifier))
    if identifier not in ['default', 'newdata']:
        return NDBStore(identifier = identifier, 
                    configuration = _STANDARD_CONFIGURATION)
    if _max_timestamp(_B) > _max_timestamp(_A):
            default = _B
            newdata = _A
    else:
            default = _A
            newdata = _B
    if identifier == 'default':
        return default
    assert identifier == 'newdata'
    return newdata

def _max_timestamp(store):
    graph = Graph(store)
    return max([o.value for o in graph.objects(SEPAKE.ThisGraph, SEPAKE.graphSetAsDefault)] + 
               [datetime(1970,1,1)]) #Use this datetime if there were no timestamps in the graph
