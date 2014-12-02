'''
Created on 2 Dec 2014

@author: Niels Christensen
'''
from dot.rural.sepake.xml_to_rdf import XMLGraph
import urllib2
import logging

class OAIHarvester(object):
    def __init__(self, url):
        self._url = url
        
    def next(self):
        xml_input = urllib2.urlopen(self._url, timeout=20)
        page = XMLGraph(xml_input)
        logging.debug('{} triples'.format(len(page)))
        logging.debug(page.serialize(format = 'n3'))