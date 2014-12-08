'''
Created on 4 Dec 2014

@author: Niels Christensen
'''
from dotruralsepake.rdf.xml_to_rdf import XMLGraph
import urllib2
import logging
from rdflib.plugins.sparql import prepareQuery

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
    ?sepakeuri sepake:wasDetailedByCode sepakecode:PureRestPublication .
    ?sepakeuri sepake:wasDetailedByData ?pureurl .
    FILTER NOT EXISTS {?sepakeuri sepake:wasDetailedAtTime ?sometime}
}
LIMIT 20
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

class PureRestPublicationHarvester(object):
    def __init__(self, graph):
        self._graph = graph
        self._queries = [prepareQuery(q) for q in _CONSTRUCTS]
    
    def __iter__(self):
        tasks = [task for task in self._graph.query(_TASKS)] #Minimize synchronization effects
        no_tasks = len(tasks)
        logging.debug('{} tasks found'.format(no_tasks))
        current_task = 0
        for task in tasks:
            current_task += 1
            logging.debug('Task {} of {}'.format(current_task, no_tasks))
            xml_input = urllib2.urlopen(task['pureurl'], timeout=20)
            page = XMLGraph(xml_input)
            for query in _CONSTRUCTS:
                yield page.query(query, initBindings = {'sepakeuri' : task['sepakeuri']})
            
