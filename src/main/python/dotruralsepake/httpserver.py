import webapp2
from dotruralsepake import harvest_handler, sparql_handler, index_handler, search_handler, delete_handler
from dotruralsepake import ask_handler


application = webapp2.WSGIApplication([
    ask_handler.route(),
    sparql_handler.route(),
    harvest_handler.route(),
    index_handler.route(),
    search_handler.route(),
    delete_handler.route(),
], debug=True) #debug=true means stack traces in browser

