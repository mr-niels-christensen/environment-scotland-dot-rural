'''
Created on 3 Oct 2014

@author: s05nc4
'''
import unittest
import StringIO
from dot.rural.sepake.csv_to_rdf import CSV, CsvGraph
from rdflib import RDF, RDFS, Literal

EXAMPLE = '''"A","B","C"
1,2,3
4,5,6
'''

QUERY = '''
SELECT ?h ?v 
WHERE {{
    ?cell <{rdf.type}> <{csv.Cell}> .
    ?cell <{csv.fieldName}> ?h . 
    ?cell <{csv.fieldValue}> ?v}}
'''.format(csv = CSV, rdf = RDF, rdfs = RDFS)

class Test(unittest.TestCase):
    def testCells(self):
            g = CsvGraph()
            g.read(StringIO.StringIO(EXAMPLE))
            self.assertEquals({(Literal(x), Literal(y)) 
                               for (x,y) 
                               in [('A', 1), ('A', 4),
                                   ('B', 2), ('B', 5),
                                   ('C', 3), ('C', 6),
                                  ]
                               }, 
                              set([tpl for tpl in g.query(QUERY)]))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()