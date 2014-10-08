'''
Created on 16 Sep 2014

@author: s05nc4
'''

from dot.rural.sepake.csv_to_rdf import CSV, PROV
from rdflib.namespace import FOAF, XSD
from dot.rural.sepake.ontology import ONTOLOGY
from rdflib import RDF, RDFS

def _expand(template_func):
    def expanded():
        template = template_func()
        return template.format(csv = CSV,
                               xsd = XSD,
                               rdf = RDF, 
                               rdfs = RDFS, 
                               prov = PROV, 
                               foaf = FOAF,
                               sepake = ONTOLOGY)
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
