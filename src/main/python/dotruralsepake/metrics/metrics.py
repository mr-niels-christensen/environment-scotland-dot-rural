'''
Created on 17 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph
from dotruralsepake.store import connect

_METRICS_GRAPH_ID = 'metrics'
_METRICS_GRAPH = Graph(connect(_METRICS_GRAPH_ID))

def register_query(queryUrl, bindings, resolver):
    if queryUrl == '/sparql-queries/focus.sparql.txt':
        _METRICS_GRAPH.update(resolver.resolve('/sparql-backend/update-metrics-focus-hit.sparql.txt'), 
                              initBindings = bindings)
        