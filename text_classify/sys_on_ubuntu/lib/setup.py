from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='keyword_filter_api',
      version=version,
      description="A new keyword fileter API",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='qihaibin',
      author_email='qi_haibin@vobile.cn',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [paste.app_factory]
      main = keyword_filter_api:main
      """,
      )
