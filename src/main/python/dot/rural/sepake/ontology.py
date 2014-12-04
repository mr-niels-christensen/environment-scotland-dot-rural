'''
Created on 16 Sep 2014

@author: s05nc4
'''

from rdflib import Graph, Namespace, RDFS, URIRef
from rdflib.namespace import FOAF
from ns_utils import RDF_NAME, namespace

@namespace('http://dot.rural/sepake', separator = '/')
class SEPAKE(object):
    UKEOFActivity     = RDF_NAME
    UKEOFOrganisation = RDF_NAME
    PureProject       = RDF_NAME
    PureDepartment    = RDF_NAME
    PurePublication   = RDF_NAME
    PurePerson        = RDF_NAME
    owns              = RDF_NAME
    ownedBy           = RDF_NAME
    htmlDescription   = RDF_NAME
    wasDetailedByData = RDF_NAME
    wasDetailedByCode = RDF_NAME
    wasDetailedAtTime = RDF_NAME
    
    
@namespace('http://www.w3.org/ns/prov')
class PROV(object):
    Activity        = RDF_NAME
    Organization    = RDF_NAME
    Person          = RDF_NAME
    startedAtTime   = RDF_NAME
    endedAtTime     = RDF_NAME
    wasInfluencedBy = RDF_NAME
    memberOf        = RDF_NAME
    hadMember       = RDF_NAME
    generatedAtTime = RDF_NAME

class SEPAKEOntologyGraph(Graph):
    '''Class for creating RDF triples for this project's ontology.
    '''
    def __init__(self):
        super(SEPAKEOntologyGraph, self).__init__()
        self.add((SEPAKE.PureProject, RDFS.subClassOf, PROV.Organization))
        self.add((SEPAKE.PureProject, RDFS.subClassOf, FOAF.Organization))
        self.add((SEPAKE.PureProject, RDFS.subClassOf, PROV.Activity))
        self.add((SEPAKE.PureDepartment, RDFS.subClassOf, PROV.Organization))
        self.add((SEPAKE.PureDepartment, RDFS.subClassOf, FOAF.Organization))
        self.add((SEPAKE.PurePerson, RDFS.subClassOf, PROV.Person))
        self.add((SEPAKE.PurePerson, RDFS.subClassOf, FOAF.Person))
        self.add((SEPAKE.UKEOFActivity, RDFS.subClassOf, PROV.Activity))
        self.add((SEPAKE.UKEOFOrganisation, RDFS.subClassOf, PROV.Organization))
        self.add((SEPAKE.UKEOFOrganisation, RDFS.subClassOf, FOAF.Organization))
        self.add((SEPAKE.wasDetailedByData, RDFS.subPropertyOf, PROV.wasInfluencedBy))
        self.add((SEPAKE.wasDetailedByCode, RDFS.subPropertyOf, PROV.wasInfluencedBy))
        self.add((SEPAKE.wasDetailedAtTime, RDFS.subPropertyOf, PROV.generatedAtTime))
        
