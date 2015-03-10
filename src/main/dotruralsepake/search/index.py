'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
from rdflib import Graph, Literal, RDFS
from rdflib.namespace import FOAF
from rdflib_appengine.ndbstore import NDBStore
from rdflib.plugins.sparql import prepareQuery
from google.appengine.api import search
import logging
from dotruralsepake.store import connect
from dotruralsepake.rdf.utils import prepareQuery
from dotruralsepake.rdf.ontology import SEPAKE, SEPAKEMETRICS, PROV
from itertools import izip_longest
from collections import Counter

def _chunk(n, iterable):
    args = [iter(iterable)] * n
    return izip_longest(fillvalue = None, *args)

def _document_from_sparql_result(sparql_result):
    fields = [search.HtmlField(name='label', value=sparql_result['label'])]

    if 'htmlDescription' in sparql_result:
        fields.append(search.HtmlField(name='description', value=sparql_result['htmlDescription']))
    if 'logo' in sparql_result:
        fields.append(search.AtomField(name='logo', value=sparql_result['logo']))
    return search.Document(doc_id = sparql_result['sepakeuri'], 
                           fields = fields,
                           rank = sparql_result['rank'])
    
class Indexer(object):
    def __init__(self, graphid):
        self._index = search.Index(name = graphid)
        self._graph = Graph(store = connect(identifier = graphid))
        self._hits = Counter()
        for (s, o) in self._graph.subject_objects(SEPAKEMETRICS.focushit):
            self._hits[s] += 1
    
    def _dict_to_gae(self, d):
        fields = [search.HtmlField(name='label', value=d['label'])]
        fields.append(search.HtmlField(name='description', value=d['htmlDescription']))
        if 'logo' in d:
            fields.append(search.AtomField(name='logo', value=d['logo']))
        return search.Document(doc_id = d['sepakeuri'], 
                               fields = fields,
                               rank = self._hits[d['sepakeuri']])

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
        #Step 2: Add documents from self._graph, in batches of 200
        for chunk in _chunk(200, self._graph.subject_objects(SEPAKE.htmlDescription)):
            dicts = []
            for pair in chunk:
                if pair is not None:
                    (s, o) = pair
                    dicts.append({'sepakeuri':s, 'htmlDescription':o})
            for d in dicts:
                logo = self._graph.value(subject = d['sepakeuri'], predicate = PROV.wasDerivedFrom / FOAF.logo)
                if logo is not None:
                    d['logo'] = logo
            for d in dicts:
                d['label'] = self._graph.value(subject = d['sepakeuri'], predicate = RDFS.label, default = '')
            documents = [self._dict_to_gae(d) for d in dicts]
            self._index.put(documents)
            yield len(documents)
