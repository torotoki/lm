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

  def execute(self, query):
    print(query)
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
