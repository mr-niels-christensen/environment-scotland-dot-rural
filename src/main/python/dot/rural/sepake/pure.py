'''
Created on 20 Oct 2014


@author: Niels Christensen

'''

from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import FOAF, XSD, Namespace
from dot.rural.sepake.ontology import SEPAKE, PROV
from rdflib import RDF, RDFS, Graph
from dot.rural.sepake.xml_to_rdf import XMLGraph

class PureGraph(Graph):
    def __init__(self, fileob):
        super(PureGraph, self).__init__()
        self += XMLGraph(fileob, 
                         delete_nodes = ['stab:associatedPublications',
                                         'stab:associatedActivities',
                                         'stab:personsUK',
                                         'personstab:staffOrganisationAssociations',
                                         'person-template:nameVariants',
                                         'person-template:callName',
                                         'person-template:email',
                                         'person-template:employeeId',
                                         'person-template:organisationAssociations',
                                         'person-template:personRole',
                                         'person-template:organisations',
                                         'organisation-template:association',
                                         'extensions-core:customField',], 
                         namespaces = {'stab' : 'http://atira.dk/schemas/pure4/model/base_uk/project/stable',
                                       'personstab' : 'http://atira.dk/schemas/pure4/model/base_uk/person/stable',
                                       'person-template' : 'http://atira.dk/schemas/pure4/model/template/abstractperson/stable',
                                       'organisation-template' : 'http://atira.dk/schemas/pure4/model/template/abstractorganisation/stable',
                                       'extensions-core' : 'http://atira.dk/schemas/pure4/model/core/extensions/stable'}).query(_CONSTRUCT_PROJECT)

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

_CONSTRUCT_PROJECT = _prep('''
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
