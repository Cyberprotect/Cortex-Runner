#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='Cortex Runner',
    version='1.0.0',
    description='Cortex jobs automation for TheHive.',
    long_description='',
    author='Rémi ALLAIN',
    author_email='rallain@cyberprotect.fr',
    maintainer='Rémi ALLAIN',
    url='https://github.com/Cyberprotect/CortexRunner',
    license='AGPL-V3',
    packages=['cortexrunner'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    include_package_data=True,
    install_requires=['requests', 'thehive4py']
)