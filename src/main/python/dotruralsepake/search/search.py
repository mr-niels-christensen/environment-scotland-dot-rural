'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
from rdflib_appengine.ndbstore import NDBStore
from google.appengine.api import search
import logging

def _dictify(scored_document):
    result = {'uri' : scored_document.doc_id,
              'label' : scored_document.field('label').value,
              }
    try:
        result['description'] = scored_document.field('description').value
    except Exception:
        pass
    return result

def search_graph(graphid, query, cursor_websafe = None):
    gae_query = search.Query(query_string=query)
    result = search.Index(name = graphid).search(gae_query)
    logging.debug(result)
    return {'number_found' : result.number_found,
            'cursor_websafe' : None,
            'results' : [_dictify(scored_document) for scored_document in result.results],
            }
 
