from os import system, path, makedirs
import sqlite3
import json

DEFAULT_DB_NAME = 'loginfo.db'
DEFAULT_CONF_DIR = './.lm/'


def solve_db_path(conf_dir, db_name):
  return path.join(conf_dir, db_name)

def init_database(db_path):
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  return (conn, cursor)

class Configure:
  db_path = None
  conn = None
  cursor = None

  def __init__(self):
    self.db_path = solve_db_path(DEFAULT_CONF_DIR,
                                 DEFAULT_DB_NAME)
    self.conn, self.cursor = init_database(self.db_path)

  def create_database(self, db_path):
    self.conn, self.cursor = init_database(db_path)
    self.STATS = {
      'num_executed_exp': 0,
      'created_by': uname()
    }

    with self.conn:

      ## overall metadata
      self.execute(
        """
        CREATE TABLE metadata (json JSON)
        """
      )

      self.execute(
        """
        INSERT INTO metadata (json)
        VALUES (
          json('%s')
        );
        """ % json.dumps(self.STATS)
      )

      ## each experiment metadata (bundles)
      self.execute(
        """
        CREATE TABLE bundles (json JSON)
        """
      )

      self.conn.commit()


  def execute(self, query):
    print("Executed SQLite command:")
    for line in query.split('\n'):
      print("  -", line)
    return self.conn.execute(query)


  def get_and_increment_num_exp(self):
    with self.conn:
      json_tree = self.execute(
        """
        SELECT
          tree.json
        FROM
          metadata,
          json_tree(metadata.json) as tree
        """
      ).fetchone()[0]
      metadata = json.loads(json_tree)

      # get num_exp
      num_executed_exp = metadata['num_executed_exp']+1

      # increment num_exp
      metadata['num_executed_exp'] += 1


      self.execute(
        """
        UPDATE metadata SET json = json('%s')
        """ % json.dumps(metadata)
      )

    return num_executed_exp


import datetime
import os
import subprocess

class ExperimentManager:
  db_path = None
  conn = None
  cursor = None

  STATE_PROCESSING = 'state_processing'
  STATE_FINISHED   = 'state_finished'
  STATE_ABORTED    = 'state_aborted'
  STATE_ERROR      = 'state_error'

  def execute(self, query):
    print("Executed SQLite command:")
    for line in query.split('\n'):
      print("  -", line)
    return self.conn.execute(query)


  def __init__(self):
    self.db_path = solve_db_path(DEFAULT_CONF_DIR,
                                 DEFAULT_DB_NAME)
    self.conn = init_database(self.db_path)

  def experiment_start(self, exp_id):
    stats = {}

    stats['exp_id'] = exp_id
    stats['uname']  = os.uname()
    stats['state']  = STATE_PROCESSING

    start_time = datetime.datetime.now()
    STATS['start_time'] = start_time.isoformat()

    ...

  def tail(fname, n=2):
    return subprocess.check_output(['tail', '-%d'%n, fname])

  def experiment_end(self, stdout_path, stderr_path):
    stats = {
      'state': STATE_FINISHED,
      'stdout_size': path.getsize(stdout_path),
      'stderr_size': path.getsize(stderr_path),
      'stdout_lastlines': self.tail(stdout_path),
      'stderr_lastlines': self.tail(stderr_path)
    }

    end_time = datetime.datetime.now()
    stats['end_time'] = end_time.isoformat()

    ...

