'''
Created on 20 Oct 2014


@author: Niels Christensen

'''

from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import FOAF, XSD, Namespace
from dot.rural.sepake.ontology import SEPAKE, PROV
from rdflib import RDF, RDFS

_NS = dict(xsd = XSD,
           rdf = RDF, 
           rdfs = RDFS, 
           prov = PROV, 
           foaf = FOAF,
           sepake = SEPAKE,
           core = Namespace('http://atira.dk/schemas/pure4/model/core/stable#'),
           project = Namespace('http://atira.dk/schemas/pure4/model/template/abstractproject/stable#'))

def _prep(query):
    return prepareQuery(query, initNs = _NS)

CONSTRUCT_PROJECT = _prep('''
CONSTRUCT {
    ?projecturi rdf:type sepake:PureProject .
    ?projecturi rdfs:label ?title .
    ?projecturi sepake:htmlDescription ?description .
}
WHERE {
    ?coreresult core:content ?corecontent .
    ?corecontent core:uuid ?uuid .
    ?corecontent project:title/core:localizedString/rdf:value ?title .
    ?corecontent project:description/core:localizedString/rdf:value ?description .
    BIND (URI(CONCAT(str(sepake:PureProject), "#", ENCODE_FOR_URI(?uuid))) AS ?projecturi)
}
''')
