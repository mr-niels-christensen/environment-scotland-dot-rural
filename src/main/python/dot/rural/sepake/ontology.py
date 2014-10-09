'''
Created on 16 Sep 2014

@author: s05nc4
'''

from rdflib import Graph, Namespace, RDFS, URIRef
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib.namespace import FOAF, ClosedNamespace
from ns_utils import RDF_NAME, namespace

ONTOLOGY = ClosedNamespace(uri = URIRef('http://dot.rural/sepake/'),
                         terms = ["PureProject", 
                                  "PureDepartment", 
                                  "PurePerson", 
                                  "UKEOFActivity", 
                                  "UKEOFOrganisation", 
                                  "CrawlOperation",
                                  "contextualStatementOf",
                                  "owns",
                                  "htmlDescription",
                                  ])

@namespace('http://www.w3.org/ns/prov')
class PROV(object):
    Activity = RDF_NAME
    Organization = RDF_NAME
    Person = RDF_NAME
    startedAtTime = RDF_NAME
    endedAtTime = RDF_NAME
    wasDerivedFrom = RDF_NAME

class OntologyGraph(Graph):
    '''Class for creating RDF triples for this project's ontology.
    '''
    def __init__(self):
        super(OntologyGraph, self).__init__()
        self.add((ONTOLOGY.PureProject, RDFS.subClassOf, PROV.Organization))
        self.add((ONTOLOGY.PureProject, RDFS.subClassOf, FOAF.Organization))
        self.add((ONTOLOGY.PureProject, RDFS.subClassOf, PROV.Activity))
        self.add((ONTOLOGY.PureDepartment, RDFS.subClassOf, PROV.Organization))
        self.add((ONTOLOGY.PureDepartment, RDFS.subClassOf, FOAF.Organization))
        self.add((ONTOLOGY.PurePerson, RDFS.subClassOf, PROV.Person))
        self.add((ONTOLOGY.PurePerson, RDFS.subClassOf, FOAF.Person))
        self.add((ONTOLOGY.UKEOFActivity, RDFS.subClassOf, PROV.Activity))
        self.add((ONTOLOGY.UKEOFOrganisation, RDFS.subClassOf, PROV.Organization))
        self.add((ONTOLOGY.UKEOFOrganisation, RDFS.subClassOf, FOAF.Organization))
        self.add((ONTOLOGY.CrawlOperation, RDFS.subClassOf, PROV.Activity))
        self.add((ONTOLOGY.contextualStatementOf, RDFS.subPropertyOf, RDFS.subPropertyOf))
        
if __name__ == '__main__':
    ont = OntologyGraph()
    print ont.serialize(format='turtle')
    remote = SPARQLUpdateStore(context_aware = False)
    remote.open(("http://localhost:3030/ds/query", "http://localhost:3030/ds/update"))
    #TODO Use += but it does not seem to work unless context_aware...which does not seem to work with Fuseki
    print 'Flushing...'
    for triple in ont:
        print '.',
        remote.add(triple)
    print 'Flushed'
    