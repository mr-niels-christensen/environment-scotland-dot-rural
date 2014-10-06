'''
Created on 3 Oct 2014

@author: s05nc4
'''
import unittest
import StringIO
from dot.rural.sepake.csv_to_rdf import CSV, CsvGraph, PROV
from rdflib import RDF, RDFS, Literal

EXAMPLE = '''"A","B","C"
1,2,3
4,5,6
'''

ALL_CELLS_QUERY = '''
SELECT ?h ?v 
WHERE {{
    ?cell <{rdf.type}> <{csv.Cell}> .
    ?cell <{csv.fieldName}> ?h . 
    ?cell <{csv.fieldValue}> ?v}}
'''.format(csv = CSV, rdf = RDF, rdfs = RDFS)

STURCTURE_QUERY = '''
SELECT *
WHERE {{
    ?cell <{rdf.type}> <{csv.Cell}> .
    ?row <{rdfs.member}> ?cell . 
    ?row <{rdf.type}> <{csv.Row}>}} .
    ?file <{rdfs.member}> ?row . 
    ?file <{rdf.type}> <{csv.File}>}} .
    ?import <{prov.generated}> ?file . 
    ?import <{rdf.type}> <{prov.Activity}>}} .
'''.format(csv = CSV, rdf = RDF, rdfs = RDFS, prov = PROV)

def _pythonify(result_row):
    '''@param result_row Row from a query result, instance of rdflib.query.ResultRow 
    '''
    return tuple([v.toPython() for v in result_row])

class Test(unittest.TestCase):
    def setUp(self):
            self.g = CsvGraph()
            self.g.read(StringIO.StringIO(EXAMPLE))
    
    def _query(self, query):
            return [_pythonify(tupl) for tupl in self.g.query(query)]
        
    def testCells(self):
            g = CsvGraph()
            g.read(StringIO.StringIO(EXAMPLE))
            self.assertEquals(set([('A', 1), ('A', 4),
                                   ('B', 2), ('B', 5),
                                   ('C', 3), ('C', 6),
                                  ]),
                              set(self._query(ALL_CELLS_QUERY)))

    def testStructure(self):
            g = CsvGraph()
            g.read(StringIO.StringIO(EXAMPLE))
            #result = [tpl for tpl in g.query(STURCTURE_QUERY)]

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()