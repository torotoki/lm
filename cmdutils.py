from os import system, path, makedirs

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

  def __init__(self, parser):
    parser.add_argument('_run', type=str)  # run command
    parser.add_argument('commands', type=str)
    parser.add_argument('--use_nohup', default=True, type=bool)
    args = parser.parse_args()
    self.commands = args.commands
    self.use_nohup = args.use_nohup

    log_dir, lognum = self.decide_log_dir()
    self.create_log_dir(log_dir)
    self.log_dir = log_dir
    self.lognum = lognum
    self.args = args

    self.stdout_path = log_dir + '/' + 'stdout.txt'
    self.stderr_path = log_dir + '/' + 'stderr.txt'


  def decide_log_dir(self):
    num = 1
    return ("logs/%d.exp" % num, num)

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
         "%s" % self.commands,
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
