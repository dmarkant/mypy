import os
import json
import numpy as np


CHOICE_PROP = [0.88, 0.44, 0.28, 0.56, 0.20, 0.12]


GAMBLES = [[np.array([[3, 1.], [0., 0.]]),
            np.array([[4, .8], [0., .2]])],
           [np.array([[3, .25], [0., .75]]),
            np.array([[4, .2], [0., .8]])],
           [np.array([[-32, .1], [0., .9]]),
            np.array([[-3, 1.], [0., 0]])],
           [np.array([[-4, .8], [0., .2]]),
            np.array([[-3, 1.], [0., 0]])],
           [np.array([[3, 1.], [0., 0]]),
            np.array([[32, .1], [0., 0.9]])],
           [np.array([[3, .25], [0., .75]]),
            np.array([[32, .025], [0., .975]])]
           ]

bpth = os.path.dirname(__file__) + "/"
if bpth=='/': bpth='./'


pth = bpth + 'hertwig_2004.txt'
pth_json = bpth + 'hertwig_2004.json'

def parse_to_json():

    with open(pth, 'r') as f:
        lines = [line.lstrip('\t').rstrip() for line in f.readlines()[1:]]

    data = [[], [], [], [], [], []]

    for line in lines:

        cols = line.split('\t')

        problem_index = int(cols[0])

        if cols[1]=='Result':

            choice_outcome = int(cols[-1])
            sample_outcomes = [int(o) for o in cols[3:-1] if o!='']

            # append everything to the data list for this problem
            data[problem_index-1].append({'samplesize': samplesize,
                                          'samples': samples,
                                          'sample_outcomes': sample_outcomes,
                                          'choice': choice,
                                          'choice_outcome': choice_outcome})

        else:
            choice = int(cols[-1])
            samples = [int(s) for s in cols[3:-1] if s!='']
            samplesize = int(cols[2])

    with open(pth_json, 'w') as f:
        f.writelines(json.dumps(data))


def load():
    with open(pth_json, 'r') as f:
        data = json.load(f)
    return data


def get_options(pid):
    return GAMBLES[pid]


def samplesize(pid):
    data = load()[pid]
    return [p['samplesize'] for p in data]


def choices(pid):
    data = load()[pid]
    return map(int, [p['choice'] for p in data])
