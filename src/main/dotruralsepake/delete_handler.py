'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
import webapp2
import logging
from rdflib_appengine.ndbstore import NDBStore
from google.appengine.api import search
from rdflib import Graph
from dotruralsepake.store import connect

def route():
    return webapp2.Route(r'/delete/<graphid>', handler=_DeleteHandler, name='delete')

class _DeleteHandler(webapp2.RequestHandler):
    def get(self, graphid):
        if 'adminconsolecustompage' in self.request.GET:
            logging.debug('Activated from Admin console')
            del self.request.GET['adminconsolecustompage']
        _delete(graphid, **self.request.GET)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('OK')

def _delete(graphid, overwriteBy = None):
    dest_graph = Graph(store = connect(identifier = graphid))
    src_graph = None if overwriteBy is None else Graph(store = connect(identifier = overwriteBy))
    logging.info('Deleting {}, len={}'.format(graphid, len(dest_graph)))
    dest_graph.destroy(None)
    logging.info('Deleted {}'.format(graphid))
    if src_graph is not None:
        dest_graph += src_graph
        logging.info('Copied {} (len={}) to {}'.format(overwriteBy, len(src_graph), graphid))

