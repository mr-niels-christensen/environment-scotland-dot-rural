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
        query = self.request.get('query')
        result = json.dumps(search_graph(graphid, query))
        self.response.write(result)        

