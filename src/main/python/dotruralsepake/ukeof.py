'''
Created on 16 Sep 2014

@author: Niels Christensen

Code for downloading the UKEOF catalogue and transforming selected parts into RDF.
The main interface is ukeof_graphs()
'''

from dotruralsepake.sparql_utils import expand_and_parse
from rdflib import Graph
from dotruralsepake.csv_to_rdf import row_graphs_from_url

def ukeof_graphs():
    '''Downloads the UKEOF catalogue and transforms each Activity into RDF.
       Note that part of the transformation on request as the client traverses the returned Graphs.
       @return: A 2-tuple (length, graphs).
                length is the number of elements in graphs
                graphs is a generator yielding one Graph containing triples regarding the import itself
                                               plus one Graph per Activity in the UKEOF catalogue
    '''
    meta_and_rows = row_graphs_from_url('https://catalogue.ukeof.org.uk/api/documents?format=csv',
                                        keep = lambda row: 'Activity' in row.values())
    yield next(meta_and_rows)
    for g in _generate_graphs(meta_and_rows):
        yield g

def _generate_graphs(rows):
    '''Generator function one per Graph in rows.
       Each of these Graphs will be transformed using the SPARQL statements
       in this file, and then all original triples (from the CSV file)
       will be removed.
    '''
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
        
@expand_and_parse
def INSERT_TYPE():
    return '''
INSERT {{
    ?urilink <{rdf.type}> <{sepake.UKEOFActivity}> .
    ?urilink <{prov.wasInfluencedBy}> ?row .
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
    ?link <{prov.wasInfluencedBy}> ?row . 
'''

@expand_and_parse
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

@expand_and_parse
def INSERT_HOMEPAGE():
    return '''
INSERT {{
    ?link <{foaf.homepage}> ?link .
}}
WHERE {{''' + ACTIVITY_CLAUSES + '''
}}
'''

@expand_and_parse
def INSERT_LEAD_ORG():
    return '''
INSERT {{
    ?leadorglink <{rdfs.label}> ?leadorg .
    ?leadorglink <{sepake.owns}> ?link .
    ?link        <{sepake.ownedBy}> ?leadorglink .
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

@expand_and_parse
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

@expand_and_parse
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

@expand_and_parse
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
