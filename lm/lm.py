#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import argparse
from os import path, makedirs
from lm.run import Executor
from lm.init import Initializer
from lm.command.ls import LSCommand
from lm.command.rm import rm

help_message = "Usage: python [COMMAND] [options]"

def run(args):
  executor = Executor(args)
  executor.execute()

def init(parser, args):
  initializer = Initializer(parser)

def ls(parser):
  cmd = LSCommand(parser)
  cmd.printout()

# rm has no wrapper function

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
  elif command=='rm':
    rm(parser)
  else:
    print(help_message)

if __name__ == '__main__':
  main()
