'''
Created on 16 Sep 2014

@author: s05nc4
'''

from rdflib import Graph, Literal,  Namespace, RDF, RDFS, URIRef
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib.namespace import FOAF

SEPAKE = Namespace('http://dot.rural/sepake/')
PROV  = Namespace('http://www.w3.org/ns/prov#')


class OntologyLoader(Graph):
    '''Class for creating RDF triples for this project's ontology.
    '''
    def __init__(self):
        super(OntologyLoader, self).__init__()
        self.add((SEPAKE.PureProject, RDFS.subClassOf, PROV.Organization))
        self.add((SEPAKE.PureProject, RDFS.subClassOf, FOAF.Organization))
        self.add((SEPAKE.PureProject, RDFS.subClassOf, PROV.Activity))
        self.add((SEPAKE.PureDepartment, RDFS.subClassOf, PROV.Organization))
        self.add((SEPAKE.PureDepartment, RDFS.subClassOf, FOAF.Organization))
        self.add((SEPAKE.PurePerson, RDFS.subClassOf, PROV.Person))
        self.add((SEPAKE.PurePerson, RDFS.subClassOf, FOAF.Person))
        self.add((SEPAKE.UKEOFActivity, RDFS.subClassOf, PROV.Activity))
        
        
    def flush(self, other):
        #TODO Use += but it does not seem to work unless context_aware...which does not seem to work with Fuseki
        print 'Flushing...'
        for triple in self:
            print '.',
            other.add(triple)
        print 'Flushed'

if __name__ == '__main__':
    ont = OntologyLoader()
    print ont.serialize(format='turtle')
    #remote = SPARQLUpdateStore(context_aware = False)
    #remote.open(("http://localhost:3030/ds/query", "http://localhost:3030/ds/update"))
    #ont.flush(remote)
    