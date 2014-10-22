#!/usr/bin/env python

from distutils.core import setup

setup(name='dot.rural.sepake',
      version='0.2',
      description='SEPAKE Python distributible',
      author='Niels Christensen',
      scripts = ['scripts/import_ukeof.py'],
      packages=['dot',
                'dot.rural',
                'dot.rural.sepake',
                ],
      install_requires=[
          'rdflib',
          'lxml'
      ],
     )