#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from optparse import OptionParser
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from dot.rural.sepake.ukeof import ukeof_graphs

_PERCENTAGES = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 101]

def _import(baseurl):
    remote = SPARQLUpdateStore(context_aware = False)
    remote.open(("%s/query" % baseurl, "%s/update" % baseurl))
    (length, graphs) = ukeof_graphs()
    print 'Processing %d graphs' % length
    checkpoints = [((x * length) / 100, '%0d%%' % x) for x in _PERCENTAGES]
    total = 0
    for g in graphs:
        _flush(g, remote)
        total += 1
        if total > checkpoints[0][0]:
                print checkpoints[0][1]
                checkpoints = checkpoints[1:]
    print 'Done'
    return 0
    
def _flush(g, remote):
    for triple in g:
        remote.add(triple)
        
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