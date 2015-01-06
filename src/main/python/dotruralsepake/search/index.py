'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph
from rdflib_appengine.ndbstore import NDBStore
from rdflib.plugins.sparql import prepareQuery
from google.appengine.api import search

_DOCUMENTS = '''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX sepake: <http://dot.rural/sepake/>
PREFIX sepakemetrics: <http://dot.rural/sepake/metrics/>
SELECT ?sepakeuri ?label ?htmlDescription (COUNT(*) AS ?rank)
WHERE {
    ?sepakeuri rdfs:label ?label .
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
        self._offset = 0
        self._more = True

    def __iter__(self):
        while self._more:
            index_now = self._graph.query(_DOCUMENTS + 'LIMIT 200 OFFSET {}'.format(self._offset))
            self._more = len(index_now) == 200
            self._offset += 200
            documents = [_document_from_sparql_result(doc.asdict()) for doc in index_now]
            self._index.put(documents)
            yield len(index_now)

