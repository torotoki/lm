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
  stats = {}

  def yes_no_input(self, message):
    while True:
      print(message)
      choice = input("Please respond with 'yes' or 'no' [y/N]: ").lower()
      if choice in ['y', 'ye', 'yes']:
        return True
      elif choice in ['n', 'no']:
        return False
      

  def mk_dir_conf(self, init_directory):
    if path.exists(init_directory):
      self.yes_no_input("config directory already exists: %s\n"
                        % str(init_directory) \
                        + "Are you sure to re-initalize the directory?")
      shutil.rmtree(init_directory)
    makedirs(init_directory, exist_ok=True)

  def __init__(self, parser):
    parser.add_argument('--init_directory',
                        default=DEFAULT_CONF_DIR, type=str)
    args = parser.parse_args()
    self.conf_dir = args.init_directory
    self.mk_dir_conf(self.conf_dir)
    self.db_path = solve_db_path(self.conf_dir, self.db_name)
    self.conn, self.cursor = init_database(self.db_path)
    self.STATS = {
      'num_executed_exp': 0,
      'created_by': uname()
    }

    with self.conn:
      self.execute(
        """
        CREATE TABLE metadata (
        json JSON
        )
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

      self.conn.commit()

  def close_db(self):
    conn.close()
