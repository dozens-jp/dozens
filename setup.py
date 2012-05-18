import os
from setuptools import setup
from setuptools import find_packages

version = '0.0.1'
classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
]

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='dozens',
    version=version,
    packages=find_packages(),
    test_suite='tests',
    tests_require=['mock'],

    author='mikamix',
    author_email='tmp@mikamix.net',
    description='Wrapper for Dozens API',
    long_description=README,
    keywords=['dozens'],
    classifiers=classifiers,
    license='MIT',
)
