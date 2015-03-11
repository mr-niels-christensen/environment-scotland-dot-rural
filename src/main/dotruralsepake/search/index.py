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
    '''Divides the given iterable into chunks of length exactly n,
       filling the last chunk with None values as required.
    '''
    args = [iter(iterable)] * n
    return izip_longest(fillvalue = None, *args)

class Indexer(object):
    '''An iterable object. When iterated it will delete the search index,
       then rebuild it from the given graph. The iterated values are counts
       of indexed documents.
    '''
    def __init__(self, graphid):
        self._index = search.Index(name = graphid)
        self._graph = Graph(store = connect(identifier = graphid))
        #Preparation: Find the number of hits for every item
        self._hits = Counter()
        for (s, o) in self._graph.subject_objects(SEPAKEMETRICS.focushit):
            self._hits[s] += 1
    
    def _dict_to_gae(self, d):
        '''
        '''
        fields = [search.HtmlField(name='label', value=d['label'])]
        fields.append(search.HtmlField(name='description', value=d['htmlDescription']))
        if 'logo' in d:
            fields.append(search.AtomField(name='logo', value=d['logo']))
        return search.Document(doc_id = d['sepakeuri'], 
                               fields = fields,
                               rank = self._hits[d['sepakeuri']])

    def _delete_index(self):
        '''Delete documents in index, in batches of 100
        '''
        while True:
            # Get up to 100 document ids
            document_ids = [document.doc_id
                            for document in self._index.get_range(ids_only=True)]
            if not document_ids:
                break
            # Delete the documents for the given ids from the Index.
            self._index.delete(document_ids)

    def __iter__(self):
        #Step 1: Delete index
        self._delete_index()
        #Step 2: Add documents from self._graph, in batches of 200
        for chunk in _chunk(200, self._graph.subject_objects(SEPAKE.htmlDescription)):
            pairs = [pair for pair in chunk if pair is not None]
            documents = self._search_documents_from_pairs(pairs)
            self._index.put(documents)
            yield len(documents)

    def _search_documents_from_pairs(self, pairs):
        '''Adds data one field at a time to avoid "page switching"
           causing very long running times.
           @param pairs A large tuple of (URI, htmlDescription) pairs.
        '''
        id_to_doc = dict()
        #Add ID, rank (number of hits), and description:
        for (s, o) in pairs:
            id_to_doc[s] = search.Document(doc_id = s,
                                           rank = self._hits[s])
            id_to_doc[s].fields.append(search.HtmlField(name='description', value = o))
        #Add logo if possible
        for (doc_id, doc) in id_to_doc.iteritems():
            logo = self._graph.value(subject = doc_id, predicate = PROV.wasDerivedFrom / FOAF.logo)
            if logo is not None:
                id_to_doc[doc_id].fields.append(search.AtomField(name='logo', value=logo))
        #Add label
        for (doc_id, doc) in id_to_doc.iteritems():
            label = self._graph.value(subject = doc_id, predicate = RDFS.label, default = '')
            id_to_doc[doc_id].fields.append(search.HtmlField(name='label', value=label))
        #Add publicationYear if possible
        for (doc_id, doc) in id_to_doc.iteritems():
            year = self._graph.value(subject = doc_id, predicate = SEPAKE.publicationYear)
            if year is not None:
                id_to_doc[doc_id].fields.append(search.TextField(name='publicationYear', value=year))
                id_to_doc[doc_id].facets.append(search.AtomFacet(name='publicationYear', value=year))
        #Return the search.Documents as a list
        return id_to_doc.values()
