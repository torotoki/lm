#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sqlite3
from sys import stderr
from os import system, path, makedirs
from lm.dbhelper import Configure, ExperimentManager
from lm.dbhelper import DEFAULT_CONF_DIR

path_variable = 'LM_LOGS_PATH'
DEFAULT_PARENT_LOG_DIRECTORY = './logs/'

class Executor:
  use_nohup = None
  hide_output = None

  args = []
  parent_log_dir = DEFAULT_PARENT_LOG_DIRECTORY
  log_dir = None
  exp_id = None
  commands = None
  stdout_path = None
  stderr_path = None

  conf = None

  def __init__(self, parser):
    parser.add_argument('commands', type=str)
    parser.add_argument('--use_nohup', default=True, type=bool)
    args = parser.parse_args()
    self.commands = args.commands
    self.use_nohup = args.use_nohup

    try:
      self.conf = Configure()
      self.manager = ExperimentManager()
    except sqlite3.OperationalError:
      print("Erro: cannot connect to the database", file=stderr)
      print("Please use 'python lm.py init' in the "
            + "current directory before execusion.\n")
      exit()

    log_dir, exp_id = self.decide_log_dir(self.conf)
    self.create_log_dir(log_dir)
    self.log_dir = log_dir
    self.exp_id = exp_id
    self.args = args

    self.stdout_path = path.join(log_dir, "stdout.txt")
    self.stderr_path = path.join(log_dir, "stderr.txt")


  def decide_log_dir(self, conf):
    with conf.conn:
      # import ipdb; ipdb.set_trace()
      num = conf.get_and_increment_num_exp()
      p = path.join(self.parent_log_dir,
                    "%d.exp/" % num)
    return (p, num)

  def create_log_dir(self, log_dir):
    if path.exists(path.dirname(log_dir)):
      raise RuntimeError(
        "Error: Somehow automatically decided " + \
        "the unique log folder is already exists:",log_dir)
    makedirs(log_dir)

  def experiment_start(self):
    print("#### The Experiment is Started. ####")
    self.manager.experiment_start(self.exp_id,
                                  self.commands)

  def experiment_completed(self):
    self.manager.experiment_completed(self.stdout_path,
                                      self.stderr_path)
    print("#### The Experiment is Completed. ####")

  def experiment_aborted(self):
    self.manager.experiment_aborted(self.stdout_path,
                                    self.stderr_path)
    print("#### The Experiment is Aborted. ####")

  def experiment_error(self):
    self.manager.experiment_error(self.stdout_path,
                                  self.stderr_path)
    print("#### The Experiment Raises An Error. ####")

  def execute(self):

    self.experiment_start()

    try:
      cmd = ' '.join(
        ["{",
         "{",
         "env %s=%s" % (path_variable, self.log_dir),
         "nohup" if self.use_nohup else "",
         "%s" % self.commands,
         "| tee %s;" % self.stdout_path,
         "} 3>&2 2>&1 1>&3",
         "| tee %s;" % self.stderr_path,
         "} 3>&2 2>&1 1>&3"]
      )
      print("Executed shell command:")
      print("  -", cmd)
      # Replaced os.system to subprocess.run (python 3.5 is required)
      ## state = system(cmd)
      state = subprocess.run(cmd, shell=True, check=True)
      self.experiment_completed()
    except (KeyboardInterrupt, SystemExit):
      print ("\naborted.")
      self.experiment_aborted()
    except subprocess.CalledProcessError:
      print ("\ncrashed.")
      self.experiment_error()
