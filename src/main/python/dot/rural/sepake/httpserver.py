import webapp2
from rdflib import Graph
from appengine.ndbstore import NDBStore

_GRAPH_ID = 'current'

class QueryJson(webapp2.RequestHandler):
    def get(self):
        #Access-Control-Allow-Origin: *
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/sparql-results+json; charset=utf-8'
        self.response.write(query(self.request.get('query')))

application = webapp2.WSGIApplication([
    ('''/sparql/current/query\.json.*''', QueryJson),
], debug=True)

def update(q):
    graph().update(q)
    
def query(q):
    return graph().query(q).serialize(format='json')
    
def graph():
    return Graph(store = NDBStore(identifier = _GRAPH_ID))

