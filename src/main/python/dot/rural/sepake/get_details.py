'''
Created on 4 Dec 2014

@author: Niels Christensen
'''
from dot.rural.sepake.xml_to_rdf import XMLGraph
import urllib2

_PREFIXES = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX sepake: <http://dot.rural/sepake/>
PREFIX sepake: <http://dot.rural/sepake/>
PREFIX sepakecode: <http://dot.rural/sepake/code>
PREFIX prov: <http://www.w3.org/ns/prov/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX publication-base_uk_hash: <http://atira.dk/schemas/pure4/model/template/abstractpublication/stable#>
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

_CONSTRUCT_PUBLICATION = _PREFIXES + '''
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
'''

class PureRestPublicationHarvester(object):
    def __init__(self, graph):
        self._graph = graph
        self._more = True
    
    def __iter__(self):
        while (self._more):
            yield self._next()

    def _next(self):
        rows = list(self._graph.query(_TASKS))
        if len(rows) == 0:
            self._more = False
        for row in rows:
            xml_input = urllib2.urlopen(row['pureurl'], timeout=20)
            page = XMLGraph(xml_input)
            for triple in page.query(_CONSTRUCT_PUBLICATION, initBindings = {'sepakeuri' : row['sepakeuri']}):
                yield triple
            
