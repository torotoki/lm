#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name='lm',
  version='0.0.1',
  description='I/O management tools for experiments in Machine Learning',
  license = 'GPL-3.0',
  keywords = 'machine-learning experiments loggin python',
  author='Hiroyoshi Komatsu',
  author_email='hiroyoshi.komat@gmail.com',
  url='https://github.com/torotoki/lm',
  classifiers=[],
  packages=['lm', 'lm.command'],
  long_description=read('README.md'),
  entry_points=
    """
    [console_scripts]
    lm = lm.lm:main
    """,
)


