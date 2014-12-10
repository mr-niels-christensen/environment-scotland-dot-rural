'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
from rdflib_appengine.ndbstore import NDBStore
from google.appengine.api import search
import logging

query_options = search.QueryOptions(
    #ids_only = True,
    returned_fields =  ['label'],
    snippeted_fields = ['description'])

def search_graph(graphid, query, cursor_websafe = None):
    result = search.Index(name = graphid).search(search.Query(query_string=query, options=query_options))
    logging.debug(result)
    return {'number_found' : result.number_found,
            'cursor_websafe' : None,
            'results' : [{'uri' : scored_document.doc_id,
                          'label' : scored_document.label,
                          'snippet' : scored_document.expressions[0].value} for scored_document in result.results],
            }
 
