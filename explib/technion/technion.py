"""

Data obtained from:
    http://tx.technion.ac.il/~erev/Comp/Comp.html

The variables are organized as follows:

ID: subject
order: order of the problem
trial: order of the sample
group: each cohort saw different set of 30 problems
set: estimation or competition dataset
sampkey: sampled key, either safe (S) or risky (R)
sampout: outcome of sample
finalr: final choice, either safe (0) or risky (1)
med, high, low, phigh: parameters of the problem

"""
import os
import numpy as np
import pandas as pd
from copy import deepcopy

pth = os.path.dirname(__file__) + "/"
if pth=='/': pth='./'

DATAFILE_COMP = 'samplingcomp.csv'
DATAFILE_EST  = 'samplingest.csv'
df = None
gdf = None
problems = None
subjects = None


def load_data(dataset):
    global df, gdf, problems, problems_srt, gambledf, subjects
    if dataset is 'comp':
        df = pd.read_table(pth+DATAFILE_COMP, sep=',')
    elif dataset is 'est':
        df = pd.read_table(pth+DATAFILE_EST, sep=',')
    else:
        print 'Dataset is either "est" or "comp"'
        return


    df['ev_s'] = df['med']
    df['ev_r'] = df['high'] * df['phigh'] + df['low'] * (1 - df['phigh'])

    # treat
    df['H'] = 1 * (df['ev_r'] > df['ev_s'])
    df['choseH'] = 1 * (df['finalr'] == df['H'])

    #
    df['sampledR'] = 1 * (df['sampkey']=='R')
    df['sampledH'] = 1 * (df['sampledR'] == df['H'])

    problems = df['Problem'].unique()
    subjects = df['ID'].unique()

    gdf = df.groupby(['ID', 'Problem']) \
            .size() \
            .reset_index()
    acc = df.groupby(['ID', 'Problem']) \
            .apply(lambda d: d.iloc[0]['choseH']) \
            .values
    gdf['choseH'] = acc
    gdf.columns = ['ID', 'Problem', 'samplesize', 'choseH']

    gambledf = pd.DataFrame([[gid, domain(gid), totalvar(gid), diffvar(gid)] for gid in problems],
                            columns=['Problem', 'domain', 'var', 'diffvar'])
    problems_srt = gambledf.sort_values(by=['domain', 'var'])['Problem'].values

    return


def get_options(gid):
    a = np.array(df[df['Problem']==gid].iloc[0][['med', 'low', 'high', 'phigh']].values)
    arr = [[[a[0], 1.], [0., 0.]],
           [[a[2], a[3]], [a[1], 1. - a[3]]]]
    evs = [a[0], a[2] * a[3] + a[1] * (1. - a[3])]

    # make sure first option is L, second is H
    if evs[0] > evs[1]:
        options = [arr[1], arr[0]]
    else:
        options = [arr[0], arr[1]]

    return np.array(options)


def totalvar(gid):
    opt = get_options(gid)
    evs = map(lambda o: np.dot(o[:,0], o[:,1]), opt)
    evar = np.array([np.dot(o[:,1], o[:,0] ** 2) - evs[i] ** 2 \
                     for i, o in enumerate(opt)])
    return np.sum(evar)

def diffvar(gid):
    opt = get_options(gid)
    evs = map(lambda o: np.dot(o[:,0], o[:,1]), opt)
    evar = np.array([np.dot(o[:,1], o[:,0] ** 2) - evs[i] ** 2 \
                     for i, o in enumerate(opt)])
    return np.sqrt(evar[1]) - np.sqrt(evar[0])


def domain(gid):
    a = np.array(df[df['Problem']==gid].iloc[0][['med', 'low', 'high', 'phigh']].values)

    if np.sum(a[:3] < 0) == 3:
        domain = 'loss'
    elif np.sum(a[:3] >= 0) == 3:
        domain = 'gain'
    else:
        domain = 'mixed'
    return domain


def samplesize():
    pass


def choices():
    pass


def fitdata(dataset):
    """Collect fitdata from the desired studies for fitting.

    dataset: 'est' or 'comp'
    """

    def maxss(tofit):
        ss_A = tofit[np.where(tofit[:,0]==0)[0],1]
        ss_B = tofit[np.where(tofit[:,0]==1)[0],1]
        max_t = np.max([np.max(ss_A), np.max(ss_B)]) + 1
        return max_t

    fitdata = []

    for gid in problems:
        d = gdf[gdf['Problem'] == gid][['choseH', 'samplesize']]
        d['samplesize'] = d['samplesize'] - 1
        d['group'] = 0
        tofit = d.values

        fitdata.append({'gid': gid,
                        'group': 0,
                        'options': get_options(gid),
                        'max_t': maxss(tofit),
                        'data': tofit})

    return fitdata


