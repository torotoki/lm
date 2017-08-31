from os import path, makedirs
import sqlite3

class Initializer:
  db_name = 'loginfo.db'

  def mk_dir(self, init_directory):
    init_dir = path.dirname(args.init_directory)

    if path.exists(init_dir):
      raise RuntimeError("Error: config directory already exists:", init_dir)

    makedirs(init_dir)


  def __init__(self, parser):
      parser.add_argument('--init_directory', default='./.lm', type=str)
      args = parser.parse_args()
      mk_dir(args.init_directory)
     # connect.
