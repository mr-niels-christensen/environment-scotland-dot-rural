#!/usr/bin/env python

from distutils.core import setup

setup(name='dot.rural.sepake',
      version='0.1',
      description='SEPAKE Python distributible',
      author='Niels Christensen',
      packages=['dot',
                'dot.rural',
                'dot.rural.sepake',
                ],
      install_requires=[
          'rdflib',
      ],
     )