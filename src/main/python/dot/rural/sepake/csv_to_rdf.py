'''
Created on 26 Sep 2014

@author: s05nc4
'''

from ns_utils import RDF_NAME, namespace
from rdflib import Graph, RDF, RDFS, URIRef, Literal
import csv
import urllib2
from rdflib.plugins.memory import IOMemory
from uuid import uuid4

@namespace('http://dot.rural/sepake/csv', separator = '/')
class CSV(object):
    Import = RDF_NAME
    File = RDF_NAME
    Row = RDF_NAME
    Cell = RDF_NAME
    fieldName = RDF_NAME
    fieldValue = RDF_NAME

def _instance(type_uri):
    return URIRef('{type_uri}#{uuid}'.format(type_uri = type_uri, uuid = uuid4().hex))

@namespace('http://www.w3.org/ns/prov')
class PROV(object):
    Activity = RDF_NAME
    generated = RDF_NAME
    
class CSVOntologyGraph(Graph):
    def __init__(self):
        super(CSVOntologyGraph, self).__init__()
        self.add((CSV.Import, RDF.type, PROV.Activity))
        self.add((CSV.File,   RDF.type, RDF.Bag))#TODO Maybe use a named graph instead?
        self.add((CSV.Row,    RDF.type, RDF.Bag))
        self.add((CSV.Cell,   RDF.type, RDFS.Resource))

class CSVGraph(Graph):
    def __init__(self, include_ontology = True, store = IOMemory()):
        super(CSVGraph, self).__init__(store = store)
        if include_ontology:
            self += CSVOntologyGraph()
        #ID of this import operation
        self._ROOT_ID = _instance(CSV.Import)
        #Type of this import operation
        self.add((self._ROOT_ID, RDF.type, CSV.Import))
    
    def read_url(self, url):
        '''Loads a CSV file from a URL and adds each row
        '''
        self.read(urllib2.urlopen(url)) #TODO add PROV
        
    def read(self, csv_input):
        '''Parses a CSV file and adds each row
        '''
        #ID of this file object
        file_id = _instance(CSV.File)
        #Type of a CSV file object
        self.add((file_id, RDF.type, CSV.File))
        #This file object was generated by this Import
        self.add((self._ROOT_ID, PROV.generated, file_id))
        #TODO add more PROV
        for row in csv.DictReader(csv_input):
            self._add_csv_row(file_id, row)
            
    def _add_csv_row(self, file_id, row):
        '''Adds a CSV row to the graph in the following style:
           file_id  -->  row_id --> cell_id_0 --> Heading_0
                              |              \--> Value_0
                              |---> cell_id_1 ...
                               ...
           The link from ROOT_ID to row_id is an rdfs:member
           The link from row_id to cell_id is also an rdfs:member
           Headings and values are literals, linked to by specific properties in our ontology.
        '''
        #ID of this row
        row_id = _instance(CSV.Row)
        #Type of a CSV row
        self.add((row_id, RDF.type, CSV.Row))
        #file_id  -->  row_id 
        self.add((file_id, RDFS.member, row_id))
        for heading, value in row.iteritems():
            #ID of this cell
            cell_id = _instance(CSV.Cell)
            #Type of a CSV cell
            self.add((cell_id, RDF.type, CSV.Cell))
            #row_id --> cell_id
            self.add((row_id, RDFS.member, cell_id))
            #cell_id --> Heading
            self.add((cell_id, CSV.fieldName, Literal(heading)))
            #cell_id --> Value
            try:
                value = int(value)
            except ValueError:
                pass #TODO Parse floats and dates
            self.add((cell_id, CSV.fieldValue, Literal(value)))

