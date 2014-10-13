#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from optparse import OptionParser
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from dot.rural.sepake.ukeof import UKEOFGraph, ukeof_graphs
from rdflib.plugins.memory import IOMemory

_PERCENTAGES = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 101]

def _import(baseurl):
    remote = SPARQLUpdateStore(context_aware = False)
    remote.open(("%s/query" % baseurl, "%s/update" % baseurl))
    total = 0
    for g in ukeof_graphs():
        l = len(g)
        total += l
        print '+%d --> %d' % (l, total)
        #_flush(g, remote)
    
def _flush(g, remote):
    length = len(g)
    print 'Flushing %d triples to %s/update...' % (length, remote.update_endpoint)
    checkpoints = [((x * length) / 100, '%0d%%' % x) for x in _PERCENTAGES]
    flushed = 0
    for triple in g:
        remote.add(triple)
        flushed += 1
        if flushed > checkpoints[0][0]:
            print checkpoints[0][1]
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