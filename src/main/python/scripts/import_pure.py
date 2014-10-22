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

_PERCENTAGES = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 101]

def _import(baseurl):
    remote = SPARQLUpdateStore(context_aware = False)
    remote.open(("%s/query" % baseurl, "%s/update" % baseurl))
    print 'Loading and processing data...'
    start = time.time()
    g = university_of_aberdeen()
    projects = set(g.subjects(RDF.type, SEPAKE.PureProject))
    print '%d project(s) found: %s' % (len(projects), [repr(g.label(p)) for p in projects])
    length = len(g)
    print 'Data loaded and processed. Storing %d triples...' % length
    checkpoints = [((x * length) / 100, '%0d%%' % x) for x in _PERCENTAGES]
    total = 0
    for triple in g:
        remote.add(triple)
        total += 1
        if total > checkpoints[0][0]:
            print '%s, %d seconds' % (checkpoints[0][1], time.time() - start)
            checkpoints = checkpoints[1:]
    print 'Done'
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