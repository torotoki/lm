#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from dbhelper import ExperimentManager

class LSCommand:
  show_long_flag = False
  manager = None

  def __init__(self, parser):
    parser.add_argument('-l', '--long', default=False, type=bool)
    args = parser.parse_args()
    self.show_long_flag = args.long

    self.manager = ExperimentManager()

  def printout(self):
    results = self.manager.get_json_list()

    # Very ad-hoc output
    pprint(results)
    # row_format ="{:>15}" * (len(teams_list) + 1)

    # print (row_format.format("", *teams_list))

    # for team, row in zip(teams_list, data):
    #   print (row_format.format(team, *row))
