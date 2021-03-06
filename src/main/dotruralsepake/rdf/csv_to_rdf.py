'''
Created on 26 Sep 2014

@author: s05nc4
'''

from dotruralsepake.rdf.utils import RDF_NAME, namespace
from rdflib import Graph, RDF, RDFS, URIRef, Literal
import csv
import urllib2
from uuid import uuid4

@namespace('http://dot.rural/sepake/csv', separator = '/')
class CSV(object):
    Import = RDF_NAME
    File = RDF_NAME
    Row = RDF_NAME
    Cell = RDF_NAME
    fieldName = RDF_NAME
    fieldValue = RDF_NAME

def row_graphs_from_url(url, keep = lambda row: True):
    '''Loads CSV from the given url, then calls row_graphs_from_file()
    '''
    csv_input = urllib2.urlopen(url, timeout=20)
    return row_graphs_from_file(csv_input, keep = keep)

def row_graphs_from_file(csv_input, keep = lambda row: True):
    '''Parses the CSV input and creates Graphs representing the data.
       @param csv_input: A file-like object with CSV content. The file must begin with a row of headers.
       @param keep: Boolean function on a row (represented as a dict mapping headers to values).
       @return: (main_graph, list of Graphs). The main Graph contains data on the import itself.
                The list contains one Graph per row for which keep is True.  
    '''
    main_graph = Graph()        
    #ID of this import operation
    ROOT_ID = _instance(CSV.Import)
    #Type of this import operation
    main_graph.add((ROOT_ID, RDF.type, CSV.Import))
    #ID of this file object
    file_id = _instance(CSV.File)
    #Type of a CSV file object
    main_graph.add((file_id, RDF.type, CSV.File))
    #This file object was generated by this Import
    main_graph.add((ROOT_ID, PROV.generated, file_id))
    yield main_graph
    #TODO add more PROV
    for row in csv.DictReader(csv_input):
        if keep(row):
            yield _graph_for_row(file_id, row)

@namespace('http://www.w3.org/ns/prov')
class PROV(object):
    Activity = RDF_NAME
    generated = RDF_NAME
    
class CSVOntologyGraph(Graph):
    '''Ontology for the data created by this module.
    '''
    def __init__(self):
        super(CSVOntologyGraph, self).__init__()
        self.add((CSV.Import, RDF.type, PROV.Activity))
        self.add((CSV.File,   RDF.type, RDF.Bag))#TODO Maybe use a named graph instead?
        self.add((CSV.Row,    RDF.type, RDF.Bag))
        self.add((CSV.Cell,   RDF.type, RDFS.Resource))


def _graph_for_row(file_id, row):
    g = Graph()
    _add_csv_row(g, file_id, row)
    return g

def _add_csv_row(g, file_id, row):
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
    g.add((row_id, RDF.type, CSV.Row))
    #file_id  -->  row_id 
    g.add((file_id, RDFS.member, row_id))
    for heading, value in row.iteritems():
        #ID of this cell
        cell_id = _instance(CSV.Cell)
        #Type of a CSV cell
        g.add((cell_id, RDF.type, CSV.Cell))
        #row_id --> cell_id
        g.add((row_id, RDFS.member, cell_id))
        #cell_id --> Heading
        g.add((cell_id, CSV.fieldName, Literal(heading)))
        #cell_id --> Value
        try:
            value = int(value)
        except ValueError:
            pass #TODO Parse floats and dates
        g.add((cell_id, CSV.fieldValue, Literal(value)))

def _instance(type_uri):
    '''@param type_uri: Any hashless URI, but preferably an rdf.type, e.g. CSV.Row
       @return: type_uri plus '#' and a random hash, as a URIRef 
    '''
    return URIRef('{type_uri}#{uuid}'.format(type_uri = type_uri, uuid = uuid4().hex))


