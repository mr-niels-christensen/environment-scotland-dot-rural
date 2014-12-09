'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
import webapp2

def route():
    return webapp2.Route(r'/search/<graphid>', handler=_SearchHandler, name='search')

class _SearchHandler(webapp2.RequestHandler):
    def get(self, graphid):
        raise Exception('Not implemented yet')