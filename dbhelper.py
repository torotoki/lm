from os import system, path
import sqlite3

def solve_db_path(self, conf_dir, db_name):
  return path.join(conf_dir, db_name)

def init_database(db_path):
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  return (conn, cursor)
