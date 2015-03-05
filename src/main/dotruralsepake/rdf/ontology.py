'''
Created on 16 Sep 2014

@author: s05nc4
'''

from rdflib import Graph, RDFS
from rdflib.namespace import FOAF
from dotruralsepake.rdf.utils import RDF_NAME, namespace

@namespace('http://dot.rural/sepake', separator = '/')
class SEPAKE(object):
    Unverified        = RDF_NAME
    UKEOFActivity     = RDF_NAME
    UKEOFOrganisation = RDF_NAME
    PureProject       = RDF_NAME
    PureDepartment    = RDF_NAME
    PurePublication   = RDF_NAME
    PurePerson        = RDF_NAME
    NERCDataSet       = RDF_NAME
    ThisGraph         = RDF_NAME
    owns              = RDF_NAME
    ownedBy           = RDF_NAME
    htmlDescription   = RDF_NAME
    wasDetailedByData = RDF_NAME
    wasDetailedByCode = RDF_NAME
    wasDetailedAtTime = RDF_NAME
    graphSetAsDefault = RDF_NAME
    
@namespace('http://dot.rural/sepake/code', separator = '/')
class SEPAKECODE(object):
    PureRestPublication = RDF_NAME
    NercRSS             = RDF_NAME
    
@namespace('http://dot.rural/sepake/metrics', separator = '/')
class SEPAKEMETRICS(object):
    focushit = RDF_NAME

@namespace('http://www.w3.org/ns/prov')
class PROV(object):
    Activity        = RDF_NAME
    Organization    = RDF_NAME
    Person          = RDF_NAME
    startedAtTime   = RDF_NAME
    endedAtTime     = RDF_NAME
    wasInfluencedBy = RDF_NAME
    wasDerivedFrom  = RDF_NAME
    memberOf        = RDF_NAME
    hadMember       = RDF_NAME
    generatedAtTime = RDF_NAME

