from setuptools import setup, find_packages
import os

version = '4.3.1'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('docs/CHANGES.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('docs/CONTRIBUTORS.txt')
    )

setup(name='plumi.app',
      version=version,
      description="Plumi video sharing",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone plumi video sharing',
      author='Andy Nicholson',
      author_email='andy@infiniterecursion.com.au',
      url='https://svn.plone.org/svn/collective/plumi.app/trunk',
      license='GPL',
      packages=find_packages('src/plumi.app',exclude=['ez_setup']),
      package_dir = {'':'src/plumi.app'},
      namespace_packages=['plumi', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plumi.content',
          'plumi.locales',
          'collective.transcode.star',
          'collective.contentlicensing',
          'qi.portlet.TagClouds',
          'Products.LinguaPlone',
          'plone.contentratings',
          'collective.seeder',
          'collective.piwik.mediaelement',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
