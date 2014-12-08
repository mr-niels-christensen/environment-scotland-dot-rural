'''
Created on 20 Oct 2014


@author: Niels Christensen

'''

from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import FOAF, XSD, Namespace
from dotruralsepake.ontology import SEPAKE, PROV
from rdflib import RDF, RDFS, Graph
from dotruralsepake.xml_to_rdf import XMLGraph
import urllib2
import logging

def university_of_aberdeen():
    xml_input = urllib2.urlopen('http://pure.abdn.ac.uk:8080/ws/rest/getprojectrequest?rendering=xml_long', timeout=20)
    return PureGraph(xml_input)

class PureGraph(Graph):
    def __init__(self, fileob):
        super(PureGraph, self).__init__()
        xml_as_rdf = _slimmed_xml_as_rdf(fileob)
        self += xml_as_rdf.query(_CONSTRUCT_PROJECT)
        if len(self) == 0:
            raise Exception('No PURE project in the given data')
        self += xml_as_rdf.query(_CONSTRUCT_PEOPLE)

def _slimmed_xml_as_rdf(fileob):
    return XMLGraph(fileob, 
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
                               'extensions-core' : 'http://atira.dk/schemas/pure4/model/core/extensions/stable'})
_NS = dict(xsd = XSD,
           rdf = RDF, 
           rdfs = RDFS, 
           prov = PROV, 
           foaf = FOAF,
           sepake = SEPAKE,
           core = Namespace('http://atira.dk/schemas/pure4/model/core/stable#'),
           project = Namespace('http://atira.dk/schemas/pure4/model/template/abstractproject/stable#'),
           extensionscore = Namespace('http://atira.dk/schemas/pure4/model/core/extensions/stable#'),
           organisationtemplate = Namespace('http://atira.dk/schemas/pure4/model/template/abstractorganisation/stable#'),
           persontemplate = Namespace('http://atira.dk/schemas/pure4/model/template/abstractperson/stable#'),
           )

def _prep(query):
    return prepareQuery(query, initNs = _NS)

logging.debug('Preparing queries for PURE data processing - this may take a while...')

_CONSTRUCT_PEOPLE = _prep('''
CONSTRUCT {
    ?personuri rdf:type        sepake:PurePerson .
    ?personuri prov:memberOf   ?projecturi .
    ?projecturi  prov:hadMember  ?personuri .
    ?personuri foaf:givenName  ?givenName .
    ?personuri foaf:familyName ?familyName .
}
WHERE {
    ?wrapper persontemplate:person ?person .
    ?person  persontemplate:uuid ?personuuid .
    ?person  persontemplate:name/core:firstName/rdf:value ?givenName .
    ?person  persontemplate:name/core:lastName /rdf:value ?familyName .
    ?wrapper (^persontemplate:participantAssociation) / (^project:persons) / core:uuid ?projectuuid .
    BIND ( URI ( CONCAT (str ( sepake:PurePerson ), "#", ENCODE_FOR_URI( ?personuuid ) ) ) AS ?personuri )
    BIND ( URI ( CONCAT (str ( sepake:PureProject ), "#", ENCODE_FOR_URI( ?projectuuid ) ) ) AS ?projecturi )
}
''')

_CONSTRUCT_PROJECT = _prep('''
CONSTRUCT {
    ?projecturi rdf:type sepake:PureProject .
    ?projecturi rdfs:label ?title .
    ?projecturi sepake:htmlDescription ?description .
    ?projecturi foaf:homepage ?homepage .
    ?projecturi prov:startedAtTime ?startdate .
    ?projecturi prov:endedAtTime ?enddate .
    ?projecturi sepake:ownedBy ?depturi .
    ?depturi    sepake:owns ?projecturi .
    ?depturi    rdf:type sepake:PureDepartment .
    ?depturi    rdfs:label ?deptname .
    ?depturi    foaf:homepage ?depthomepage .
}
WHERE {
    ?coreresult core:content ?corecontent .
    ?corecontent core:uuid ?projectuuid .
    ?corecontent project:title/core:localizedString/rdf:value ?title .
    OPTIONAL { ?corecontent project:description/core:localizedString/rdf:value ?description } .
    OPTIONAL { ?corecontent project:projectURL/rdf:value ?projectURL .
               BIND ( IF ( CONTAINS ( ?projectURL, "://" ), ?projectURL, CONCAT ( "http://", ?projectURL ) ) AS ?amendedURL )
               BIND ( URI ( ?amendedURL ) AS ?homepage )
    } .
    ?corecontent project:startFinishDate/extensionscore:startDate/rdf:value ?startdatestr .
    ?corecontent project:startFinishDate/extensionscore:endDate/rdf:value ?enddatestr .
    ?corecontent project:owner ?dept .
    ?dept        project:uuid ?deptuuid .
    ?dept        organisationtemplate:name/core:localizedString/rdf:value ?deptname .
    ?dept        core:portalUrl/rdf:value ?depthomepagestr
    BIND ( URI ( CONCAT (str ( sepake:PureProject ), "#", ENCODE_FOR_URI( ?projectuuid ) ) ) AS ?projecturi )
    BIND ( URI ( CONCAT (str ( sepake:PureDepartment ), "#", ENCODE_FOR_URI( ?deptuuid ) ) ) AS ?depturi )
    BIND ( URI ( ?depthomepagestr ) AS ?depthomepage )
    BIND ( STRDT ( ?startdatestr, xsd:date ) AS ?startdate )
    BIND ( STRDT ( ?enddatestr, xsd:date ) AS ?enddate )
}
''')

logging.debug('Done preparing queries for PURE data processing.')

