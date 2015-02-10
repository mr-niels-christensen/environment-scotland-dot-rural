'''
Created on 20 Oct 2014


@author: Niels Christensen

'''

from dotruralsepake.rdf.ontology import SEPAKECODE
import logging

def build_nerc_iterator_from_graph(graph):
	#TODO: Fix the user of SEPAKECODE namespace to always have a slash after 'code'
	return build_iterator_from_tasks(graph, 'http://dot.rural/sepake/codeNercRSS', lambda url : None)

def build_iterator_from_tasks(graph, codeURI, url_to_iterator_fun):
    try:
    	query = _TASK.replace('?codeURI', '<{}>'.format(codeURI))
    	result = graph.query(query)
        task = result.__iter__().next()
        logging.debug(task['pureurl'])
        return url_to_iterator_fun(task['pureurl'])
    except StopIteration:
        return None

_TASK = '''
PREFIX sepake: <http://dot.rural/sepake/>
PREFIX sepakecode: <http://dot.rural/sepake/code>
SELECT ?pureurl
WHERE {
    ?pureurl sepake:wasDetailedByCode ?codeURI .
    FILTER NOT EXISTS {?pureurl sepake:wasDetailedAtTime ?sometime}
}
LIMIT 1
'''