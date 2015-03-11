'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
import webapp2
from dotruralsepake.search.index import Indexer
import logging
import datetime

def route():
    return webapp2.Route(r'/index/<graphid>', handler=_IndexHandler, name='index')

class _IndexHandler(webapp2.RequestHandler):
    def get(self, graphid):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('{} working on /index/{} ...\n'.format(datetime.datetime.utcnow(), graphid))
        for num in Indexer(graphid):
            logging.debug('Indexed {} resources'.format(num))
            self.response.write('{} Indexed {} resources\n'.format(datetime.datetime.utcnow(), num))
        self.response.write('{} OK, action completed\n'.format(datetime.datetime.utcnow()))
