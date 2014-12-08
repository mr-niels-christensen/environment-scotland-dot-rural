'''
Created on 3 Oct 2014

@author: s05nc4
'''
import unittest
import StringIO
from dotruralsepake.rdf.xml_to_rdf import XMLGraph
from rdflib.term import URIRef, Literal

EXAMPLE_OAI = '''<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
  <responseDate>2014-10-15T16:17:58Z</responseDate>
  <request verb="ListRecords">https://pure.someuni.ac.uk:8888/ws/oai</request>
  <ListRecords>
    <record>
      <header>
        <identifier>oai:pure.atira.dk:persons/c5f5cc43-8667-44f6-926f-c9d04df2e033</identifier>
        <datestamp>2013-11-08T07:31:08Z</datestamp>
        <setSpec>persons:all</setSpec>
      </header>
      <metadata>
        <oai_dc:dc xmlns:ns2="http://purl.org/dc/terms/" xmlns="http://purl.org/dc/elements/1.1/" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/">
          <identifier>http://pure.someuni.ac.uk:8888/portal/en/persons/n-christensen(c5f5cc43-8667-44f6-926f-c9d04df2e033).html</identifier>
          <title>Christensen, N</title>
        </oai_dc:dc>
      </metadata>
    </record>
    <record>
      <header>
        <identifier>oai:pure.atira.dk:persons/956194cf-8772-4d30-b536-e47b035683db</identifier>
        <datestamp>2013-11-28T07:34:11Z</datestamp>
        <setSpec>persons:all</setSpec>
      </header>
      <metadata>
        <oai_dc:dc xmlns:ns2="http://purl.org/dc/terms/" xmlns="http://purl.org/dc/elements/1.1/" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/">
          <identifier>http://pure.someuni.ac.uk:8888/portal/en/persons/edoardo-pignotti(956194cf-8772-4d30-b536-e47b035683db).html</identifier>
          <title>Pignotti, Edoardo</title>
        </oai_dc:dc>
      </metadata>
    </record>
    <resumptionToken cursor="0" completeListSize="24220">oai_dc/24220/42662723/100/0/2738/persons:all/x/x</resumptionToken>
  </ListRecords>
</OAI-PMH>
'''
EXAMPLE_AB = '''<?xml version="1.0" encoding="UTF-8"?>
<A a="test">
  <A>
    <A></A>
    <B></B>
    <C></C>
  </A>
  <B>
    <A>1</A>    
  </B>
  <C>
  </C>
</A>
'''

#TODO: Test deleting nodes

class Test(unittest.TestCase):
    def testAB(self):
        g = XMLGraph(StringIO.StringIO(EXAMPLE_AB))
        A = g.value(subject = URIRef(''), predicate = URIRef('#A'), any = False)
        self.assertEquals(URIRef('#A'), A)
        self.assertEquals(Literal('test'), g.value(subject = A, predicate = URIRef('#a'), any = False))
        for letter in 'ABC':
            self.assertEquals(URIRef('#A/' + letter), 
                              g.value(subject = A, 
                                      predicate = URIRef('#' + letter), 
                                      any = False))
        self.assertEquals(URIRef('#A/A/C'), g.value(subject = URIRef(''), 
                                                    predicate = URIRef('#A') / URIRef('#A') / URIRef('#C'), 
                                                    any = False))
        self.assertEquals(Literal('1'), g.value(subject = URIRef('#A/B/A'), 
                                                predicate = URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#value'),
                                                any = False))
                   
    def testOAI(self):
        g = XMLGraph(StringIO.StringIO(EXAMPLE_OAI))
        metadata_nodes = list(g.objects(URIRef('#OAI-PMH/ListRecords'), 
                                        predicate = URIRef('http://www.openarchives.org/OAI/2.0/#record') 
                                        / URIRef('http://www.openarchives.org/OAI/2.0/#metadata')))
        self.assertEquals(2, len(metadata_nodes))
        titles = [g.value(subject = node, 
                          predicate = URIRef('http://www.openarchives.org/OAI/2.0/oai_dc/#dc')
                                      / URIRef('http://purl.org/dc/elements/1.1/#title')
                                      / URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#value'), 
                          any = False)
                  for node in metadata_nodes]
        self.assertEquals(set(Literal(name) for name in ['Christensen, N', 'Pignotti, Edoardo']),
                          set(titles))
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()