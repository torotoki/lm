from os import system, path, makedirs
from dbhelper import Configure

path_variable = 'LM_LOGS_PATH'

class Executor:
  ## configs:
  use_nohup = None
  hide_output = None

  args = []
  log_dir = None
  lognum = None
  commands = None
  stdout_path = None
  stderr_path = None

  conf = None

  def __init__(self, parser):
    parser.add_argument('--use_nohup', default=True, type=bool)
    args = parser.parse_args()
    self.command = args.command
    self.use_nohup = args.use_nohup

    self.conf = Configure()

    log_dir, lognum = self.decide_log_dir(self.conf)
    self.create_log_dir(log_dir)
    self.log_dir = log_dir
    self.lognum = lognum
    self.args = args

    self.stdout_path = path.join(log_dir, stdout.txt)
    self.stderr_path = path.join(log_dir, stderr.txt)


  def decide_log_dir(self, conf):
    with conf.conn:
      conf.get_and_increment_num_exp()
      num = 1
      p = path.join(log_dir, "%d.exp" % num)
    return (p, num)

  def create_log_dir(self, log_dir):
    if path.exists(path.dirname(log_dir)):
      raise RuntimeError("Error: log folder is already exists:",log_dir)
    makedirs(log_dir)

  def execute(self):
    try:
      cmd = ' '.join(
        ["{",
         "{",
         "env %s=%s" % (path_variable, self.log_dir),
         "nohup" if self.use_nohup else "",
         "%s" % self.command,
         "| tee %s;" % self.stdout_path,
         "} 3>&2 2>&1 1>&3",
         "| tee %s;" % self.stderr_path,
         "} 3>&2 2>&1 1>&3"]
      )
      print("Execute: %s" % cmd)
      state = system(cmd)
    except (KeyboardInterrupt, SystemExit):
      print ("\naborted.")
      raise
