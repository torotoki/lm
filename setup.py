#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

if __name__ == '__main__':
  setup(
    name='lm',
    version='0.0.1',
    description='I/O management tools for experiments in Machine Learning',
    author='Hiroyoshi Komatsu',
    author_email='hiroyoshi.komat@gmail.com',
    url='https://github.com/torotoki/lm',
    classifiers=[],
    packages=find_packages(),
    install_requires=[],
    tests_require=[],
    include_package_data=True,
    zip_safe=False,
    entry_points="""
    [console_scripts]
    lm = lm.lm:main
    """,
  )


