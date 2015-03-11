'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
from rdflib_appengine.ndbstore import NDBStore
from google.appengine.api import search
import logging

facetNames = ['publicationYear'];

def _dictify(scored_document):
    result = {'uri' : scored_document.doc_id,
              'label' : scored_document.field('label').value,
              'rank' : scored_document.rank,
              }
    try:
        result['description'] = scored_document.field('description').value
        if len(result['description']) > 500:
            result['description'] = result['description'][:497] + "..."
    except Exception:
        pass
    try:
        result['logo'] = scored_document.field('logo').value
    except Exception:
        pass
    return result
	
def _dictify_facet(facet):
    facet = {'label' : facet.label,
              'count' : facet.count,
              'refinement_token' : facet.refinement_token,
              }
    return facet

def search_graph(graphid, query, refinement_token = None, cursor_websafe = None):
    refinement_tokens = []
    if refinement_token is not None:
        refinement_tokens.append(refinement_token)
    gae_query = search.Query(query_string=query,
                             facet_refinements=refinement_tokens,
                             return_facets=facetNames,
                             options = search.QueryOptions(cursor = search.Cursor(web_safe_string = cursor_websafe),
                                                           limit = 10))
    result = search.Index(name = graphid).search(gae_query)
    facets = {}
    for facetResult in result.facets:
        facets[facetResult.name] = [_dictify_facet(facetValue) for facetValue in facetResult.values]
    next_cursor_websafe = result.cursor.web_safe_string if result.cursor is not None else None
    return {'query' : query,
            'cursor_websafe' : cursor_websafe,
            'number_found' : result.number_found,
            'next_cursor_websafe' : next_cursor_websafe,
			'facets' : facets,
            'results' : [_dictify(scored_document) for scored_document in result.results],
            }
 
