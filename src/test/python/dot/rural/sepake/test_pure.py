'''
Created on 20 Oct 2014

@author: s05nc4
'''
import unittest
from rdflib import RDF, RDFS, URIRef, Graph
from rdflib.namespace import FOAF
from dot.rural.sepake.ontology import SEPAKE, PROV
import datetime
from rdflib.term import Literal
from dot.rural.sepake.xml_to_rdf import XMLGraph
from dot.rural.sepake.pure import CONSTRUCT_PROJECT

class Test(unittest.TestCase):
    def testConstructProject(self):
        with open('src/main/resources/dot/rural/sepake/cli/search-projects-for-rural.xml') as f:
            x = XMLGraph(f, 
                         delete_nodes = ['stab:associatedPublications',
                                         'stab:associatedActivities',
                                         'stab:personsUK',
                                         'personstab:staffOrganisationAssociations',
                                         'person-template:nameVariants',
                                         'person-template:callName'], 
                         namespaces = {'stab' : 'http://atira.dk/schemas/pure4/model/base_uk/project/stable',
                                       'personstab' : 'http://atira.dk/schemas/pure4/model/base_uk/person/stable',
                                       'person-template' : 'http://atira.dk/schemas/pure4/model/template/abstractperson/stable'})
            g = Graph()
            g += x.query(CONSTRUCT_PROJECT)
            self.assertEquals(3, len(g))
            proj = URIRef(u'http://dot.rural/sepake/PureProject#e963d657-b41f-44eb-a85d-7639346b378d')
            self.assertEquals(SEPAKE.PureProject, g.value(proj, RDF.type, any = False))
            self.assertEquals(Literal('RURAL DIGITAL ECONOMY RESEARCH HUB'),
                              g.value(proj, RDFS.label, any = False))
            self.assertTrue(str(g.value(proj, SEPAKE.htmlDescription, any = False)).startswith('One of the three'))
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()