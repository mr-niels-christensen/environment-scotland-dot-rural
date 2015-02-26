'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
import webapp2
import json
from dotruralsepake.search.search import search_graph
def route():
    return webapp2.Route(r'/search/<graphid>', handler=_SearchHandler, name='search')

class _SearchHandler(webapp2.RequestHandler):
    def get(self, graphid):
        #Access-Control-Allow-Origin: *
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        result = search_graph(graphid, **self.request.GET)
        result = json.dumps(result)
        self.response.write(result)        

