#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from optparse import OptionParser
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib import RDF
from dot.rural.sepake.ontology import SEPAKE
from dot.rural.sepake.pure import university_of_aberdeen
import time
from dot.rural.sepake.sparql_utils import copy
import logging

def _import(baseurl):
    remote = SPARQLUpdateStore(context_aware = False)
    remote.open(("%s/query" % baseurl, "%s/update" % baseurl))
    logging.info('Loading and processing data...')
    copy(university_of_aberdeen(), remote)
    return 0
            
def main():
    program_name = os.path.basename(sys.argv[0])
    argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser()
        parser.add_option("-u", "--url", dest="baseurl", help="set base url of SPARQL endpoint [default: %default]", metavar="URL")

        # set defaults
        parser.set_defaults(baseurl="http://localhost:3030/ds")

        # process options
        (opts, _args) = parser.parse_args(argv)

        # do
        return _import(opts.baseurl)
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


if __name__ == "__main__":
    sys.exit(main())