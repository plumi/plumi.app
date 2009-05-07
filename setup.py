from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='plumi.app',
      version=version,
      description="Plumi application setup",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone plumi web',
      author='Andy Nicholson',
      author_email='andy@engagemedia.org',
      url='https://svn.plone.org/svn/collective/plumi.app/trunk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plumi', 'plumi.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
