'''
Created on 3 Oct 2014

@author: s05nc4
'''
import unittest
import StringIO
from dot.rural.sepake.csv_to_rdf import CSV, CsvGraph, PROV
from rdflib import RDF, RDFS, Literal
from rdflib.query import ResultRow

EXAMPLE = '''"A","B","C"
1,2,3
4,5,6
'''

ALL_CELLS_QUERY = '''
SELECT ?h ?v 
WHERE {{
    ?cell <{rdf.type}> <{csv.Cell}> .
    ?cell <{csv.fieldName}> ?h . 
    ?cell <{csv.fieldValue}> ?v .
}}
'''

STRUCTURE_QUERY = '''
SELECT *
WHERE {{
    ?cell <{rdf.type}> <{csv.Cell}> .
    ?row <{rdfs.member}> ?cell . 
    ?row <{rdf.type}> <{csv.Row}> .
    ?file <{rdfs.member}> ?row . 
    ?file <{rdf.type}> <{csv.File}> .
    ?import <{prov.generated}> ?file . 
    ?import <{rdf.type}> <{csv.Import}> .
}}
'''

def _pythonify(result_row):
    '''@param result_row Row from a query result, instance of rdflib.query.ResultRow 
    '''
    return tuple([v.toPython() for v in result_row])

class Test(unittest.TestCase):
    def setUp(self):
            self.g = CsvGraph()
            self.g.read(StringIO.StringIO(EXAMPLE))
    
    def _query(self, template, transformation = _pythonify):
        query = template.format(csv = CSV, rdf = RDF, rdfs = RDFS, prov = PROV)
        return [transformation(tupl) for tupl in self.g.query(query)]
        
    def testCells(self):
            g = CsvGraph()
            g.read(StringIO.StringIO(EXAMPLE))
            self.assertEquals(set([('A', 1), ('A', 4),
                                   ('B', 2), ('B', 5),
                                   ('C', 3), ('C', 6),
                                  ]),
                              set(self._query(ALL_CELLS_QUERY)))

    def testStructure(self):
            result = self._query(STRUCTURE_QUERY, transformation = ResultRow.asdict)
            self.assertEquals(6, len(result), repr(result))
            found_csv_rows = {result_row['row'] for result_row in result}
            self.assertEquals(2, len(found_csv_rows), repr(result))
            found_csv_files = {result_row['file'] for result_row in result}
            self.assertEquals(1, len(found_csv_files), repr(result))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()