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


pth = "/Users/doug/code/SamplingDynamics/data/Hau2008/"


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


def samplesize(study, gid):
    df_samples, df_choices = load_study(study)
    return df_samples[df_samples['problem']==(gid+1)].sort('subject').groupby('subject').apply(lambda x: len(x)).values


def choices(study, gid):
    df_samples, df_choices = load_study(study)
    c = df_choices[df_choices['problem']==(gid+1)].sort('subject')['choice'].values
    return np.abs(c - 1)


def get_options(study, gid):

    if study==1 or study==2:

        return GAMBLES_STUDY_1[gid]
