#!/usr/bin/env python

from setuptools import setup,find_packages

setup(
    name='Hammertime',
    description='Time tracking with git',
    packages=find_packages(),
    author='Alen Mujezinovic',
    author_email='alen@caffeinehit.com',
    version='0.1.1',
    entry_points = {
        'console_scripts': [
            'git-time = hammertime:main',
        ],
    },
    install_requires = [
        'simplejson == 2.1.1',
        'GitPython >= 0.3.0'
    ]
)
