import webapp2
from rdflib import Graph
from appengine.ndbstore import NDBStore
import logging
from dot.rural.sepake.pure import university_of_aberdeen
from dot.rural.sepake.sparql_utils import copy

_GRAPH_ID = 'current'

class QueryJson(webapp2.RequestHandler):
    def get(self):
        #Access-Control-Allow-Origin: *
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/sparql-results+json; charset=utf-8'
        self.response.write(query(self.request.get('query')))

class CrawlOrder(webapp2.RequestHandler):
    def get(self):
        load_pure_data()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Load succeeded')

application = webapp2.WSGIApplication([
    ('''/sparql/current/query\.json.*''', QueryJson),
    ('''/crawl.order''', CrawlOrder),
], debug=True)

def load_pure_data():
    logging.info('Loading and processing data...')
    copy(university_of_aberdeen(), graph())
    
def update(q):
    graph().update(q)
    
def query(q):
    try:
        return graph().query(q).serialize(format='json')
    except Exception as e:
        logging.warn('%s caused %s'.format(q, e))
        raise e
    
def graph():
    return Graph(store = NDBStore(identifier = _GRAPH_ID))
