from lm.dbhelper import ExperimentManager

def rm(parser):
  parser.add_argument('specification', type=str)
  args = parser.parse_args()

  specification = args.specification

  manager = ExperimentManager()
  manager.remove_data(specification)
