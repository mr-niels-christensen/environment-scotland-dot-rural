'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
from rdflib_appengine.ndbstore import NDBStore
from google.appengine.api import search

def _dictify(scored_document):
    result = {'uri' : scored_document.doc_id,
              'label' : scored_document.field('label').value,
              }
    try:
        result['description'] = scored_document.field('description').value
        if len(result['description']) > 500:
            result['description'] = result['description'][:497] + "..."
    except Exception:
        pass
    return result

def search_graph(graphid, query, cursor_websafe = None):
    gae_query = search.Query(query_string=query, 
                             options = search.QueryOptions(cursor = search.Cursor(web_safe_string = cursor_websafe),
                                                           limit = 10))
    result = search.Index(name = graphid).search(gae_query)
    next_cursor_websafe = result.cursor.web_safe_string if result.cursor is not None else None
    return {'query' : query,
            'cursor_websafe' : cursor_websafe,
            'number_found' : result.number_found,
            'next_cursor_websafe' : next_cursor_websafe,
            'results' : [_dictify(scored_document) for scored_document in result.results],
            }
 
