'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
import webapp2
from dotruralsepake.search.index import Indexer

def route():
    return webapp2.Route(r'/index/<graphid>', handler=_IndexHandler, name='index')

class _IndexHandler(webapp2.RequestHandler):
    def get(self, graphid):
        for _ in Indexer(graphid):
            pass
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('OK')
