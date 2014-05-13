#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
  name='pymtgx',
  author='Petter Bjelland',
  version='0.1',
  author_email='petter.bjelland@gmail.com',
  description='API for generating Maltego MTGX file.',
  license='Apache2',    
  scripts=[],
  packages=['pymtgx'],
  install_requires=[
    'networkx'
  ]
)
