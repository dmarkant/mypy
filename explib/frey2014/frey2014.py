import os
import numpy as np
import pandas as pd


def load_data():
    return pd.read_csv('dfe.csv')


def load_data_by_game():
    return pd.read_csv('dfe_by_game.csv')


def gambles():
    data = load_data_by_game()
    gambles = data[data['partid']==1]
    gambles_srt = gambles.sort(['domain', 'pairtype', 'session'])
    return gambles_srt


def sampledata_by_subject():
    """
    Return grouped list of data, where each group is an individual subject
    """
    data = load_data()
    SUBJ = data['partid'].unique()


    sampledata = {}
    for s in SUBJ:
        sampledata[s] = []
        sdata = data[data['partid']==s]
        gset  = sdata['gamble_lab'].unique()

        for gid in gset:
            gdata = sdata[sdata['gamble_lab']==gid][['sample_opt', 'sample_out', 'decision']]

            samples = np.array([0 if it[0]=='L' else 1 for it in gdata.values])
            outcomes = np.array(gdata['sample_out'].values)
            choice = 0 if gdata.values[0][2]=='L' else 1
            sampledata[s].append({'sid': s,
                                  'gid': gid,
                                  'sampledata': samples,
                                  'outcomes': outcomes,
                                  'choice': choice})

    return sampledata



if __name__=='__main__':

    data = sampledata_by_subject()

