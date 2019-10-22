#!/usr/bin/env python

from setuptools import setup

setup(
    name='metacritic',
    version='0.0.1',
    description='Metacritic parser',
    packages=['metacritic'],
    entry_points={
        'console_scripts': [
            'metacriticapp = metacritic.__main__:start_parser'
        ]
    },
    include_package_data=True,
    install_requires=[
        'typing;python_version<"3.5"',
        'requests',
        'beautifulsoup4',
        'lxml',
        'cached_property',
    ]
)
