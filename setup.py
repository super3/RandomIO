import sys
from setuptools import setup

from RandomIO import __version__

setup(
    name='RandomIO',
    version=__version__,
    packages=['RandomIO'],
    url='https://github.com/Storj/RandomIO',
    license='MIT',
    author='William James, Storj Labs',
    author_email='info@storj.io',
    description='Random byte and file generator',
    install_requires=[
        'pycrypto >= 2.6.1',
    ]
)
