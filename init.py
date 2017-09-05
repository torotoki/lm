from os import path, makedirs, uname
from utils import solve_db_path, init_database

DEFAULT_DB_NAME = 'loginfo.db'
DEFAULT_CONF_DIR = './.lm'

class Initializer:
  db_name = DEFAULT_DB_NAME
  conn = None
  cursor = None
  stats = {}

  def mk_dir_conf(self, init_directory):
    init_dir = path.dirname(args.init_directory)

    if path.exists(init_dir):
      raise RuntimeError("Error: config directory already exists:", init_dir)

    makedirs(init_dir)

  def execute(self, query):
    print(query)
    return self.conn.execute(query)


  def __init__(self, parser):
    parser.add_argument('--init_directory',
                        default=DEFAULT_CONF_DIR, type=str)
    args = parser.parse_args()
    self.mk_dir_conf(args.init_directory)
    self.db_path = self.solve_db_path(conf_dir, db_name)
    self.conn, self.cursor = init_database(db_path)
    self.STATS = {
      'num_executed_exp': 0,
      'created_by': uname
    }

    with conn:
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
        """ % self.STATS
      )

      conn.commit()

  def close_db(self):
    conn.close()
