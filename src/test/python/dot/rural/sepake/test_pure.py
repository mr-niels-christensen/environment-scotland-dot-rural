'''
Created on 20 Oct 2014

@author: s05nc4
'''
import unittest
from rdflib import RDF, RDFS, URIRef
from rdflib.namespace import FOAF
from dot.rural.sepake.ontology import SEPAKE, PROV
from rdflib.term import Literal
from dot.rural.sepake.pure import PureGraph
from StringIO import StringIO
import datetime

PROJ = URIRef('http://dot.rural/sepake/PureProject#e963d657-b41f-44eb-a85d-7639346b378d')
DEPT = URIRef('http://dot.rural/sepake/PureDepartment#0031dcc2-16ec-4fd4-b88a-8eef66c67c67')

class Test(unittest.TestCase):
    def testConstructProject(self):
        self.g = PureGraph(StringIO(EXAMPLE))
        self.assertSingleValue(SEPAKE.PureProject, PROJ, RDF.type)
        self.assertSingleValue(Literal('RURAL DIGITAL ECONOMY RESEARCH HUB'), PROJ, RDFS.label)
        self.assertTrue(str(self.g.value(PROJ, SEPAKE.htmlDescription, any = False)).startswith('One of the three'))
        self.assertSingleValue(URIRef('http://www.dotrural.ac.uk'), PROJ, FOAF.homepage)
        self.assertSingleValue(datetime.datetime.strptime('2009-10-01+01:00', '%Y-%m-%d+%H:%M').date(), 
                               PROJ, PROV.startedAtTime)
        self.assertSingleValue(datetime.datetime.strptime('2015-03-31+01:00', '%Y-%m-%d+%H:%M').date(),
                               PROJ, PROV.endedAtTime)
        self.assertSingleValue(PROJ, DEPT, SEPAKE.owns)
        self.assertSingleValue(SEPAKE.PureDepartment, DEPT, RDF.type)
        self.assertEquals(8, len(self.g))

    def assertSingleValue(self, value, subject, predicate):
        found = self.g.value(subject, predicate, any = False)
        if type(value) not in [Literal, URIRef]:
            found = found.value
        self.assertEquals(value, found)

EXAMPLE = '''<?xml version="1.0" encoding="utf-8"?>
<project-template:GetProjectResponse requestId="" xmlns:activity-template="http://atira.dk/schemas/pure4/model/template/abstractactivity/stable" xmlns:core="http://atira.dk/schemas/pure4/model/core/stable" xmlns:extensions-base_uk="http://atira.dk/schemas/pure4/model/base_uk/extensions/stable" xmlns:extensions-core="http://atira.dk/schemas/pure4/model/core/extensions/stable" xmlns:externalorganisation-template="http://atira.dk/schemas/pure4/model/template/externalorganisation/stable" xmlns:journal-template="http://atira.dk/schemas/pure4/model/template/abstractjournal/stable" xmlns:organisation-template="http://atira.dk/schemas/pure4/model/template/abstractorganisation/stable" xmlns:person-base_uk="http://atira.dk/schemas/pure4/model/base_uk/person/stable" xmlns:person-template="http://atira.dk/schemas/pure4/model/template/abstractperson/stable" xmlns:project-template="http://atira.dk/schemas/pure4/wsdl/template/abstractproject/stable" xmlns:publication-base_uk="http://atira.dk/schemas/pure4/model/template/abstractpublication/stable" xmlns:stab="http://atira.dk/schemas/pure4/model/template/abstractproject/stable" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <core:count>1</core:count>
  <core:result>
    <core:content uuid="e963d657-b41f-44eb-a85d-7639346b378d" xmlns:stab="http://atira.dk/schemas/pure4/model/base_uk/project/stable" xsi:type="stab:FundedProjectType">
      <core:created>2010-03-31T15:38:08.835+01:00</core:created>
      <core:modified>2014-08-11T07:48:50.875+01:00</core:modified>
      <core:family>dk.atira.pure.api.shared.model.base_uk.project.Project</core:family>
      <core:type>dk.atira.pure.api.shared.model.base_uk.project.FundedProject</core:type>
      <stab1:title xmlns:stab1="http://atira.dk/schemas/pure4/model/template/abstractproject/stable">
        <core:localizedString formatted="true" locale="en_GB">RURAL DIGITAL ECONOMY RESEARCH HUB</core:localizedString>
      </stab1:title>
      <stab1:description xmlns:stab1="http://atira.dk/schemas/pure4/model/template/abstractproject/stable">
        <core:localizedString formatted="false" locale="en_GB">One of the three RCUK Digital Economy Research Hubs. Exploring how digital technologies can have a transformational impact on rural communities and business. User-centric activity is based around four interconnecting themes: Accessibility &amp; Mobilities, Healthcare, Enterprise &amp; Culture, and Natural Resource Conservation.</core:localizedString>
      </stab1:description>
      <stab1:projectURL xmlns:stab1="http://atira.dk/schemas/pure4/model/template/abstractproject/stable">www.dotrural.ac.uk</stab1:projectURL>
      <stab1:startFinishDate xmlns:stab1="http://atira.dk/schemas/pure4/model/template/abstractproject/stable">
        <extensions-core:startDate>2009-10-01+01:00</extensions-core:startDate>
        <extensions-core:endDate>2015-03-31+01:00</extensions-core:endDate>
      </stab1:startFinishDate>
      <stab1:status id="371" xmlns:stab1="http://atira.dk/schemas/pure4/model/template/abstractproject/stable">
        <core:uri>/dk/atira/pure/project/states/yes</core:uri>
        <core:term>
          <core:localizedString formatted="false" locale="en_GB">Awarded</core:localizedString>
        </core:term>
        <core:description/>
      </stab1:status>
      <stab1:typeClassification id="8231620" xmlns:stab1="http://atira.dk/schemas/pure4/model/template/abstractproject/stable">
        <core:uri>/dk/atira/pure/project/projecttypes/fundedproject/grant</core:uri>
        <core:term>
          <core:localizedString formatted="false" locale="en_GB">Grant project</core:localizedString>
        </core:term>
        <core:description/>
      </stab1:typeClassification>
      <stab1:owner uuid="0031dcc2-16ec-4fd4-b88a-8eef66c67c67" xmlns:stab1="http://atira.dk/schemas/pure4/model/template/abstractproject/stable">
        <core:created>2010-03-31T12:58:38.616+01:00</core:created>
        <core:modified>2014-05-09T05:30:15.869+01:00</core:modified>
        <core:portalUrl>http://pure.abdn.ac.uk:8080/portal/en/organisations/geosciences-geography--environment(0031dcc2-16ec-4fd4-b88a-8eef66c67c67).html</core:portalUrl>
        <core:family>dk.atira.pure.api.shared.model.organisation.Organisation</core:family>
        <core:type>dk.atira.pure.api.shared.model.organisation.Organisation</core:type>
        <organisation-template:name>
          <core:localizedString formatted="false" locale="en_GB">Geosciences, Geography &amp; Environment</core:localizedString>
        </organisation-template:name>
        <organisation-template:nameVariant>
          <core:classificationDefinedFieldExtension>
            <core:value>
              <core:localizedString formatted="false" locale="en_GB">Geography &amp; Environment</core:localizedString>
            </core:value>
            <core:typeClassification id="30819253">
              <core:uri>/dk/atira/pure/organisation/namevariants/shortname</core:uri>
              <core:term>
                <core:localizedString formatted="false" locale="en_GB">Short name</core:localizedString>
              </core:term>
              <core:description/>
            </core:typeClassification>
          </core:classificationDefinedFieldExtension>
          <core:classificationDefinedFieldExtension>
            <core:value/>
            <core:typeClassification id="30819255">
              <core:uri>/dk/atira/pure/organisation/namevariants/sortname</core:uri>
              <core:term>
                <core:localizedString formatted="false" locale="en_GB">Sort name</core:localizedString>
              </core:term>
              <core:description/>
            </core:typeClassification>
          </core:classificationDefinedFieldExtension>
          <core:classificationDefinedFieldExtension>
            <core:value/>
            <core:typeClassification id="30819257">
              <core:uri>/dk/atira/pure/organisation/namevariants/webname</core:uri>
              <core:term>
                <core:localizedString formatted="false" locale="en_GB">Web name</core:localizedString>
              </core:term>
              <core:description/>
            </core:typeClassification>
          </core:classificationDefinedFieldExtension>
        </organisation-template:nameVariant>
        <organisation-template:typeClassification id="316">
          <core:uri>/dk/atira/pure/organisation/organisationtypes/organisation/department</core:uri>
          <core:term>
            <core:localizedString formatted="false" locale="en_GB">Department</core:localizedString>
          </core:term>
          <core:description/>
        </organisation-template:typeClassification>
        <organisation-template:sources>
          <core:classificationDefinedStringFieldExtension>
            <core:value>40602</core:value>
            <core:classification id="30819287">
              <core:uri>/dk/atira/pure/organisation/organisationsources/organisationid</core:uri>
              <core:term>
                <core:localizedString formatted="false" locale="en_GB">Organisation ID</core:localizedString>
              </core:term>
              <core:description>
                <core:localizedString formatted="false" locale="en_GB">ID</core:localizedString>
              </core:description>
            </core:classification>
          </core:classificationDefinedStringFieldExtension>
        </organisation-template:sources>
        <organisation-template:external>
          <extensions-core:source>aberdeen_organisation</extensions-core:source>
          <extensions-core:sourceId>UNIT_CODE:40602</extensions-core:sourceId>
          <extensions-core:external>true</extensions-core:external>
        </organisation-template:external>
        <organisation-template:limitedVisibility>
          <core:visibility>FREE</core:visibility>
        </organisation-template:limitedVisibility>
      </stab1:owner>
      <stab1:persons xmlns:stab1="http://atira.dk/schemas/pure4/model/template/abstractproject/stable">
        <person-template:participantAssociation xmlns:stab="http://atira.dk/schemas/pure4/model/base_uk/person/stable" xsi:type="stab:UKClassifiedParticipantAssociationType">
          <person-template:person uuid="cd82bede-c06a-4eb8-9f50-f2c9bd949301" xsi:type="stab:UKPersonType">
            <core:created>2010-03-31T13:25:46.812+01:00</core:created>
            <core:modified>2014-05-28T09:39:14.624+01:00</core:modified>
            <core:portalUrl>http://pure.abdn.ac.uk:8080/portal/en/persons/claire-denise-wallace(cd82bede-c06a-4eb8-9f50-f2c9bd949301).html</core:portalUrl>
            <core:family>dk.atira.pure.api.shared.model.base_uk.person.Person</core:family>
            <core:type>dk.atira.pure.api.shared.model.base_uk.person.Person</core:type>
            <person-template:name>
              <core:firstName>Claire Denise</core:firstName>
              <core:lastName>Wallace</core:lastName>
            </person-template:name>
            <person-template:gender xsi:nil="true"/>
            <person-template:dateOfBirth xsi:nil="true"/>
            <person-template:linkIdentifiers>
              <extensions-core:linkIdentifier id="37172">
                <extensions-core:linkIdentifier>hesa:0000807053272</extensions-core:linkIdentifier>
              </extensions-core:linkIdentifier>
            </person-template:linkIdentifiers>
            <person-template:external>
              <extensions-core:source>aberdeen_person</extensions-core:source>
              <extensions-core:sourceId>41012912</extensions-core:sourceId>
              <extensions-core:external>true</extensions-core:external>
            </person-template:external>
            <person-template:limitedVisibility>
              <core:visibility>FREE</core:visibility>
            </person-template:limitedVisibility>
            <stab:title>Professor</stab:title>
            <stab:totalFTE>1.0</stab:totalFTE>
          </person-template:person>
        </person-template:participantAssociation>
        <person-template:participantAssociation xmlns:stab="http://atira.dk/schemas/pure4/model/base_uk/person/stable" xsi:type="stab:UKClassifiedParticipantAssociationType">
          <person-template:person uuid="ba1ce2e1-5952-4d2c-9cde-a304ab290454" xsi:type="stab:UKPersonType">
            <core:created>2010-03-31T13:05:29.014+01:00</core:created>
            <core:modified>2014-08-11T06:43:41.719+01:00</core:modified>
            <core:portalUrl>http://pure.abdn.ac.uk:8080/portal/en/persons/stephen-redpath(ba1ce2e1-5952-4d2c-9cde-a304ab290454).html</core:portalUrl>
            <core:family>dk.atira.pure.api.shared.model.base_uk.person.Person</core:family>
            <core:type>dk.atira.pure.api.shared.model.base_uk.person.Person</core:type>
            <person-template:name>
              <core:firstName>Stephen</core:firstName>
              <core:lastName>Redpath</core:lastName>
            </person-template:name>
            <person-template:gender xsi:nil="true"/>
            <person-template:dateOfBirth xsi:nil="true"/>
            <person-template:linkIdentifiers>
              <extensions-core:linkIdentifier id="9224">
                <extensions-core:linkIdentifier>hesa:0711700149028</extensions-core:linkIdentifier>
              </extensions-core:linkIdentifier>
            </person-template:linkIdentifiers>
            <person-template:external>
              <extensions-core:source>aberdeen_person</extensions-core:source>
              <extensions-core:sourceId>41014902</extensions-core:sourceId>
              <extensions-core:external>true</extensions-core:external>
            </person-template:external>
            <person-template:limitedVisibility>
              <core:visibility>FREE</core:visibility>
            </person-template:limitedVisibility>
            <stab:title>Professor</stab:title>
            <stab:researcherId>B-4640-2012</stab:researcherId>
            <stab:totalFTE>1.0</stab:totalFTE>
          </person-template:person>
        </person-template:participantAssociation>
        <person-template:participantAssociation xmlns:stab="http://atira.dk/schemas/pure4/model/base_uk/person/stable" xsi:type="stab:UKClassifiedParticipantAssociationType">
          <person-template:person uuid="b2a93e16-76c8-4eec-8553-43afabc45cc8" xsi:type="stab:UKPersonType">
            <core:created>2010-03-31T13:26:11.755+01:00</core:created>
            <core:modified>2014-08-11T06:43:41.844+01:00</core:modified>
            <core:portalUrl>http://pure.abdn.ac.uk:8080/portal/en/persons/rene-van-der-wal(b2a93e16-76c8-4eec-8553-43afabc45cc8).html</core:portalUrl>
            <core:family>dk.atira.pure.api.shared.model.base_uk.person.Person</core:family>
            <core:type>dk.atira.pure.api.shared.model.base_uk.person.Person</core:type>
            <person-template:name>
              <core:firstName>Rene</core:firstName>
              <core:lastName>Van Der Wal</core:lastName>
            </person-template:name>
            <person-template:gender xsi:nil="true"/>
            <person-template:dateOfBirth xsi:nil="true"/>
            <person-template:linkIdentifiers>
              <extensions-core:linkIdentifier id="37759">
                <extensions-core:linkIdentifier>hesa:0711700149039</extensions-core:linkIdentifier>
              </extensions-core:linkIdentifier>
            </person-template:linkIdentifiers>
            <person-template:external>
              <extensions-core:source>aberdeen_person</extensions-core:source>
              <extensions-core:sourceId>41014903</extensions-core:sourceId>
              <extensions-core:external>true</extensions-core:external>
            </person-template:external>
            <person-template:limitedVisibility>
              <core:visibility>FREE</core:visibility>
            </person-template:limitedVisibility>
            <stab:title>Dr</stab:title>
            <stab:totalFTE>1.0</stab:totalFTE>
          </person-template:person>
        </person-template:participantAssociation>
        <person-template:participantAssociation xmlns:stab="http://atira.dk/schemas/pure4/model/base_uk/person/stable" xsi:type="stab:UKClassifiedParticipantAssociationType">
          <person-template:person uuid="abcf1d8e-1703-46b1-8568-a1df91498898" xsi:type="stab:UKPersonType">
            <core:created>2012-08-01T06:41:05.743+01:00</core:created>
            <core:modified>2014-08-11T06:38:56.642+01:00</core:modified>
            <core:portalUrl>http://pure.abdn.ac.uk:8080/portal/en/persons/philip-michael-john-wilson(abcf1d8e-1703-46b1-8568-a1df91498898).html</core:portalUrl>
            <core:family>dk.atira.pure.api.shared.model.base_uk.person.Person</core:family>
            <core:type>dk.atira.pure.api.shared.model.base_uk.person.Person</core:type>
            <person-template:name>
              <core:firstName>Philip Michael John</core:firstName>
              <core:lastName>Wilson</core:lastName>
            </person-template:name>
            <person-template:gender xsi:nil="true"/>
            <person-template:dateOfBirth xsi:nil="true"/>
            <person-template:linkIdentifiers/>
            <person-template:external>
              <extensions-core:source>aberdeen_person</extensions-core:source>
              <extensions-core:sourceId>41020982</extensions-core:sourceId>
              <extensions-core:external>true</extensions-core:external>
            </person-template:external>
            <person-template:limitedVisibility>
              <core:visibility>FREE</core:visibility>
            </person-template:limitedVisibility>
            <stab:title>Professor</stab:title>
            <stab:totalFTE>1.0</stab:totalFTE>
          </person-template:person>
        </person-template:participantAssociation>
        <person-template:participantAssociation xmlns:stab="http://atira.dk/schemas/pure4/model/base_uk/person/stable" xsi:type="stab:UKClassifiedParticipantAssociationType">
          <person-template:person uuid="0606734d-5693-49ea-9ee3-cd4b8ddad60b" xsi:type="stab:UKPersonType">
            <core:created>2010-03-31T13:07:35.853+01:00</core:created>
            <core:modified>2014-05-28T09:39:10.806+01:00</core:modified>
            <core:portalUrl>http://pure.abdn.ac.uk:8080/portal/en/persons/pete-edwards(0606734d-5693-49ea-9ee3-cd4b8ddad60b).html</core:portalUrl>
            <core:family>dk.atira.pure.api.shared.model.base_uk.person.Person</core:family>
            <core:type>dk.atira.pure.api.shared.model.base_uk.person.Person</core:type>
            <person-template:name>
              <core:firstName>Peter</core:firstName>
              <core:lastName>Edwards</core:lastName>
            </person-template:name>
            <person-template:gender xsi:nil="true"/>
            <person-template:dateOfBirth xsi:nil="true"/>
            <person-template:profileInformation/>
            <person-template:photos>
              <core:file>
                <core:id>1766995</core:id>
                <core:fileName>pedwards2.jpg</core:fileName>
                <core:mimeType>image/jpeg</core:mimeType>
                <core:size>32892</core:size>
                <core:url>https://pure.abdn.ac.uk:8443/ws/files/1766995/pedwards2.jpg</core:url>
              </core:file>
            </person-template:photos>
            <person-template:linkIdentifiers>
              <extensions-core:linkIdentifier id="11889">
                <extensions-core:linkIdentifier>hesa:0000883000236</extensions-core:linkIdentifier>
              </extensions-core:linkIdentifier>
            </person-template:linkIdentifiers>
            <person-template:external>
              <extensions-core:source>aberdeen_person</extensions-core:source>
              <extensions-core:sourceId>41004169</extensions-core:sourceId>
              <extensions-core:external>true</extensions-core:external>
            </person-template:external>
            <person-template:limitedVisibility>
              <core:visibility>FREE</core:visibility>
            </person-template:limitedVisibility>
            <stab:title>Professor</stab:title>
            <stab:researcherId>A-4808-2010</stab:researcherId>
            <stab:totalFTE>1.0</stab:totalFTE>
          </person-template:person>
        </person-template:participantAssociation>
        <person-template:participantAssociation xmlns:stab="http://atira.dk/schemas/pure4/model/base_uk/person/stable" xsi:type="stab:UKClassifiedParticipantAssociationType">
          <person-template:person uuid="eca463f4-cd21-4ca6-9d77-84699601943c" xsi:type="stab:UKPersonType">
            <core:created>2010-03-31T13:08:03.061+01:00</core:created>
            <core:modified>2014-05-28T09:39:10.766+01:00</core:modified>
            <core:portalUrl>http://pure.abdn.ac.uk:8080/portal/en/persons/timothy-j-norman(eca463f4-cd21-4ca6-9d77-84699601943c).html</core:portalUrl>
            <core:family>dk.atira.pure.api.shared.model.base_uk.person.Person</core:family>
            <core:type>dk.atira.pure.api.shared.model.base_uk.person.Person</core:type>
            <person-template:name>
              <core:firstName>Timothy James Forester</core:firstName>
              <core:lastName>Norman</core:lastName>
            </person-template:name>
            <person-template:gender xsi:nil="true"/>
            <person-template:dateOfBirth xsi:nil="true"/>
            <person-template:linkIdentifiers>
              <extensions-core:linkIdentifier id="12475">
                <extensions-core:linkIdentifier>hesa:9911700087725</extensions-core:linkIdentifier>
              </extensions-core:linkIdentifier>
            </person-template:linkIdentifiers>
            <person-template:external>
              <extensions-core:source>aberdeen_person</extensions-core:source>
              <extensions-core:sourceId>41008772</extensions-core:sourceId>
              <extensions-core:external>true</extensions-core:external>
            </person-template:external>
            <person-template:limitedVisibility>
              <core:visibility>FREE</core:visibility>
            </person-template:limitedVisibility>
            <stab:title>Professor</stab:title>
            <stab:totalFTE>1.0</stab:totalFTE>
          </person-template:person>
        </person-template:participantAssociation>
        <person-template:participantAssociation xmlns:stab="http://atira.dk/schemas/pure4/model/base_uk/person/stable" xsi:type="stab:UKClassifiedParticipantAssociationType">
          <person-template:person uuid="bea4f526-c59a-43ff-aff8-01bf4eb28afb" xsi:type="stab:UKPersonType">
            <core:created>2010-03-31T13:25:34.240+01:00</core:created>
            <core:modified>2014-08-07T06:41:55.410+01:00</core:modified>
            <core:portalUrl>http://pure.abdn.ac.uk:8080/portal/en/persons/christopher-stuart-mellish(bea4f526-c59a-43ff-aff8-01bf4eb28afb).html</core:portalUrl>
            <core:family>dk.atira.pure.api.shared.model.base_uk.person.Person</core:family>
            <core:type>dk.atira.pure.api.shared.model.base_uk.person.Person</core:type>
            <person-template:name>
              <core:firstName>Christopher Stuart</core:firstName>
              <core:lastName>Mellish</core:lastName>
            </person-template:name>
            <person-template:gender xsi:nil="true"/>
            <person-template:dateOfBirth xsi:nil="true"/>
            <person-template:linkIdentifiers>
              <extensions-core:linkIdentifier id="36848">
                <extensions-core:linkIdentifier>hesa:0000795037731</extensions-core:linkIdentifier>
              </extensions-core:linkIdentifier>
            </person-template:linkIdentifiers>
            <person-template:external>
              <extensions-core:source>aberdeen_person</extensions-core:source>
              <extensions-core:sourceId>41011938</extensions-core:sourceId>
              <extensions-core:external>true</extensions-core:external>
            </person-template:external>
            <person-template:limitedVisibility>
              <core:visibility>FREE</core:visibility>
            </person-template:limitedVisibility>
            <stab:title>Professor</stab:title>
            <stab:totalFTE>0.8</stab:totalFTE>
          </person-template:person>
        </person-template:participantAssociation>
        <person-template:participantAssociation xmlns:stab="http://atira.dk/schemas/pure4/model/base_uk/person/stable" xsi:type="stab:UKClassifiedParticipantAssociationType">
          <person-template:person uuid="a91cf78b-0849-4c4c-8569-6f1b133b5220" xsi:type="stab:UKPersonType">
            <core:created>2010-03-31T13:17:45.310+01:00</core:created>
            <core:modified>2014-07-23T12:29:14.947+01:00</core:modified>
            <core:portalUrl>http://pure.abdn.ac.uk:8080/portal/en/persons/gorry-fairhurst(a91cf78b-0849-4c4c-8569-6f1b133b5220).html</core:portalUrl>
            <core:family>dk.atira.pure.api.shared.model.base_uk.person.Person</core:family>
            <core:type>dk.atira.pure.api.shared.model.base_uk.person.Person</core:type>
            <person-template:name>
              <core:firstName>Godred</core:firstName>
              <core:lastName>Fairhurst</core:lastName>
            </person-template:name>
            <person-template:gender xsi:nil="true"/>
            <person-template:dateOfBirth xsi:nil="true"/>
            <person-template:profileInformation/>
            <person-template:linkIdentifiers>
              <extensions-core:linkIdentifier id="25772">
                <extensions-core:linkIdentifier>hesa:0000871000303</extensions-core:linkIdentifier>
              </extensions-core:linkIdentifier>
            </person-template:linkIdentifiers>
            <person-template:external>
              <extensions-core:source>aberdeen_person</extensions-core:source>
              <extensions-core:sourceId>41002177</extensions-core:sourceId>
              <extensions-core:external>true</extensions-core:external>
            </person-template:external>
            <person-template:limitedVisibility>
              <core:visibility>FREE</core:visibility>
            </person-template:limitedVisibility>
            <stab:title>Professor</stab:title>
            <stab:totalFTE>1.0</stab:totalFTE>
          </person-template:person>
        </person-template:participantAssociation>
        <person-template:participantAssociation xmlns:stab="http://atira.dk/schemas/pure4/model/base_uk/person/stable" xsi:type="stab:UKClassifiedParticipantAssociationType">
          <person-template:person uuid="b008c70d-5a8e-46ce-9e93-174193fa5f0f" xsi:type="stab:UKPersonType">
            <core:created>2010-03-31T13:19:19.113+01:00</core:created>
            <core:modified>2014-07-19T06:35:54.059+01:00</core:modified>
            <core:portalUrl>http://pure.abdn.ac.uk:8080/portal/en/persons/john-donald-nelson(b008c70d-5a8e-46ce-9e93-174193fa5f0f).html</core:portalUrl>
            <core:family>dk.atira.pure.api.shared.model.base_uk.person.Person</core:family>
            <core:type>dk.atira.pure.api.shared.model.base_uk.person.Person</core:type>
            <person-template:name>
              <core:firstName>John Donald</core:firstName>
              <core:lastName>Nelson</core:lastName>
            </person-template:name>
            <person-template:gender xsi:nil="true"/>
            <person-template:dateOfBirth xsi:nil="true"/>
            <person-template:linkIdentifiers>
              <extensions-core:linkIdentifier id="28268">
                <extensions-core:linkIdentifier>hesa:0711700149855</extensions-core:linkIdentifier>
              </extensions-core:linkIdentifier>
            </person-template:linkIdentifiers>
            <person-template:external>
              <extensions-core:source>aberdeen_person</extensions-core:source>
              <extensions-core:sourceId>41014985</extensions-core:sourceId>
              <extensions-core:external>true</extensions-core:external>
            </person-template:external>
            <person-template:limitedVisibility>
              <core:visibility>FREE</core:visibility>
            </person-template:limitedVisibility>
            <stab:title>Professor</stab:title>
            <stab:totalFTE>1.0</stab:totalFTE>
          </person-template:person>
        </person-template:participantAssociation>
        <person-template:participantAssociation xmlns:stab="http://atira.dk/schemas/pure4/model/base_uk/person/stable" xsi:type="stab:UKClassifiedParticipantAssociationType">
          <person-template:person uuid="e3821ac9-10fe-4615-bb9f-a3af2329eb54" xsi:type="stab:UKPersonType">
            <core:created>2010-03-31T13:14:32.906+01:00</core:created>
            <core:modified>2014-05-28T09:39:12.852+01:00</core:modified>
            <core:portalUrl>http://pure.abdn.ac.uk:8080/portal/en/persons/john-hugh-farrington(e3821ac9-10fe-4615-bb9f-a3af2329eb54).html</core:portalUrl>
            <core:family>dk.atira.pure.api.shared.model.base_uk.person.Person</core:family>
            <core:type>dk.atira.pure.api.shared.model.base_uk.person.Person</core:type>
            <person-template:name>
              <core:firstName>John Hugh</core:firstName>
              <core:lastName>Farrington</core:lastName>
            </person-template:name>
            <person-template:gender xsi:nil="true"/>
            <person-template:dateOfBirth xsi:nil="true"/>
            <person-template:linkIdentifiers>
              <extensions-core:linkIdentifier id="21204">
                <extensions-core:linkIdentifier>hesa:0000707003360</extensions-core:linkIdentifier>
              </extensions-core:linkIdentifier>
            </person-template:linkIdentifiers>
            <person-template:external>
              <extensions-core:source>aberdeen_person</extensions-core:source>
              <extensions-core:sourceId>41001932</extensions-core:sourceId>
              <extensions-core:external>true</extensions-core:external>
            </person-template:external>
            <person-template:limitedVisibility>
              <core:visibility>FREE</core:visibility>
            </person-template:limitedVisibility>
            <stab:title>Professor</stab:title>
            <stab:totalFTE>1.0</stab:totalFTE>
          </person-template:person>
        </person-template:participantAssociation>
      </stab1:persons>
      <stab1:organisations xmlns:stab1="http://atira.dk/schemas/pure4/model/template/abstractproject/stable"/>
      <stab1:external xmlns:stab1="http://atira.dk/schemas/pure4/model/template/abstractproject/stable">
        <extensions-core:source>aberdeen_project</extensions-core:source>
        <extensions-core:sourceId>26804</extensions-core:sourceId>
        <extensions-core:external>true</extensions-core:external>
      </stab1:external>
      <stab1:limitedVisibility xmlns:stab1="http://atira.dk/schemas/pure4/model/template/abstractproject/stable">
        <core:visibility>FREE</core:visibility>
      </stab1:limitedVisibility>
      <stab:acronym>dot.rural</stab:acronym>
      <stab:keyFindings/>
      <stab:laymansdescription/>
      <stab:expectedStartDate>2009-10-01+01:00</stab:expectedStartDate>
      <stab:expectedEndDate>2014-09-30+01:00</stab:expectedEndDate>
    </core:content>
  </core:result>
</project-template:GetProjectResponse>
'''
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()