import os
import numpy as np
import pandas as pd
pth = os.path.dirname(__file__) + "/"
if pth=='/': pth='./'

data = pd.read_csv(pth + 'dfe_by_game.csv')
gamble_lab = data['gamble_lab'].unique()

data_by_gamble = pd.read_csv(pth + 'dfe_by_gamble.csv')


# sort by problem type
gambles = data[data['partid']==1]
gambles_srt = gambles.sort(['domain', 'pairtype', 'session'])
gamble_lab_srt = gambles_srt['gamble_lab']



def subjects():
    data = load_data()
    return data['partid'].unique()


def get_options(gid):
    gdata = data_by_gamble[data_by_gamble['gid']==gid]
    L = np.array([gdata[['L_x1', 'L_p1']].values, gdata[['L_x2', 'L_p2']].values, gdata[['L_x3', 'L_p3']].values]).reshape((3,2))
    H = np.array([gdata[['H_x1', 'H_p1']].values, gdata[['H_x2', 'H_p2']].values, gdata[['H_x3', 'H_p3']].values]).reshape((3,2))
    return [L, H]

def condition(sid):
    return data[data.partid==sid]['group'].values[0]


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
    df = pd.read_csv(pth + 'dfe.csv')
    df['session'] = df['gamble_lab'].apply(session_from_label)
    df['game'] = df['gamble_lab'].apply(game_from_label)
    df = df[df['session'] < 22] # restrict to first 21 sessions
    df = df.sort(['partid', 'session', 'gamble_ind', 'sample_ind'])
    return df


def load_data_by_game():
    return pd.read_csv('dfe_by_game.csv')


"""
def gambles():
    data = load_data_by_game()
    gambles = data[data['partid']==1]
    gambles_srt = gambles.sort(['domain', 'pairtype', 'session'])
    return gambles_srt
"""


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


def fitdata():
    """Compile data for fitting."""

    def maxss(tofit):
        ss_A = tofit[np.where(tofit[:,0]==0)[0],1]
        ss_B = tofit[np.where(tofit[:,0]==1)[0],1]
        max_t = np.max([np.max(ss_A), np.max(ss_B)]) + 1
        return max_t

    fitdata = []

    for ig, grp in enumerate(['old', 'yng']):

        for gid in gamble_lab_srt:

            gdata = data[(data['gamble_lab']==gid) & (data['group']==grp)]

            tofit = []
            for obs in gdata[['decision', 'samplesize', 'group']].values:
                choice = 0 if obs[0]=='L' else 1
                group = 0 if obs[2]=='old' else 1
                samplesize = obs[1]
                tofit.append([choice, samplesize, group])
            tofit = np.array(tofit)

            fitdata.append({'gid': gid,
                            'group': ig,
                            'options': get_options(gid),
                            'max_t': maxss(tofit),
                            'data': tofit})

    return fitdata


def subject_fitdata(sid):

    fitdata = []
    for gid in gamble_lab_srt:
        gdata = data[(data['partid']==sid) & (data['gamble_lab']==gid)]
        tofit = []
        for obs in gdata[['decision', 'samplesize', 'group']].values:
            choice = 0 if obs[0]=='L' else 1
            group = 0 if obs[2]=='old' else 1
            samplesize = obs[1]
            tofit.append([choice, samplesize, group])
        if tofit != []:
            tofit = np.array(tofit)

            if len(tofit)==0:
                max_t = 1
            else:
                max_t = tofit[0][1] + 1

            #for obs in tofit:
            #    fitdata.append([sid, gid, max_t, obs[2], obs[0], obs[1]])

            fitdata.append({'gid': gid,
                            'group': group,
                            'options': get_options(gid),
                            'max_t': max_t,
                            'data': tofit})

    #df = pd.DataFrame(fitdata, columns=['sid', 'probid', 'max_t', 'group', 'choice', 'samplesize'])

    return fitdata


def session_fitdata(session):

    fitdata = []
    sdata = data[data.session==session]
    for gid in sdata['gamble_lab'].unique():
        gdata = sdata[sdata['gamble_lab']==gid]
        tofit = []
        for obs in gdata[['decision', 'samplesize', 'group']].values:
            choice = 0 if obs[0]=='L' else 1
            group = 0 if obs[2]=='old' else 1
            samplesize = obs[1]
            tofit.append([choice, samplesize, group])
        if tofit!=[]:
            tofit = np.array(tofit)
            if len(tofit)==0:
                max_t = 1
            else:
                max_t = np.max(tofit[:,1]) + 1

            fitdata.append({'gid': gid,
                            'group': 0, #!fix!
                            'options': get_options(gid),
                            'max_t': max_t,
                            'data': tofit})

    return fitdata


def choices(sid):
    observed = subject_fitdata(sid)
    dec = []
    for gid in gamble_lab_srt:
        gd = filter(lambda d: d['gid']==gid, observed)
        if len(gd) == 0:
            dec.append(np.nan)
        else:
            if gd[0]['data'] != []:
                dec.append(gd[0]['data'][0][0])
            else:
                dec.append(np.nan)
    return np.array(dec)


def choices_by_type(sid):
    dec = choices(sid)
    return [np.nanmean(dec[:21]), np.nanmean(dec[21:42]), np.nanmean(dec[42:63]), np.nanmean(dec[63:])]


if __name__=='__main__':

    #data = sampledata_by_subject()
    print getoptions('S1G1')

