'''
Created on 4 Dec 2014

@author: Niels Christensen
'''
from dotruralsepake.rdf.xml_to_rdf import XMLGraph
import urllib2
import logging
from dotruralsepake.rdf.utils import prepareQuery

_PREFIXES = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX sepake: <http://dot.rural/sepake/>
PREFIX sepake: <http://dot.rural/sepake/>
PREFIX sepakecode: <http://dot.rural/sepake/code>
PREFIX prov: <http://www.w3.org/ns/prov/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX publication-base_uk_hash: <http://atira.dk/schemas/pure4/model/template/abstractpublication/stable#>
PREFIX person-template_hash: <http://atira.dk/schemas/pure4/model/template/abstractperson/stable#>
PREFIX core_hash: <http://atira.dk/schemas/pure4/model/core/stable#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
'''

_TASKS = _PREFIXES + '''
SELECT ?sepakeuri ?pureurl
WHERE {
    { ?sepakeuri sepake:wasDetailedByCode sepakecode:PureRestPublication .
      FILTER NOT EXISTS {?sepakeuri sepake:wasDetailedAtTime ?sometime}
    } .
    ?sepakeuri sepake:wasDetailedByData ?pureurl .
}
LIMIT 30
'''

_CONSTRUCTS = list()
_CONSTRUCTS.append(_PREFIXES + '''
CONSTRUCT {
    ?sepakeuri rdf:type sepake:PurePublication .
    ?sepakeuri dc:title ?title .
    ?sepakeuri rdfs:label ?title .
    ?sepakeuri sepake:wasDetailedAtTime ?now .
}
WHERE {
    [] publication-base_uk_hash:includedOnStaffPages / rdf:value "true" .
    [] publication-base_uk_hash:title                / rdf:value ?title .
    BIND ( ( ?sepakeuri ) AS ?sepakeuri )
    BIND ( ( NOW() ) AS ?now )
}
''')
_CONSTRUCTS.append(_PREFIXES + '''
CONSTRUCT {
    ?personuri rdf:type sepake:PurePerson .
    ?sepakeuri sepake:hasAuthor ?personuri .
    ?personuri sepake:authorOf ?sepakeuri .
    ?personuri foaf:givenName  ?givenName .
    ?personuri foaf:familyName ?familyName .
    ?personuri rdfs:label ?label .
    ?personuri foaf:homepage ?homepage .
}
WHERE {
    [] publication-base_uk_hash:includedOnStaffPages / rdf:value "true" .
    ?person person-template_hash:uuid ?personuuid .
    ?person  person-template_hash:name/core_hash:firstName/rdf:value ?givenName .
    ?person  person-template_hash:name/core_hash:lastName /rdf:value ?familyName .
    ?person  core_hash:portalUrl/rdf:value ?homepage .
    BIND ( ( ?sepakeuri ) AS ?sepakeuri )
    BIND ( URI ( CONCAT (str ( sepake:PurePerson ), "#", ENCODE_FOR_URI( ?personuuid ) ) ) AS ?personuri )
    BIND ( CONCAT ( ?familyName, ", ", ?givenName ) AS ?label )
}
''')
_CONSTRUCTS.append(_PREFIXES + '''
CONSTRUCT {
    ?sepakeuri foaf:homepage ?homepage .
}
WHERE {
    [] publication-base_uk_hash:includedOnStaffPages / rdf:value "true" .
    { {[] core_hash:doi/core_hash:doi/rdf:value ?homepage}
      UNION
      {[] core_hash:result/core_hash:content/core_hash:portalUrl/rdf:value ?homepage}
    }
    BIND ( ( ?sepakeuri ) AS ?sepakeuri )
}
''')

def details_iterator_generator(graph):
    tasks = [task for task in graph.query(prepareQuery(_TASKS))]
    if len(tasks) > 0:
        return PureRESTPublicationHarvester(graph, tasks)
    else:
        return None
    
class PureRESTPublicationHarvester(object):
    def __init__(self, graph, tasks, verbose = False):
        self._graph = graph
        self._tasks = tasks
        self._queries = [prepareQuery(q) for q in _CONSTRUCTS]
        self._verbose = verbose
        
    def __iter__(self):
        no_tasks = len(self._tasks)
        logging.debug('{} detail URLs found'.format(no_tasks))
        current_task = 0
        for task in self._tasks:
            current_task += 1
            if self._verbose:
                logging.debug('Task {} of {}: {}'.format(current_task, no_tasks, task['pureurl']))
            xml_input = urllib2.urlopen(task['pureurl'], timeout=20)
            page = XMLGraph(xml_input)
            for query in self._queries:
                yield page.query(query, initBindings = {'sepakeuri' : task['sepakeuri']})
            
