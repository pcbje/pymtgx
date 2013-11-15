#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='pymtgx',
    author='Petter Bjelland',
    version='0.1',
    author_email='petter.bjellans@hig.no',
    description='API for generating Maltego mtgx file.',
    license='Apache2',    
    scripts=[],
    zip_safe=False,
    package_data={},
    install_requires=[
        'networkx'
    ]
)
