'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
import webapp2

def route():
    return webapp2.Route(r'/index/<graphid>', handler=_IndexHandler, name='index')

class _IndexHandler(webapp2.RequestHandler):
    def get(self, graphid):
        raise Exception('Not implemented yet')