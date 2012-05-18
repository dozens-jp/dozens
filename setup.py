from setuptools import setup
from setuptools import find_packages

setup(
    name='dozens',
    version='0.0.1',
    packages=find_packages(),
    test_suite='dozens.tests',
    setup_requires=['nose'],
    tests_require=['mock', 'coverage'],
)
