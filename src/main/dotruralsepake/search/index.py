'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph, Literal
from rdflib_appengine.ndbstore import NDBStore
from rdflib.plugins.sparql import prepareQuery
from google.appengine.api import search
import logging
from dotruralsepake.store import connect
from dotruralsepake.rdf.utils import prepareQuery

_DOCUMENTS = '''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX sepake: <http://dot.rural/sepake/>
PREFIX sepakemetrics: <http://dot.rural/sepake/metrics/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?sepakeuri ?label ?htmlDescription ?publicationYear ?logo (COUNT(*) AS ?rank)
WHERE {
    { ?sepakeuri rdfs:label ?label .
       FILTER (STRENDS(STR(?sepakeuri), ?suffix))
    } .
    OPTIONAL { ?sepakeuri sepake:htmlDescription ?htmlDescription } .
    OPTIONAL { ?sepakeuri sepake:publicationYear ?publicationYear } .
    OPTIONAL { ?sepakeuri prov:wasDerivedFrom / foaf:logo ?logo } .
    OPTIONAL { ?sepakeuri sepakemetrics:focushit []} . 
}
GROUP BY ?sepakeuri
'''

def _document_from_sparql_result(sparql_result):
    fields = [search.HtmlField(name='label', value=sparql_result['label'])]
    facets = []
    if 'htmlDescription' in sparql_result:
        fields.append(search.HtmlField(name='description', value=sparql_result['htmlDescription']))
    if 'publicationYear' in sparql_result: # for papers
        fields.append(search.TextField(name='publicationYear', value=sparql_result['publicationYear']))
        facets.append(search.AtomFacet(name='publicationYear', value=sparql_result['publicationYear']))
    if 'logo' in sparql_result:
        fields.append(search.AtomField(name='logo', value=sparql_result['logo']))
    return search.Document(doc_id = sparql_result['sepakeuri'], 
                           fields = fields,
                           facets = facets,
                           rank = sparql_result['rank'].value)
    
class Indexer(object):
    def __init__(self, graphid):
        self._index = search.Index(name = graphid)
        self._graph = Graph(store = connect(identifier = graphid))
        
    def __iter__(self):
        #Step 1: Delete documents in index, in batches of 100
        while True:
            # Get up to 100 document ids
            document_ids = [document.doc_id
                            for document in self._index.get_range(ids_only=True)]
            if not document_ids:
                break
            # Delete the documents for the given ids from the Index.
            self._index.delete(document_ids)
        #Step 2: Add documents from self._graph, in 16 batches
        for suffix in [str(i) for i in range(10)] + [chr(i) for i in range(ord('a'), ord('g'))]:#Each of the 16 hex digits
            index_now = self._graph.query(prepareQuery(_DOCUMENTS.replace('?suffix', '"{}"'.format(suffix))))#initBindings do not work with FILTER
            dicts = [doc.asdict() for doc in index_now]
            documents = [_document_from_sparql_result(d) for d in dicts if 'label' in d]
            self._index.put(documents)
            yield len(documents)
