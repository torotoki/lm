import os
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
      'created_by': os.uname()
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
        CREATE TABLE bundles (json JSON, exp_id integer)
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
  stats = {}

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
    (self.conn, self.cursor) = init_database(self.db_path)

  def experiment_start(self, exp_id):
    self.stats['exp_id'] = exp_id
    self.stats['uname']  = os.uname()
    self.stats['state']  = self.STATE_PROCESSING

    start_time = datetime.datetime.now()
    self.stats['start_time'] = start_time.isoformat()

    with self.conn:
      self.execute(
        """
        INSERT INTO bundles (exp_id, json)
        VALUES (
          %d,
          json('%s')
        );
        """ % (exp_id, json.dumps(self.stats))
      )

  def tail(self, fname, n=2):
    binary_out = subprocess.check_output(
      ['tail', '-%d'%n, fname]
    )
    return binary_out.decode('utf-8')

  def experiment_end(self, stdout_path, stderr_path):
    self.stats['state'] = self.STATE_FINISHED
    self.stats['stdout_size'] = path.getsize(stdout_path)
    self.stats['stderr_size'] = path.getsize(stderr_path)
    self.stats['stdout_lastlines'] = self.tail(stdout_path)
    self.stats['stderr_lastlines'] = self.tail(stderr_path)

    end_time = datetime.datetime.now()
    self.stats['end_time'] = end_time.isoformat()

    with self.conn:
      exp_id = self.stats['exp_id']

      self.execute(
        """
        UPDATE bundles
        SET json = json('%s')
        WHERE exp_id = %d;
        """ % (json.dumps(self.stats), exp_id)
      )

