'''
Created on 3 Oct 2014

@author: s05nc4
'''
import unittest
import StringIO
from dot.rural.sepake.csv_to_rdf import CSV, PROV, row_graphs_from_file
from rdflib import RDF, RDFS, Graph
import csv
from rdflib.term import Literal

EXAMPLE = '''"A","B","C"
1,2,3
4,5,6
'''

class Test(unittest.TestCase):
    def setUp(self):
            self.g = Graph()
            (main_graph, row_graphs) = row_graphs_from_file(StringIO.StringIO(EXAMPLE))
            self.g += main_graph
            for rg in row_graphs:
                self.g += rg
            self.csv = csv.DictReader(StringIO.StringIO(EXAMPLE))
        
    def testCells(self):
        #Count cells and make no one else has a fieldname
        self.assertEquals(6, len(list(self.g[: RDF.type : CSV.Cell])))
        for (cell, _) in self.g[ : CSV.fieldName :]:
            self.assertEquals(CSV.Cell, self.g.value(cell, RDF.type))
        #Check that all CSV cells are represented
        for csv_row in self.csv:
            for key, value in csv_row.items():
                self.assertIn(Literal(int(value)),
                              self.g[Literal(key) : ~CSV.fieldName / CSV.fieldValue])

    def testStructure(self):
        #Count
        self.assertEquals(1, len(list(self.g[: PROV.generated :])))
        self.assertEquals(2, len(list(self.g[: PROV.generated / RDFS.member :])))
        self.assertEquals(6, len(list(self.g[: PROV.generated / RDFS.member / RDFS.member :])))
        #Types
        for (imp, f) in self.g[: PROV.generated :]:
            self.assertEquals(CSV.Import, self.g.value(imp, RDF.type))
            self.assertEquals(CSV.File, self.g.value(f, RDF.type))
            for row in self.g[f : RDFS.member]:
                self.assertEquals(CSV.Row, self.g.value(row, RDF.type))
                for cell in self.g[row : RDFS.member]:
                    self.assertEquals(CSV.Cell, self.g.value(cell, RDF.type))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()