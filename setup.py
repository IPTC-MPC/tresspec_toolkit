"""
Your licence goes here
"""

from setuptools import setup, find_packages

# See note below for more information about classifiers
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'Operating System:: Microsoft:: Windows:: Windows10',
    'Topic :: Scientific/Engineering :: Chemistry',
    'Topic :: Scientific/Engineering :: Physics',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9'
]

setup(
    name='tresspec_toolkit',
    version='0.0.1',
    description='A python package to process, analyze and visualize data from time-resolved spectroscopic measurements',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='Tobias Unruh',
    author_email='unruh@pc.uni-bonn.de',
    license='MIT',  # note the American spelling
    classifiers=classifiers,
    keywords='time-resolved spectroscopy',  # used when people are searching for a module, keywords separated with a space
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'matplotlib'],  # a list of other Python modules which this module depends on.  For example RPi.GPIO
    url='https://github.com/TobiU94/tresspec_toolkit'
)
