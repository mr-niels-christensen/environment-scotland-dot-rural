from google.appengine.ext.appstats import recording

#see https://code.google.com/p/googleappengine/source/browse/trunk/python/google/appengine/ext/appstats/sample_appengine_config.py

def webapp_add_wsgi_middleware(app):
    app = recording.appstats_wsgi_middleware(app)
    return app

# Enable Interactive Playground.
appstats_SHELL_OK = True

# Enable RPC cost calculation.
appstats_CALC_RPC_COSTS = True
