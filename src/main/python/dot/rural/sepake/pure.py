'''
Created on 20 Oct 2014


@author: Niels Christensen

'''

from dot.rural.sepake.sparql_utils import expand_and_parse
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import FOAF, XSD
from dot.rural.sepake.ontology import SEPAKE, PROV
from rdflib import RDF, RDFS

_NS = dict(xsd = XSD,
           rdf = RDF, 
           rdfs = RDFS, 
           prov = PROV, 
           foaf = FOAF,
           sepake = SEPAKE)

def _prep(query):
    return prepareQuery(query, initNs = _NS)

CONSTRUCT_PROJECT = _prep('''
CONSTRUCT {
    ?projecturi rdf:type sepake:PureProject .
}
WHERE {
    ?coreresult <http://atira.dk/schemas/pure4/model/core/stable#content> ?corecontent .
    ?corecontent <http://atira.dk/schemas/pure4/model/core/stable#uuid> ?uuid .
    BIND (URI(CONCAT(str(sepake:PureProject), "#", ENCODE_FOR_URI(?uuid))) AS ?projecturi)
}
''')
