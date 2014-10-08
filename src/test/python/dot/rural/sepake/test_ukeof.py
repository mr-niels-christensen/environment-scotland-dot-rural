'''
Created on 3 Oct 2014

@author: s05nc4
'''
import unittest
import StringIO
from dot.rural.sepake.csv_to_rdf import CSV, CsvGraph, PROV
from rdflib import RDF, RDFS
from rdflib.namespace import FOAF
from dot.rural.sepake.ontology import ONTOLOGY
from rdflib.query import ResultRow
import csv

EXAMPLE = '''Type,Title,Description,Link to full record,Objectives,Keywords,Reasons for collection,Environmental domains,Parameters measured,Lead organisation,Online resources,Links to data,Lifespan start,Lifespan end,Funding categories,Last edited,UKEOF Identifier,Envirobase codings,GMES codings,GEOSS codings,ECV codings,Measurement regime,Legal background,Location (bounding boxes or points)
Activity,"Agri-environment scheme monitoring in England (ESA, CSS and ASPS schemes) - Monitoring of Cereal Field Margin Options",This three-year programme of work aimed to undertake a comprehensive and comparative evaluation of the effectiveness of a range of field margin management options used within various agri-environment schemes in conserving arable plants and providing resources for foraging bumblebees. The project looked at (i) 5-year old margins provided in two areas under the Arable Stewardship Pilot Scheme; (ii) Cultivated margins for Rare Arable Plants established and previously monitored under the Breckland ESA Scheme; and (iii) Arable margins established nationally under the expansion of the Countryside Stewardship Scheme to accommodate a wider range of Arable Options. The project as a whole was intended to provide a comprehensive picture of the contribution being made by agri-environment schemes to delivery of the Habitat Action Plan for Cereal Field Margins.,https://catalogue.ukeof.org.uk/id/00329c57-7e1e-401e-8804-bc71a1aa0a59,"Agri-environment monitoring activities are designed to enable an assessment of the impact of each Scheme on target features of environmental interest. They also provide information about the performance of management prescriptions. Monitoring activities are co-ordinated, rather than carried out in isolation, to ensure that an overall assessment of the effectiveness of the scheme can be made. Most monitoring protocols allow for repeat surveys capable of detecting significant real change and provide baseline and resurvey data. Due to the nature of sampling and the use of common methods, sample sites within the monitoring programme can be used to provide data or a sampling framework to address other policy and scientific needs. The main objective of this activity is: a) to undertake a comprehensive and comparative evaluation of the effectiveness of a range of field margin management options used within various agri-environment schemes in conserving arable plants and providing resources for foraging bumblebees.",Agri-environment scheme;Cereal field margin;Cereal headlands;Conservation headlands;Bumblebees;Sown Margins;Field Margins;Margins;Cultivated Margins;Countryside Stewardship;Arable margins;Biodiversity;Arable Opti;Biodiversity Action Plan;BAP,Data collection;Policy;Strategic goals;Ministerial commitment,Biosphere,land use;Site condition,Natural England,,,2003-01-01,2005-01-01,public,2014-05-15 14:18:49,641313,"A4, B2, C1, D5.4, C13.9, C2.1, E1.2.2, E5.A.1, E5.A.2, E5.B.4.1, E5.B.4.2, E5.C.3.9, G2.2.1.1, D2.1.4, D5.2.6, D5.2.8, E5.C.2, S3.6, S3.8, S3.10, S3.11",,,,,,-6.4526 49.8638 1.7675 55.8121
Activity,Detecting Pine Martens in England and Wales,"Records of Pine Marten sightings. Sightings validated for confidence using standardised interview approach, plus mortalities.",https://catalogue.ukeof.org.uk/id/004e1491-03ec-421d-a8fe-59eaec004672,Detection and status of Pine Martens in England and Wales,Biodiversity;Live sightings;telephone interview;quality score;validation;skill assessment;specimens;Feedback;Citizen science;volunteers,Basic science;Data collection;Statutory advice,Biosphere,Habitat;location;Observer knowledge;Date/time;Sighting duration;Sighting distance;Observer activity;weather;Light conditions;Description of animal;altitude;Quality score,The Vincent Wildlife Trust,,,1995-01-01,,voluntary,2014-04-30 17:14:28,457722,"E1.3, B1, B7, A4, C14, C16, A4, B7, C1, C13.9, E1.2.2, D2.1.6, E5.A.1, E5.A.2, G2.2.1.4, E5.B.4.2, G2.2.1.1, D5.2.2, E5.C.2, S3.8, S3.10, D5.2.2",,,,,,-6.4526 49.8638 1.7675 55.8121
Activity,Deepwater Survey Quarter 3,The recent Scottish deep-water fishery prompted Fisheries Research Services (FRS) to undertake a new type of survey dedicated to deep-water fish species. FRV Scotia has now conducted three bi-annual surveys along the slope and shelf edge to the west of Scotland. The results of these surveys will form a new time series of data that will allow us to identify long-term trends. Further information at: http://www.marlab.ac.uk/Delivery/standalone.aspx?contentid=585,https://catalogue.ukeof.org.uk/id/005036ca-98e5-48cf-bf50-5db3fb5dc925,,Fish,Data series,Marine,Fauna abundance per unit area of the bed;Fish taxonomy-related abundance per unit area of the bed,Marine Scotland,,,2002-01-01,,,2014-04-30 09:41:33,458291,"A4, B1, C1, D5.6, C3, E1.2.2, D3.2.4, G2.2.1.3, D5.2.3, G3.2.1, S6.2",,,,,,-8.6484 54.6338 -0.7283 60.8610
Activity,The Food We Waste in Scotland,Amounts and types of household food waste in Scotland 2009,https://catalogue.ukeof.org.uk/id/00536709-1366-490c-9c42-8d33f4507050,To quantify the amount and type of food waste thrown away by Scottish households,food waste;Scotland,Data collection;Legislative,Built environment,Amount of food waste;type of food waste,Waste and Resources Action Programme,,,2009-01-01,2009-01-01,public,2014-04-30 09:46:22,631514,"C12, A4, B3, D9, E2.2.B.3, C13.9, E2.2.A.4, E5.B.3.3, E5.A.1, E5.B.5.4, E5.B.5.9, G2.2.1.3, C6.2.2, E5.C.1, E5.C.3, S11.2, S11.7, S11.10, A2, S4.3, S4.23, S6.6, S7.4",,,,,,-8.6484 54.6338 -0.7283 60.8610
Facility,Owenkillew River,none provided,https://catalogue.ukeof.org.uk/id/00621cb0-ed85-11e3-ac10-0800200c9a66,,,,,,Northern Ireland Environment Agency,,,,,,2014-06-06 16:20:32,,,,,,,,POINT(-6.9836 54.7122)
Activity,Lowland grassland restoration monitoring (Twyford),"Field surveys. Botanical monitoring of fixed quadrats in June/July on all three downland restoration sites in Twyford, Hampshire. Invertebrate monitoring June- September on two of the sites",https://catalogue.ukeof.org.uk/id/0077fd09-f27a-4989-bf97-e4fb71f0be91,Following the development of vegetation and invertebrate communities post-reinstatement using translocated turf and seed mixes.,succession;restoration;Management;dynamics;Biodiversity;development;grassland;translocation,Basic science;Legislative;Statutory advice;Policy,Biosphere,treatment;seed mix;translocation;controls;management,Centre for Ecology & Hydrology,,,1992-01-01,,public,2014-04-30 09:42:45,463203,"E4.B.4.1, E4.B.4.3, E1.1, E1.3, E1.4, B1, A4, C16, E4.A.2, D5.2.8, D5.2.9, A4, B2, C1, D5.5, C13.9, G5, E1.2.2, D2.1.7, E5.A.2, E5.B.4.1, E5.C.3.9, G2.2.1.1, E5.C.3.2, D2.1.2, D5.2.6, D5.2.7, D5.2.8, E5.C.2, T3, T5, S3.10, S3.11, D5.2.6, D5.2.7, E4.C.4.6",,,,,,-6.4526 49.8638 1.7675 55.8121
Activity,Noble chafer beetles (specialist invertebrate survey),Targeted survey by entomologists for noble chafer beetles in orchard habitats in known historic range.,https://catalogue.ukeof.org.uk/id/0081d712-4af3-4b83-bd70-d62746193f92,Identify presence of noble chafers,NBN;Biodiversity;Coleoptera;Noble chafer beetles,Data series,Biosphere,Noble chafer beetles,Peoples Trust for Endangered Species,,https://data.nbn.org.uk/Datasets/GA000738,1999-01-01,,voluntary,2014-06-03 15:40:08,465995,"A4, B7, C1, C13.9, E1.2.2, E5.A.1, E5.A.2, E5.B.4.2, D2.1.4, D5.2.6, E5.C.2, G2.2.1, S3.8, S3.10",,,,,,-6.4526 49.8638 1.7675 55.8121
Activity,CCW Lagoon soft sediment survey,"Saline lagoons are identified as an Annex 1 feature under the Habitats directive. 3 SACs in Wales have Saline Lagoons listed as a feature; Cemlyn Bay SAC (Cemlyn lagoon), Pen Llyn a''r Sarnau SAC (Morfa Gwyllt Lagoon) and Pembrokeshire Marine SAC (Pickleridge Lagoon). Work is undertaken at each of the lagoons to monitoring and make a condition assessment of the annex 1 feature Within Cemlyn and Pickleridge Lagoon, benthic samples are collected at 3 fixed stations using either an Eckman grab or hand-held core. At Morfa Gwyllt a minimum of 10 random samples are taken within the lagoon using a hand-held core. For all three lagoons, sampling tales place in the winter on an annual basis. All samples are sieved over a 0.5mm mesh and granulometry samples are also collected. Benthic invertebrate samples are processed by laboratories that are members of the National Marine Biological Analytical Quality Control (NMBAQC) scheme and random samples from each survey are also selected for audit by an independent third party under the NMBAQC's Own Sample module. At each lagoon, temperature and salinity measures are taken continuously using in-situ loggers. http://www.jncc.gov.uk/protectedsites/sacselection/sac.asp?EUCode=UK0030114",https://catalogue.ukeof.org.uk/id/00a1aab5-3e82-498a-a78f-b41e1955248b,,Biodiversity;sediment;NBN;lagoon;Benthic invertebrates,Legislative,Marine;Biosphere,Sediment grain size parameters;Salinity of the water column;Temperature of the water column;Zoobenthos taxonomy-related counts,Natural Resources Wales,http://www.jncc.gov.uk/protectedsites/sacselection/sac.asp?EUCode=UK0030114,https://data.nbn.org.uk/Datasets/GA000789,2006-01-01,,,2014-06-25 09:23:09,511870,"A4, B2, C1, D5.4, G5, E1.2.2, D2.2.2, G2.2.1.4, D3.3.3, D5.2.10, D5.2.6, D5.2.7, S3.11",,,,,,
Facility,FAUGHAN RIVER AT DRUMAHOE,River monitoring stationAltitude: ,https://catalogue.ukeof.org.uk/id/00bc6172-9e06-42fa-8bc6-d9fcd0647f5a,,,,,,Northern Ireland Environment Agency,,,,,,2014-06-04 11:12:20,,,,,,,,POINT(-7.2805 54.9794)
'''

INSERT_TYPE = '''
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

INSERT_LABEL = '''
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

ADD_HOMEPAGE = '''
CONSTRUCT {{
    ?link <{foaf.homepage}> ?link .
}}
WHERE {{''' + ACTIVITY_CLAUSES + '''
}}
'''

ADD_LEAD_ORG = '''
CONSTRUCT {{
    ?leadorglink <{rdfs.label}> ?leadorg .
    ?leadorglink <{sepake.owns}> ?link .
}}
WHERE {{''' + ACTIVITY_CLAUSES + '''
    ?row <{rdfs.member}> ?leadcell .
    ?leadcell <{rdf.type}> <{csv.Cell}> .
    ?leadcell <{csv.fieldName}> "Lead organisation" .
    ?leadcell <{csv.fieldValue}> ?leadorg . 
    BIND (URI(CONCAT(str(<{sepake.UKEOFOrganisation}>), "#", ENCODE_FOR_URI(?leadorg))) AS ?leadorglink) 
}}
'''

'''
CONSTRUCT {{
    ?link <{rdfs.comment}> ?comment .
}}

'''
ADD_COMMENT = '''
SELECT *
WHERE {{''' + ACTIVITY_CLAUSES + '''
    ?row <{rdfs.member}> ?desccell .
    ?row <{rdfs.member}> ?objectivecell .
    ?desccell <{rdf.type}> <{csv.Cell}> .
    ?desccell <{csv.fieldName}> "Description" .
    ?desccell <{csv.fieldValue}> ?desc . 
    ?objectivecell <{rdf.type}> <{csv.Cell}> .
    ?objectivecell <{csv.fieldName}> "Objectives" .
    ?objectivecell <{csv.fieldValue}> ?objective . 
    BIND (IF(STRLEN(?objective) > 0, CONCAT(?desc, "<br>Objective: ", ?objective), ?desc) AS ?comment)
}}
'''

def _pythonify(result_row):
    '''@param result_row Row from a query result, instance of rdflib.query.ResultRow 
    '''
    return tuple([v.toPython() for v in result_row])

class Test(unittest.TestCase):
    def setUp(self):
            self.g = CsvGraph()
            self.g.read(StringIO.StringIO(EXAMPLE))
            self.csv = csv.DictReader(StringIO.StringIO(EXAMPLE))
    
    def _query(self, template, transformation = _pythonify):
        query = template.format(csv = CSV, 
                                rdf = RDF, 
                                rdfs = RDFS, 
                                prov = PROV, 
                                foaf = FOAF,
                                sepake = ONTOLOGY)
        return [transformation(tupl) for tupl in self.g.query(query)]
    
    def _update(self, template):
        query = template.format(csv = CSV, 
                                rdf = RDF, 
                                rdfs = RDFS, 
                                prov = PROV, 
                                foaf = FOAF,
                                sepake = ONTOLOGY)
        self.g.update(query)
    
    def _testUpdate(self, template):
        i = 0
        for row in self._query(template):
            print '%0d: %s' % (i, repr(row))
            i += 1
            
    def testAddType(self):
        self._update(INSERT_TYPE)
        activities = set(self.g.subjects(RDF.type, ONTOLOGY.UKEOFActivity))
        self.assertEquals(7, len(activities), repr(activities))
        for subject in activities:
            known = set(self.g.triples((subject, None, None)))
            self.assertEquals(2, len(known), known) #TODO test wasDerivedFrom

    def testAddLabel(self):
        self._update(INSERT_TYPE)
        self._update(INSERT_LABEL)
        labels = [_pythonify(r) for r in self.g.subject_objects(RDFS.label)]
        self.assertEquals(7, len(labels), repr(labels))
        self.assertEquals({(csv_row['Link to full record'], csv_row['Title']) 
                           for csv_row in self.csv if csv_row['Type'] == 'Activity'},
                          set(labels))

    def testAddHomepage(self):
        self._update(INSERT_TYPE)
        self._testUpdate(ADD_HOMEPAGE)

    def testAddLeadorg(self):
        self._update(INSERT_TYPE)
        self._testUpdate(ADD_LEAD_ORG)

    def testAddComment(self):
        self._update(INSERT_TYPE)
        self._testUpdate(ADD_COMMENT)
        r = self._query(ADD_COMMENT, transformation = ResultRow.asdict)
        print len(r)
        for f in ['link', 'comment', 'row', 'desccell', 'objectivecell']:
            s = {rr[f] for rr in r}
            print '%s(%d): %s' % (f, len(s), repr(s))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()