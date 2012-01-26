#!/usr/bin/env python

import sys

from setuptools import setup,find_packages

install_requires = ['setuptools','GitPython' ]
# simplejson is included in the standard library since Python 2.6 as json.
if sys.version_info[:2] < (2, 6):
    install_requires.append('simplejson >= 2.1.1')

setup(
    name='Hammertime',
    version='0.2.3',

    description='Time tracking with git.',
    long_description=open('README.rst').read(),
    keywords='git time tracking',
    url='https://github.com/caffeinehit/hammertime',
    author='Alen Mujezinovic',
    author_email='alen@caffeinehit.com',
    license='MIT',

    packages=find_packages(),
    include_package_data=True,

    entry_points = {
        'console_scripts': [
            'git-time = hammertime:main',
        ],
    },
    install_requires = install_requires,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
    ],
)