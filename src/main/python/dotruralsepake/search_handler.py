'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
import webapp2
import json

def route():
    return webapp2.Route(r'/search/<graphid>', handler=_SearchHandler, name='search')

class _SearchHandler(webapp2.RequestHandler):
    def get(self, graphid):
        #Access-Control-Allow-Origin: *
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/sparql-results+json; charset=utf-8'
        _ = self.request.get('query')
        result = json.dumps(_DUMMY_RESULT)
        self.response.write(result)        

_DUMMY_RESULT = {'number_found' : 3,
                 'results' : [{'uri' : 'http://dot.rural/sepake/PurePublication#bd6d7ee9-8513-42be-aeb6-6511dc86abb4',
                               'snippet' : 'f<i>o</i>o bar'},
                              {'uri' : 'http://dot.rural/sepake/PurePublication#e3a7198c-aded-447d-b67d-2279fcee8bb2',
                               'snippet' : 'f<i>o</i>o bar'},
                              {'uri' : 'http://dot.rural/sepake/PurePublication#05bfd7ea-b0b8-4e76-ad51-4ef7f544758e',
                               'snippet' : 'f<i>o</i>o bar'},
                              ],
                 'cursor.websafe' : 'foo',
                 }