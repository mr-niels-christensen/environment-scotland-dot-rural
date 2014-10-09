'''
Created on 16 Sep 2014

@author: s05nc4
'''

from rdflib import Graph, Namespace, RDFS, URIRef
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib.namespace import FOAF, ClosedNamespace
from ns_utils import RDF_NAME, namespace

@namespace('http://dot.rural/sepake', separator = '/')
class SEPAKE(object):
    UKEOFActivity     = RDF_NAME
    UKEOFOrganisation = RDF_NAME
    PureProject       = RDF_NAME
    PureDepartment    = RDF_NAME
    PurePerson        = RDF_NAME
    owns              = RDF_NAME
    htmlDescription   = RDF_NAME
    
@namespace('http://www.w3.org/ns/prov')
class PROV(object):
    Activity       = RDF_NAME
    Organization   = RDF_NAME
    Person         = RDF_NAME
    startedAtTime  = RDF_NAME
    endedAtTime    = RDF_NAME
    wasDerivedFrom = RDF_NAME

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
        
if __name__ == '__main__':
    ont = SEPAKEOntologyGraph()
    print ont.serialize(format='turtle')
    remote = SPARQLUpdateStore(context_aware = False)
    remote.open(("http://localhost:3030/ds/query", "http://localhost:3030/ds/update"))
    #TODO Use += but it does not seem to work unless context_aware...which does not seem to work with Fuseki
    print 'Flushing...'
    for triple in ont:
        print '.',
        remote.add(triple)
    print 'Flushed'
    