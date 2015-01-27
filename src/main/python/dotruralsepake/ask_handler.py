'''
Created on 9 Dec 2014

@author: Niels Christensen
'''
import webapp2
import logging
from google.appengine.api import mail

def route():
    return webapp2.Route(r'/ask/<to>', handler=_AskHandler, name='ask')

class _AskHandler(webapp2.RequestHandler):
    def get(self, to):
        if 'adminconsolecustompage' in self.request.GET:
            logging.debug('Activated from Admin console')
            del self.request.GET['adminconsolecustompage']
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write("mail.send_mail('Portalbot <admin@example.com>', to, 'Subject', 'Body', reply_to = 'foo@bar')")
