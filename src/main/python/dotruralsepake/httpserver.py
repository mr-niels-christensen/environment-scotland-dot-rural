import webapp2
from dotruralsepake import crawl_handler
from dotruralsepake import query_handler


application = webapp2.WSGIApplication([
    query_handler.route(),
    crawl_handler.route(),
], debug=True) #debug=true means stack traces in browser

