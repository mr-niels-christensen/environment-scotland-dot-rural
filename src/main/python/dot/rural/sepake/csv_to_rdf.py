'''
Created on 26 Sep 2014

@author: s05nc4
'''

from rdflib import URIRef, Graph, RDF, RDFS,BNode, Literal
import csv
import urllib2

RDF_NAME = object()

class MyMeta(type):
    def __getattribute__(self, name):
        x = type.__getattribute__(self, name)
        if x is RDF_NAME:
            return URIRef(type.__getattribute__(self, 'BASE_URI') + '#' + name)
        else:
            return x
        
def namespace(base_uri):
    def class_rebuilder(cls):
        class NewClass(cls):
            __metaclass__ = MyMeta
            BASE_URI = base_uri
        return NewClass
    return class_rebuilder

@namespace('http://dot.rural/sepake/csv')
class CSV(object):
    Import = RDF_NAME
    Row = RDF_NAME
    Cell = RDF_NAME
    fieldName = RDF_NAME
    fieldValue = RDF_NAME
    

class CsvGraph(Graph):
    def __init__(self, url):
        super(CsvGraph, self).__init__()
        #ID of this import operation
        self._ROOT_ID = BNode()
        #Type of this import operation
        self.add((self._ROOT_ID, RDF.type, CSV.Import))
    
    def read_url(self, url):
        '''Loads a CSV file from a URL and adds each row
        '''
        self.read(urllib2.urlopen(url)) #TODO add PROV
        
    def read(self, csv_input):
        '''Parses a CSV file and adds each row
        '''
        #TODO add PROV
        for row in csv.DictReader(csv_input):
            self._add_csv_row(row)
            
    def _add_csv_row(self, row):
        '''Adds a CSV row to the graph in the following style:
           ROOT_ID  -->  row_id --> cell_id_0 --> Heading_0
                              |              \--> Value_0
                              |---> cell_id_1 ...
                               ...
           The link from ROOT_ID to row_id is an rdfs:member
           The link from row_id to cell_id is also an rdfs:member
           Headings and values are literals, linked to by specific properties in our ontology.
        '''
        #ID of this row
        row_id = BNode()
        #Type of a CSV row
        self.add((row_id, RDF.type, CSV.Row))
        #ROOT_ID  -->  row_id 
        self.add((self._ROOT_ID, RDFS.member, row_id))
        for heading, value in row.iter_items():
            #ID of this cell
            cell_node = BNode()
            #Type of a CSV cell
            self.add((row_id, RDF.type, CSV.Cell))
            #row_id --> cell_id
            self.add(row_id, RDFS.member, cell_node)
            #cell_id --> Heading
            self.add((cell_node, CSV.fieldName, Literal(heading)))
            #cell_id --> Value
            self.add((cell_node, CSV.fieldValue, Literal(value)))

if __name__ == '__main__':
    print repr(CSV.Import)
        
        