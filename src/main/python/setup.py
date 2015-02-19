#!/usr/bin/env python

from distutils.core import setup
from dotruralsepake import VERSION

setup(name='dot.rural.sepake',
      version = VERSION,
      description='SEPAKE Python distributible',
      author='Niels Christensen',
      packages=['dotruralsepake',
                'dotruralsepake.rdf',
                'dotruralsepake.harvest',
                'dotruralsepake.search',
                'dotruralsepake.metrics',
                ],
      install_requires=[
          'rdflib-appengine',
          'rdflib',
          'lxml'
      ],
     )