#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import argparse
from os import path, makedirs
from cmdutils import Executor
from init import Initializer

help_message = "Usage: python [COMMAND] [options]"

def run(args):
  executor = Executor(args)
  executor.execute()

def init(parser, args):
  initializer = Initializer(parser)



def main():
  if len(sys.argv) < 2:
    print("Please specify a command.")
    print(help_message)
    exit()

  parser = argparse.ArgumentParser()
  command = sys.argv[1]
  if command=='run':
    run(parser)
  elif command=='init':
    init(parser, sys.argv)
  else:
    print(help_message)

if __name__ == '__main__':
  main()
