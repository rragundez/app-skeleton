import os

from setuptools import find_packages
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="dummypackage",
    description="Python application example",
    author="Rodrigo Agundez",
    packages=find_packages(),
    long_description=read('README.md'),
)
