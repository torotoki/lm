#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import argparse
from os import path, makedirs
from run import Executor
from init import Initializer
from ls import LSCommand

help_message = "Usage: python [COMMAND] [options]"

def run(args):
  executor = Executor(args)
  executor.execute()

def init(parser, args):
  initializer = Initializer(parser)

def ls(parser):
  cmd = LSCommand(parser)
  cmd.printout()

def main():
  if len(sys.argv) < 2:
    print("Please specify a command.")
    print(help_message)
    exit()

  parser = argparse.ArgumentParser()
  parser.add_argument('command', type=str)
  command = sys.argv[1]
  if command=='run':
    run(parser)
  elif command=='init':
    init(parser, sys.argv)
  elif command=='ls':
    ls(parser)
  else:
    print(help_message)

if __name__ == '__main__':
  main()
