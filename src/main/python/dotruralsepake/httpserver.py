import webapp2
from dotruralsepake import crawl_handler
from dotruralsepake import sparql_handler


application = webapp2.WSGIApplication([
    sparql_handler.route(),
    crawl_handler.route(),
], debug=True) #debug=true means stack traces in browser

