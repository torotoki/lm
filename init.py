import json
import shutil
from os import path, makedirs, uname
from dbhelper import solve_db_path, init_database
from dbhelper import DEFAULT_DB_NAME, DEFAULT_CONF_DIR

class Initializer:
  db_name = DEFAULT_DB_NAME
  conf_dir = DEFAULT_CONF_DIR
  conn = None
  cursor = None
  conf = None
  stats = {}

  def yes_no_input(self, message):
    while True:
      print(message)
      choice = input("Please respond with 'yes' or 'no' [y/N]: ").lower()
      if choice in ['y', 'ye', 'yes']:
        return True
      elif choice in ['n', 'no']:
        return False
      
  def execute(self, query):
    print(query)
    return self.conn.execute(query)

  def mk_dir_conf(self, init_directory):
    if path.exists(init_directory):
      self.yes_no_input("config directory already exists: %s\n"
                        % str(init_directory) \
                        + "Are you want sure to reinitalize the directory?")
      # remove files on the directory
      shutil.rmtree(init_directory)
    makedirs(init_directory, exist_ok=True)

  def __init__(self, parser):
    parser.add_argument('--init_directory',
                        default=DEFAULT_CONF_DIR, type=str)
    args = parser.parse_args()
    self.conf_dir = args.init_directory
    self.mk_dir_conf(self.conf_dir)
    self.db_path = solve_db_path(self.conf_dir, self.db_name)

    self.conf = Configure()
    self.conf.create_database(self.db_path)


  def close_db(self):
    conn.close()
