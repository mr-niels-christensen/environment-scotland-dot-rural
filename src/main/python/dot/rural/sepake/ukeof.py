'''
Created on 16 Sep 2014

@author: s05nc4
'''

from dot.rural.sepake.csv_to_rdf import CSV
from rdflib.namespace import FOAF, XSD
from dot.rural.sepake.ontology import SEPAKE, SEPAKEOntologyGraph, PROV
from rdflib import RDF, RDFS
from rdflib import Graph
from csv_to_rdf import CSVGraph
import time
from rdflib.plugins.memory import IOMemory

class UKEOFGraph(Graph):
    def __init__(self, include_ontology = False, store = IOMemory()):
        super(UKEOFGraph, self).__init__(store = store)
        self._start = time.time()
        if include_ontology:
            self += SEPAKEOntologyGraph()
        csv = CSVGraph(include_ontology, store = store)
        self._log()
        print 'Downloading data from UKEOF...'
        csv.read_url('https://catalogue.ukeof.org.uk/api/documents?format=csv',
                     keep = lambda row: 'Activity' in row.values())
        self += csv
        self._log()
        for sparql in [INSERT_TYPE(), 
                       INSERT_LABEL(), 
                       INSERT_HOMEPAGE(), 
                       INSERT_LEAD_ORG(), 
                       INSERT_START_DATE(), 
                       INSERT_END_DATE(),
                       INSERT_COMMENT()]:
            print 'Updating with %s...' % sparql
            self.update(sparql)
            self._log()
        
    def _log(self):
        print 'Accumulated %d triples, total time %d seconds' % (len(self), time.time() - self._start)
        
def _expand(template_func):
    def expanded():
        template = template_func()
        return template.format(csv = CSV,
                               xsd = XSD,
                               rdf = RDF, 
                               rdfs = RDFS, 
                               prov = PROV, 
                               foaf = FOAF,
                               sepake = SEPAKE)
    return expanded

@_expand
def INSERT_TYPE():
    return '''
INSERT {{
    ?urilink <{rdf.type}> <{sepake.UKEOFActivity}> .
    ?urilink <{prov.wasDerivedFrom}> ?row .
}}
WHERE {{
    ?row <{rdf.type}> <{csv.Row}> .
    ?row <{rdfs.member}> ?typecell .
    ?typecell <{rdf.type}> <{csv.Cell}> .
    ?typecell <{csv.fieldName}> "Type" . 
    ?typecell <{csv.fieldValue}> "Activity" .
    ?row <{rdfs.member}> ?linkcell .
    ?linkcell <{rdf.type}> <{csv.Cell}> .
    ?linkcell <{csv.fieldName}> "Link to full record" .
    ?linkcell <{csv.fieldValue}> ?link . 
    BIND (URI(?link) AS ?urilink)
}}
'''

ACTIVITY_CLAUSES = '''
    ?link <{rdf.type}> <{sepake.UKEOFActivity}> .
    ?link <{prov.wasDerivedFrom}> ?row . 
'''

@_expand
def INSERT_LABEL():
    return '''
INSERT {{
    ?link <{rdfs.label}> ?title .
}}
WHERE {{''' + ACTIVITY_CLAUSES + '''
    ?row <{rdfs.member}> ?titlecell .
    ?titlecell <{rdf.type}> <{csv.Cell}> .
    ?titlecell <{csv.fieldName}> "Title" .
    ?titlecell <{csv.fieldValue}> ?title . 
}}
'''

@_expand
def INSERT_HOMEPAGE():
    return '''
INSERT {{
    ?link <{foaf.homepage}> ?link .
}}
WHERE {{''' + ACTIVITY_CLAUSES + '''
}}
'''

@_expand
def INSERT_LEAD_ORG():
    return '''
INSERT {{
    ?leadorglink <{rdfs.label}> ?leadorg .
    ?leadorglink <{sepake.owns}> ?link .
    ?leadorglink <{rdf.type}> <{sepake.UKEOFOrganisation}> .
}}
WHERE {{''' + ACTIVITY_CLAUSES + '''
    ?row <{rdfs.member}> ?leadcell .
    ?leadcell <{rdf.type}> <{csv.Cell}> .
    ?leadcell <{csv.fieldName}> "Lead organisation" .
    ?leadcell <{csv.fieldValue}> ?leadorg . 
    BIND (URI(CONCAT(str(<{sepake.UKEOFOrganisation}>), "#", ENCODE_FOR_URI(?leadorg))) AS ?leadorglink) 
}}
'''

@_expand
def INSERT_COMMENT():
    return '''
INSERT {{
    ?link <{sepake.htmlDescription}> ?htmldesc .
}}
WHERE {{''' + ACTIVITY_CLAUSES + '''
    ?row <{rdfs.member}> ?desccell .
    ?row <{rdfs.member}> ?objectivecell .
    ?row <{rdfs.member}> ?reasoncell .
    ?desccell <{rdf.type}> <{csv.Cell}> .
    ?desccell <{csv.fieldName}> "Description" .
    ?desccell <{csv.fieldValue}> ?desc . 
    ?objectivecell <{rdf.type}> <{csv.Cell}> .
    ?objectivecell <{csv.fieldName}> "Objectives" .
    ?objectivecell <{csv.fieldValue}> ?objective . 
    ?reasoncell <{rdf.type}> <{csv.Cell}> .
    ?reasoncell <{csv.fieldName}> "Reasons for collection" .
    ?reasoncell <{csv.fieldValue}> ?reason . 
    BIND (IF(STRLEN(?objective) > 0, CONCAT(?desc, "</p><p>Objective: ", ?objective), ?desc) AS ?withob)
    BIND (IF(STRLEN(?reason) > 0, CONCAT(?withob, "</p><p>Reasons for collection: ", ?reason), ?withob) AS ?htmldesc)
}}
'''

@_expand
def INSERT_START_DATE():
    return '''
INSERT {{
    ?link <{prov.startedAtTime}> ?startdate .
}}
WHERE {{''' + ACTIVITY_CLAUSES + '''
    ?row <{rdfs.member}> ?startdatecell .
    ?startdatecell <{rdf.type}> <{csv.Cell}> .
    ?startdatecell <{csv.fieldName}> "Lifespan start" .
    ?startdatecell <{csv.fieldValue}> ?startdatestr . 
    BIND (STRDT(?startdatestr, <{xsd.date}>) AS ?startdate)
}}
'''

@_expand
def INSERT_END_DATE():
    return '''
INSERT {{
    ?link <{prov.endedAtTime}> ?enddate .
}}
WHERE {{''' + ACTIVITY_CLAUSES + '''
    ?row <{rdfs.member}> ?enddatecell .
    ?enddatecell <{rdf.type}> <{csv.Cell}> .
    ?enddatecell <{csv.fieldName}> "Lifespan end" .
    ?enddatecell <{csv.fieldValue}> ?enddatestr . 
    BIND (STRDT(?enddatestr, <{xsd.date}>) AS ?enddate)
}}
'''
