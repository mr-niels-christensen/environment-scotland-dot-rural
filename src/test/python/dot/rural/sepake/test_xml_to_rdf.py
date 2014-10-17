'''
Created on 3 Oct 2014

@author: s05nc4
'''
import unittest
import StringIO
from dot.rural.sepake.xml_to_rdf import XMLGraph

EXAMPLE = '''<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
  <responseDate>2014-10-15T16:17:58Z</responseDate>
  <request verb="ListRecords">https://pure.abdn.ac.uk:8443/ws/oai</request>
  <ListRecords>
    <record>
      <header>
        <identifier>oai:pure.atira.dk:persons/c5f5cc43-8667-44f6-926f-c9d04df2e033</identifier>
        <datestamp>2013-11-08T07:31:08Z</datestamp>
        <setSpec>persons:all</setSpec>
      </header>
      <metadata>
        <oai_dc:dc xmlns:ns2="http://purl.org/dc/terms/" xmlns="http://purl.org/dc/elements/1.1/" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/">
          <identifier>http://pure.abdn.ac.uk:8080/portal/en/persons/m-welsh(c5f5cc43-8667-44f6-926f-c9d04df2e033).html</identifier>
          <title>Welsh, M</title>
        </oai_dc:dc>
      </metadata>
    </record>
    <record>
      <header>
        <identifier>oai:pure.atira.dk:persons/956194cf-8772-4d30-b536-e47b035683db</identifier>
        <datestamp>2013-11-28T07:34:11Z</datestamp>
        <setSpec>persons:all</setSpec>
      </header>
      <metadata>
        <oai_dc:dc xmlns:ns2="http://purl.org/dc/terms/" xmlns="http://purl.org/dc/elements/1.1/" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/">
          <identifier>http://pure.abdn.ac.uk:8080/portal/en/persons/elizabeth-anne-loggie(956194cf-8772-4d30-b536-e47b035683db).html</identifier>
          <title>Loggie, Elizabeth Anne</title>
        </oai_dc:dc>
      </metadata>
    </record>
    <resumptionToken cursor="0" completeListSize="24220">oai_dc/24220/42662723/100/0/2738/persons:all/x/x</resumptionToken>
  </ListRecords>
</OAI-PMH>
'''

class Test(unittest.TestCase):
    def setUp(self):
        self.g = XMLGraph(StringIO.StringIO(EXAMPLE))
         
    def testREST(self):
        g = []
        print 'Reading large file'
        import time
        start = time.time()
        with open('/Users/s05nc4/git/environment-scotland-dot-rural/src/main/resources/dot/rural/sepake/cli/search-projects-for-rural.xml') as f:
            g = XMLGraph(f, pre_process_xslt=_XSLT_IGNORE_SUB_TREES)
        print 'Reading and converting took %d seconds' % (time.time() - start)
        print 'Triples in large file: %d' % len(g)
        print 'Total time: %d seconds' % (time.time() - start)
           
    def testOai(self):
        self.assertEquals(60, len(self.g))
        #print self.g.serialize(format = 'nt')

_XSLT_IGNORE_SUB_TREES = '''
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:stab="http://atira.dk/schemas/pure4/model/base_uk/project/stable"
xmlns:personstab="http://atira.dk/schemas/pure4/model/base_uk/person/stable"
xmlns:person-template="http://atira.dk/schemas/pure4/model/template/abstractperson/stable">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
 <xsl:copy>
  <xsl:apply-templates select="@*|node()"/>
 </xsl:copy>
</xsl:template>

<xsl:template match="stab:associatedPublications|stab:associatedActivities|stab:personsUK|personstab:staffOrganisationAssociations|person-template:nameVariants|person-template:callName" />

</xsl:stylesheet>
'''
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()