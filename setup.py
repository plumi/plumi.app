from setuptools import setup, find_packages
import os

version = '0.6'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    )

setup(name='plumi.app',
      version=version,
      description="Plumi application setup",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone plumi policy',
      author='Andy Nicholson',
      author_email='andy@infiniterecursion.com.au',
      url='https://svn.plone.org/svn/collective/plumi.app/trunk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plumi', 'plumi.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plumi.content',
          'plumi.skin',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone

      """,
      )
