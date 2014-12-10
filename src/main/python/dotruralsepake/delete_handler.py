'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
import webapp2
import logging
from rdflib import Graph
from rdflib_appengine.ndbstore import NDBStore

def route():
    return webapp2.Route(r'/delete/<graphid>', handler=_DeleteHandler, name='delete')

class _DeleteHandler(webapp2.RequestHandler):
    def get(self, graphid):
        logging.info('Deleting {}'.format(graphid))
        NDBStore(identifier = graphid).destroy(None)
        #TODO: Destroy search index
        logging.info('Deleted {}'.format(graphid))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('OK')
