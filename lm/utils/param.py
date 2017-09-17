from __future__ import print_function
from random import randrange, choice, random
import sys
import json

def load_criteria(filename):
  with open(filename) as f:
    j = json.loads(f)
  if not (j.get('header') or j.get('criteria')):
    raise RuntimeError('Some attribute not found:', filename)

  header = j['header']
  footer = j.get('footer') or ''
  multicomponent = j.get('multicomponent_criteria')
  N = j.get('N')
  # if N:
  #   random_param(header, j['criteria'], footer,
  #                N, multicomponent)
  # else:
  #   random_param(header, j['criteria'],  footer,
  #                multicomponent=multicomponent)

def random_param(header, criteria, footer, N=40):
  commands = []
  for i in range(N):
    command = [header]
    ranges = criteria.get('range_criteria')
    choices = criteria.get('choice_criteria')
    multicomp = critria.get('multicomponent_criteria')
    if ranges:
      for key, cri in ranges.items():
        command.append('--' + key)
        if len(cri) == 3:
          opt = randrange(cri[0], cri[1]), cri[2])  ## random
        elif len(cri) == 2:
          opt = randrange(cri[0], cri[1])
        command.append(opt)
    if choices:
      for key, cri in choices.items():
        command.append('--' + key)
        if not isinstance(cri, list):
          opt = cri
        else:
          opt = choice(choices)
        command.append(opt)
    if multicomp:
      for criteria_set in multicomp:
        for key, cri in criteria_set.items():
          command.append('--' + key)
          opt = cri[0]  # int
          command.append(opt)
      
    command.append(footer)
    commands.append(command)
  return commands
