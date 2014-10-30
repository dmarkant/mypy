import os
import numpy as np
import pandas as pd

def streak_lengths(samples):
    
    lengths = []
    current_length = 0
    for trial, option in enumerate(samples):

        if trial==0:
            current_length = 1
        else:
            if option == samples[trial - 1]:
                current_length += 1
            else:
                lengths.append(current_length)
                current_length = 1
    lengths.append(current_length)
    return np.array(lengths)


def session_from_label(label):
    return int(label.lstrip('S').split('G')[0])


def game_from_label(label):
    return int(label.lstrip('S').split('G')[1])


def load_data():
    df = pd.read_csv('dfe.csv')
    df['session'] = df['gamble_lab'].apply(session_from_label)
    df['game'] = df['gamble_lab'].apply(game_from_label)
    df = df[df['session'] < 22] # restrict to first 21 sessions
    df = df.sort(['partid', 'session', 'gamble_ind', 'sample_ind'])    
    return df


def load_data_by_game():
    return pd.read_csv('dfe_by_game.csv')


def gambles():
    data = load_data_by_game()
    gambles = data[data['partid']==1]
    gambles_srt = gambles.sort(['domain', 'pairtype', 'session'])
    return gambles_srt


def streak_lengths_by_subject(sid):
    df = load_data()
    return df[(df['partid']==sid)].groupby('gamble_lab').apply(lambda gdf: streak_lengths(gdf['sample_opt'].values))



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

