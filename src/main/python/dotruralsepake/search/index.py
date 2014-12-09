'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph
from rdflib_appengine.ndbstore import NDBStore
import logging
from rdflib.plugins.sparql import prepareQuery
from google.appengine.api import search

_DOCUMENTS = '''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
SELECT ?sepakeuri ?label
WHERE {
    ?sepakeuri rdfs:label ?label .
}
LIMIT 200
'''

def _document_from_sparql_result(sparql_result):
    return search.Document(
    doc_id = sparql_result['sepakeuri'],
    fields=[
       search.HtmlField(name='label', value=sparql_result['label']),
       ])
    
class Indexer(object):
    def __init__(self, graphid):
        self._graph = Graph(store = NDBStore(identifier = graphid))
        self._query = prepareQuery(_DOCUMENTS)
        self._index = search.Index(name = graphid)

    def __iter__(self):
        docs = self._graph.query(self._query)
        logging.debug('Indexing {} documents'.format(len(docs)))
        documents = [_document_from_sparql_result(doc) for doc in docs]
        self._index.put(documents)
        if False:
            yield None

