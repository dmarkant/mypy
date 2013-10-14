#!/usr/bin/python2.7
"""
Some general functions for loading data from MTurk Battleship experiment

March, 2013
"""
import os
from mypy.datautil import datadir
from numpy import *

BASEDIR = "%s/exp-mturk/sparsity-v3" % datadir()

SUBJECTS = [0]

DATA = {}
GAMEDATA = {}

N_GAMES = 32
N_TRIALS_PER_GAME = 4
N_BLOCKS = 2

MAX_RADIUS = 200.

RADII = [0.414125584817,
         0.585662018574,
         0.754983443527,
         0.894427191]

#------------------------------ 
# LOAD DATA
#------------------------------ 
def setdatadir(dir):
    global BASEDIR
    BASEDIR = dir

def data(subj, force=False):

    if not force and subj in DATA:
        return DATA[subj]
    else:
        spath = "%s/%s.txt" % (BASEDIR, subj)

        if not os.path.exists(spath):
            print "no subject file found!"
            return None
        else:
            print "loading data from %s" % spath
            with open(spath,'r') as f:
                lines = f.readlines()
            
            DATA[subj] = [l.split(' ') for l in lines]
            return DATA[subj]

def gamedata(subj, game):

    arena = {}
    target = {}
    samples = []
    response = {}

    for line in data(subj):
        if len(line)>1 and line[1]=='0' and line[2]==str(game):

            if line[3]=='arena':
                if line[4]=='size':
                    arena['size'] = float(line[5])
                elif line[4]=='radius':
                    arena['radius'] = float(line[5])

            elif line[3]=='target':
                if line[4]=='size':
                    target['size'] = float(line[5])
                elif line[4]=='radius':
                    target['radius'] = float(line[5])
                elif line[4]=='offset':
                    target['offset'] = float(line[5])
                elif line[4]=='loc':
                    target['loc'] = (float(line[5]), float(line[6]))

            elif line[3]=='sample':
                samples.append( [float(line[4]), float(line[5]), int(line[6])] )
                
            elif line[3]=='placed':
                response['placed'] = (float(line[4]), float(line[5]))

            elif line[3]=='distance':
                response['distance'] = float(line[4])

            elif line[3]=='bonus':
                response['bonus'] = float(line[4])


    GAMEDATA[(subj,game)] = {"arena":arena,
                             "target":target, 
                             "samples":array(samples),
                             "response":response}

    return GAMEDATA[(subj,game)]

def samples(subj, game): 
    if (subj,game) in GAMEDATA:
        return GAMEDATA[(subj,game)]['samples']
    else:
        return gamedata(subj, game)['samples']

def arena(subj, game):
    if (subj,game) in GAMEDATA:
        return GAMEDATA[(subj,game)]['arena']
    else:
        return gamedata(subj, game)['arena']

def target(subj, game): 
    if (subj,game) in GAMEDATA:
        return GAMEDATA[(subj,game)]['target']
    else:
        return gamedata(subj, game)['target']

def response(subj, game): 
    if (subj,game) in GAMEDATA:
        return GAMEDATA[(subj,game)]['response']
    else:
        return gamedata(subj, game)['response']





if __name__=="__main__":

    print gamedata(0, 0)
