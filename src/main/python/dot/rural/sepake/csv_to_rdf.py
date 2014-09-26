'''
Created on 26 Sep 2014

@author: s05nc4
'''

from rdflib import Graph, RDF, RDFS,BNode, Literal
import csv
import urllib2
from dot.rural.sepake.ontology import SEPAKE

class CsvGraph(Graph):
    def __init__(self, url):
        super(CsvGraph, self).__init__()
        self._node = BNode()
        self.add((self._node, RDF.type, SEPAKE.CsvImport))
        self._load_csv_url(url)

    def _load_csv_url(self, url):
        for row in csv.DictReader(urllib2.urlopen(url)):
            self._add_csv_row(row)
            
    def _add_csv_row(self, row):
        row_node = BNode()
        self.add((row_node, RDF.type, SEPAKE.CsvRow))
        self.add((self._node, RDFS.member, row_node))
        for heading, value in row.iter_items():
            cell_node = BNode()
            self.add(row_node, RDFS.member, cell_node)
            self.add((cell_node, SEPAKE.hasCSVHeading, Literal(heading)))
            self.add((cell_node, SEPAKE.hasCSVValue, Literal(value)))


        
        
        