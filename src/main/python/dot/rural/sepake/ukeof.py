'''
Created on 16 Sep 2014

@author: Niels Christensen

Code for downloading the UKEOF catalogue and transforming selected parts into RDF.
The main interface is ukeof_graphs()
'''

from dot.rural.sepake.csv_to_rdf import CSV
from rdflib.namespace import FOAF, XSD
from dot.rural.sepake.ontology import SEPAKE, PROV
from rdflib import RDF, RDFS
from rdflib import Graph
from csv_to_rdf import row_graphs_from_url
from rdflib.plugins.sparql.parser import parseUpdate
from rdflib.plugins.sparql.algebra import translateUpdate

def ukeof_graphs():
    '''Downloads the UKEOF catalogue and transforms each Activity into RDF.
       Note that part of the transformation on request as the client traverses the returned Graphs.
       @return: A 2-tuple (length, graphs).
                length is the number of elements in graphs
                graphs is a generator yielding one Graph containing triples regarding the import itself
                                               plus one Graph per Activity in the UKEOF catalogue
    '''
    (meta, rows) = row_graphs_from_url('https://catalogue.ukeof.org.uk/api/documents?format=csv',
                                       keep = lambda row: 'Activity' in row.values())
    return (1 + len(rows), _generate_graphs(meta, rows))


def _generate_graphs(meta, rows):
    '''Generator function yielding meta (unchanged)
       plus one per Graph in rows.
       Each of these Graphs will be transformed using the SPARQL statements
       in this file, and then all original triples (from the CSV file)
       will be removed.
    '''
    yield meta
    _UPDATES = [INSERT_TYPE(), 
                INSERT_LABEL(), 
                INSERT_HOMEPAGE(), 
                INSERT_LEAD_ORG(), 
                INSERT_START_DATE(), 
                INSERT_END_DATE(),
                INSERT_COMMENT()]
    for row in rows:
        g = Graph()
        #Add CSV triples
        g += row
        #Add triples from SPARQL statements
        for sparql in _UPDATES:
            g.update(sparql)
        #Remove CSV triples
        g -= row
        #Yield resulting graph
        yield g
        
def _expand_and_parse(template_func):
    '''Decorates a function which returns a Python format string.
       The format string must be SPARQL update with namespaces referenced dict-style like this:
       "INSERT {{ ?x <{rdfs.label}> "Hello" }} WHERE {{ ?x <{rdf.type}> <{sepake.HelloType}> }}"
       The decorated function will expand namespaces and return a preparsed SPARQL update.
    '''
    def expanded():
        template = template_func()
        updateString = template.format(csv = CSV,
                                       xsd = XSD,
                                       rdf = RDF, 
                                       rdfs = RDFS, 
                                       prov = PROV, 
                                       foaf = FOAF,
                                       sepake = SEPAKE)
        return translateUpdate(parseUpdate(updateString), None, {})
    return expanded

@_expand_and_parse
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

@_expand_and_parse
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

@_expand_and_parse
def INSERT_HOMEPAGE():
    return '''
INSERT {{
    ?link <{foaf.homepage}> ?link .
}}
WHERE {{''' + ACTIVITY_CLAUSES + '''
}}
'''

@_expand_and_parse
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

@_expand_and_parse
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

@_expand_and_parse
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

@_expand_and_parse
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
