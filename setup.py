# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et

from setuptools import setup
import flask_sass as package

setup(name=package.__package_name__,
      version=package.__version__,
      author=package.__author__,
      author_email=package.__email__,
      url=package.__url__,
      download_url='http://python.org/pypi/%s' % package.__package_name__,
      description=package.__summary__,
      long_description=package.__description__,
      license=package.__license__,
      platforms="OS Independent - Anywhere Python and Ruby's Sass is known to run.",
      keywords = "Flask SASS",
      py_modules = ["flask_sass"],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries :: Python Modules'
          'Topic :: Utilities',
      ]
)
