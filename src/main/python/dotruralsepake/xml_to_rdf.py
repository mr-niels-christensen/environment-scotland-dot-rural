'''
Created on 26 Sep 2014

@author: s05nc4
'''

from rdflib import Graph
from lxml import etree
import logging

class XMLGraph(Graph):
    '''Loads any XML input and transforms it into RDF using http://www.gac-grid.org/project-products/Software/XML2RDF.html
    '''
    def __init__(self, xml_input, delete_nodes = None, namespaces = {}):
        super(XMLGraph, self).__init__()
        doc = etree.parse(xml_input)
        logging.debug('XML downloaded and parsed')
        if delete_nodes is not None:
            xslt = _XSLT_IGNORE_SUB_TREES_TEMPLATE % (' '.join('xmlns:%s="%s"' % ns_url for ns_url in namespaces.items()),
                                                      '|'.join(delete_nodes))
            doc = etree.XSLT(etree.XML(xslt))(doc)
            logging.debug('XML nodes deleted')
        xslt_root = etree.XML(_XSLT_XML2RDF)
        transform = etree.XSLT(xslt_root)
        result_tree = transform(doc)
        logging.debug('XML transformed to RDF/XML')
        self.parse(data = str(result_tree))
        logging.debug('RDF/XML parsed')

def _save_doc_for_debug(doc, filename = 'pretty.xml'):
    import StringIO
    s = StringIO.StringIO()
    doc.write(s)
    import xml.dom.minidom
    xml = xml.dom.minidom.parseString(s.getvalue())
    pretty_xml_as_string = xml.toprettyxml(indent="  ", encoding="utf-8")
    with open(filename, 'w') as out:
        out.write(pretty_xml_as_string)

_XSLT_IGNORE_SUB_TREES_TEMPLATE = '''
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
%s>
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
 <xsl:copy>
  <xsl:apply-templates select="@*|node()"/>
 </xsl:copy>
</xsl:template>

<xsl:template match="%s" />

</xsl:stylesheet>
'''
     
_XSLT_XML2RDF = '''<?xml version="1.0" encoding="UTF-8"?>
<!-- xml2rdf3.xsl        XSLT stylesheet to transform XML into RDF/XML

     Version             3.0  (2009-05-28)
     Changes to V2.5     rdf:value for all text, no attribute triples,
                         order predicates, comments as triples
     Web page            http://www.gac-grid.org/project-products/Software/XML2RDF.html
     Usage               xsltproc xml2rdf3.xsl file.xml
     Author              Frank Breitling (fbreitling at aip.de)
     Copyright 2009      AstroGrid-D (http://www.gac-grid.org/) 
   
     Licensed under the Apache License, Version 2.0 (the "License");
     you may not use this file except in compliance with the License.
     You may obtain a copy of the License at
 
         http://www.apache.org/licenses/LICENSE-2.0
 
     Unless required by applicable law or agreed to in writing, software
     distributed under the License is distributed on an "AS IS" BASIS,
     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
     See the License for the specific language governing permissions and
     limitations under the License. -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
       xmlns:xs="http://www.w3.org/TR/2008/REC-xml-20081126#">

       <xsl:strip-space elements="*"/>
       <xsl:output method="xml" indent="yes"/>

       <xsl:param name="BaseURI"><!-- Define if not completed by application-->
              <!-- http://www.exampleURI.net/STELLA-I -->
       </xsl:param>

       <!-- Begin RDF document -->
       <xsl:template match="/">
              <xsl:element name="rdf:RDF">
                     <rdf:Description>
                            <xsl:attribute name="rdf:about"/>
                            <xsl:apply-templates select="/*|/@*"/>
                     </rdf:Description>
              </xsl:element>
       </xsl:template>

       <!-- Turn XML elements into RDF triples. -->
       <xsl:template match="*">
              <xsl:param name="subjectname"/>

              <!-- Build URI for subjects resources from acestors elements -->
              <xsl:variable name="newsubjectname">
                     <xsl:if test="$subjectname=''">
                            <xsl:value-of select="$BaseURI"/>
                            <xsl:text>#</xsl:text>
                     </xsl:if>
                     <xsl:value-of select="$subjectname"/>
                     <xsl:value-of select="name()"/>
                     <!-- Add an ID to sibling element of identical name -->
                     <xsl:variable name="number">
                            <xsl:number/>
                     </xsl:variable>
                     <xsl:if test="$number > 1">
                            <xsl:text>_</xsl:text>
                            <xsl:number/>
                     </xsl:if>
              </xsl:variable>

              <xsl:element name="{name()}" namespace="{concat(namespace-uri(),'#')}">
                     <rdf:Description>
                            <xsl:attribute name="rdf:about">
                                   <xsl:value-of select="$newsubjectname"/>
                            </xsl:attribute>
                            <xsl:apply-templates select="@*|node()">
                                   <xsl:with-param name="subjectname"
                                          select="concat($newsubjectname,'/')"/>
                            </xsl:apply-templates>
                     </rdf:Description>
              </xsl:element>

              <!-- rdf:_no triple to preserve the order of elements, 
                   comment out if not needed -->
              <xsl:if test="count(../*) >1">
                     <xsl:element name="{concat('rdf:_',count(preceding-sibling::*)+1)}">
                            <rdf:Description>
                                   <xsl:attribute name="rdf:about">
                                          <xsl:value-of select="$newsubjectname"/>
                                   </xsl:attribute>
                            </rdf:Description>
                     </xsl:element>
              </xsl:if>
       </xsl:template>

       <!-- Create attribute triples. -->
       <xsl:template match="@*" name="attributes">
              <xsl:variable name="ns">
                     <!-- If attribute doesn't have a namespace use element namespace -->
                     <xsl:choose>
                            <xsl:when test="namespace-uri()=''">
                                   <xsl:value-of select="concat(namespace-uri(..),'#')"/>
                            </xsl:when>
                            <xsl:otherwise>
                                   <xsl:value-of select="concat(namespace-uri(),'#')"/>
                            </xsl:otherwise>
                     </xsl:choose>
              </xsl:variable>
              <xsl:element name="{name()}" namespace="{$ns}">
                     <xsl:value-of select="."/>
              </xsl:element>
       </xsl:template>

       <!-- Enclose text in an rdf:value element -->
       <xsl:template match="text()">
              <xsl:element name="rdf:value">
                     <xsl:value-of select="."/>
              </xsl:element>
       </xsl:template>

       <!-- Add triple to preserve comments -->
       <xsl:template match="comment()">
              <xsl:element name="xs:comment">
                     <xsl:value-of select="."/>
              </xsl:element>
       </xsl:template>

</xsl:stylesheet>
'''