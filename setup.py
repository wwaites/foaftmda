from setuptools import setup, find_packages
import sys, os

version = '0.1'

def readme():
    dirname = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dirname, "README.txt")
    return open(filename).read()

setup(name='foaftmda',
    version=version,
    description="Integration of FOAF into TMDA",
    long_description=readme(),
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='William Waites',
    author_email='ww@styx.org',
    url='http://river.styx.org/~ww/2010/10/foaftmda/',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "rdflib",
    ],
    entry_points="""
        [console_scripts]
        mboxlist2foaf=foaftmda.command:mboxlist2foaf
        checkfoaf=foaftmda.command:checkfoaf
    """,
    )
