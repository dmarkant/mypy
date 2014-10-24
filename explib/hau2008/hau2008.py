import os
import numpy as np
import pandas as pd


GAMBLES_STUDY_1 = [[np.array([[3,   1.], [0., 0.]]),   # 0 1
                    np.array([[4,   .8], [0., .2]])],  # 1 0
                   [np.array([[3,  .25], [0., .75]]),  # 1 1
                    np.array([[4,   .2], [0., .8]])],  # 0 0
                   [np.array([[-32, .1], [0., .9]]),   # 1 1
                    np.array([[-3,  1.], [0., 0]])],   # 0 0
                   [np.array([[-4,  .8], [0., .2]]),   # 1 1
                    np.array([[-3,  1.], [0., 0]])],   # 0 0
                   [np.array([[3,   1.], [0., 0]]),    # 1 1
                    np.array([[32,  .1], [0., 0.9]])], # 0 0
                   [np.array([[3,  .25], [0., .75]]),  # 1 1
                    np.array([[32,.025], [0., .975]])] # 0 0
                    ]
"""
GAMBLES_STUDY_1 = [[np.array([[4,   .8], [0., .2]]),
                    np.array([[3,   1.], [0., 0.]])],   # 0 1
                   [np.array([[4,   .2], [0., .8]]),  # 0 0
                    np.array([[3,  .25], [0., .75]])],  # 1 1
                   [np.array([[-3,  1.], [0., 0]]),   # 0 0
                    np.array([[-32, .1], [0., .9]])],   # 1 1
                   [np.array([[-3,  1.], [0., 0]]),   # 0 0
                    np.array([[-4,  .8], [0., .2]])],   # 1 1
                   [np.array([[32,  .1], [0., 0.9]]), # 0 0
                    np.array([[3,   1.], [0., 0]])],    # 1 1
                   [np.array([[32,.025], [0., .975]]) # 0 0
                    np.array([[3,  .25], [0., .75]])]]
"""


pth = os.path.dirname(__file__) + "/"
if pth=='/': pth='./'

files_sampling = ["Hau08_s1.sampling_117.0.txt",
                  "Hau08_s2.sampling_118.0.txt",
                  "Hau08_s3.sampling_119.0.txt"]

files_choice = ["Hau08_s1.choices_117.0.txt",
                "Hau08_s2.choices_118.0.txt",
                "Hau08_s3.choices_119.0.txt"]


def load_study(study):
    df_samples = pd.read_table(pth+files_sampling[study-1], sep=' ')
    df_choices = pd.read_table(pth+files_choice[study-1], sep=' ')
    return df_samples, df_choices


def subjects(study):
    df_samples, df_choices = load_study(study)
    return df_samples['subject'].unique()


def samplesize(study, gid):
    df_samples, df_choices = load_study(study)
    return df_samples[df_samples['problem']==(gid+1)].sort('subject').groupby('subject').apply(lambda x: len(x)).values


def choices(study, gid):
    df_samples, df_choices = load_study(study)
    c = df_choices[df_choices['problem']==(gid+1)].sort('subject')['choice'].values
    return np.abs(c - 1)


def get_subj_data(study, sid, gid):
    df_samples, df_choices = load_study(study)
    sdata = df_samples[(df_samples['subject']==sid) & (df_samples['problem']==(gid+1))]
    sampledata = np.abs(sdata[['option', 'outcome']].values - 1)

    choicedata = df_choices[(df_choices['subject']==sid) & (df_choices['problem']==(gid+1))]
    if len(choicedata) > 0:
        choice = np.abs(choicedata['choice'].values[0] - 1)
    else:
        choice = np.nan

    return {'sid': sid,
            'gid': gid,
            'options': GAMBLES_STUDY_1[gid],
            'samples': sampledata[:,0],
            'outcomes': sampledata[:,1],
            'choice': choice}


def sampledata_by_subject(study=1):
    """
    Return grouped list of data, where each group is an individual subject
    """
    df_samples, df_choices = load_study(study)
    SUBJ = df_samples['subject'].unique()

    sampledata = {}
    for s in SUBJ:
        sampledata[s] = []
        gset = df_samples[df_samples['subject']==s]['problem'].unique()
        for gid in gset:
            df_game = df_samples[(df_samples['subject']==s) & (df_samples['problem']==gid)]
            samples = np.abs(np.array(df_game['option'].values) - 1)
            outcomes = np.array(df_game['outcome'].values)
            choice = np.abs(df_choices[(df_choices['subject']==s) & (df_choices['problem']==gid)]['choice'].values[0] - 1)

            sampledata[s].append({'sid': s,
                                  'gid': gid,
                                  'options': GAMBLES_STUDY_1[gid-1],
                                  'samples': samples,
                                  'outcomes': outcomes,
                                  'choice': choice})
    return sampledata


def get_options(study, gid):

    if study==1 or study==2:

        return GAMBLES_STUDY_1[gid]

if __name__=='__main__':

    print sampledata_by_subject(2)
