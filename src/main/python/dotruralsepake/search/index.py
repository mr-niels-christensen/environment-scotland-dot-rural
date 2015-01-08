'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph, Literal
from rdflib_appengine.ndbstore import NDBStore
from rdflib.plugins.sparql import prepareQuery
from google.appengine.api import search
import logging

_DOCUMENTS = '''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX sepake: <http://dot.rural/sepake/>
PREFIX sepakemetrics: <http://dot.rural/sepake/metrics/>
SELECT ?sepakeuri ?label ?htmlDescription (COUNT(*) AS ?rank)
WHERE {
    { ?sepakeuri rdfs:label ?label .
       FILTER (STRENDS(STR(?sepakeuri), ?suffix))
    } .
    OPTIONAL { ?sepakeuri sepake:htmlDescription ?htmlDescription } .
    OPTIONAL { ?sepakeuri sepakemetrics:focushit []} . 
}
GROUP BY ?sepakeuri
'''

def _document_from_sparql_result(sparql_result):
    fields = [search.HtmlField(name='label', value=sparql_result['label'])]
    if 'htmlDescription' in sparql_result:
        fields.append(search.HtmlField(name='description', value=sparql_result['htmlDescription']))
    return search.Document(doc_id = sparql_result['sepakeuri'], 
                           fields = fields,
                           rank = sparql_result['rank'].value)
    
class Indexer(object):
    def __init__(self, graphid):
        self._index = search.Index(name = graphid)
        self._graph = Graph(store = NDBStore(identifier = graphid))
        
    def __iter__(self):
        for suffix in [str(i) for i in range(10)] + [chr(i) for i in range(ord('a'), ord('g'))]:#Each of the 16 hex digits
            index_now = self._graph.query(_DOCUMENTS.replace('?suffix', '"{}"'.format(suffix)))#initBindings do not work with FILTER
            documents = [_document_from_sparql_result(doc.asdict()) for doc in index_now]
            self._index.put(documents)
            yield len(index_now)

