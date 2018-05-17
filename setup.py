#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (3, 5):
    raise NotImplementedError("Sorry, you need at least Python 3.5+ to use yomogi.")


setup(name='yomogi',
      version='0.1.0',
      description='Pure python library for data envelopment analysis.',
      #long_description=yomogi.__doc__,
      url='http://github.com/jzuccollo/yomogi',
      author='pomcho555',
      author_email='',
      license='None',
      packages=['yomogi'],
      install_requires=[
          'mecab-python3'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False,)
