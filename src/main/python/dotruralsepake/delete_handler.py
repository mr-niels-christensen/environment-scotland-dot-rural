'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
import webapp2
import logging
from rdflib_appengine.ndbstore import NDBStore
from google.appengine.api import search

def route():
    return webapp2.Route(r'/delete/<graphid>', handler=_DeleteHandler, name='delete')

class _DeleteHandler(webapp2.RequestHandler):
    def get(self, graphid):
        logging.info('Deleting {}'.format(graphid))
        NDBStore(identifier = graphid).destroy(None)
        _delete_all_in_index(graphid)
        logging.info('Deleted {}'.format(graphid))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('OK')

def _delete_all_in_index(index_name):
    """Delete all the docs in the given index."""
    doc_index = search.Index(name=index_name)

    # looping because get_range by default returns up to 100 documents at a time
    while True:
        # Get a list of documents populating only the doc_id field and extract the ids.
        document_ids = [document.doc_id
                        for document in doc_index.get_range(ids_only=True)]
        if not document_ids:
            break
        # Delete the documents for the given ids from the Index.
        doc_index.delete(document_ids)
