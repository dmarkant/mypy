#!/usr/bin/python2.7
"""
Some general functions for loading data from MTurk Battleship experiment

March, 2012
"""
import os
from mypy.datautil import datadir
from numpy import *

BASEDIR = "%s/exp-mturk/shift-prior-v1.2" % datadir()

N_BLOCKS = 2
N_GAMES_PER_BLOCK = 12
BIASTYPES = ["unbiased","long","thin","sameshape"]

BIASBLOCK = {
             641: [0, 3], # done
             642: [2, 0], # done
             644: [2, 0], # done
             648: [1, 0], # done
             649: [0, 1], # done
             651: [0, 1], # done
             652: [2, 0], # done
             655: [2, 0], # done
             657: [0, 2], # done
             662: [0, 3], # done
             663: [1, 0], # done
             664: [3, 0], # done
             665: [0, 2], # done
             666: [0, 3], # done
             667: [0, 3], # done
             668: [0, 1], # done
             670: [0, 2], # done
             671: [1, 0], # done
             672: [3, 0], # done
            }


GAMESPLAYED = {
               (648,0): range(N_GAMES_PER_BLOCK),
               (648,1): [0,1,2,3,4,5,6,7,8,9,10],
               (655,0): [0,1,2,3,4,6,7,8,9,10,11],
               (655,1): range(N_GAMES_PER_BLOCK),
               (665,0): [0,1,2,3,4,5,6,7,8,9,11],
               (665,1): [0,1,2,3,4,5,6,7,8,9,11],
               (668,0): [0,1,2,3,4,5,6,8,9,10,11],
               (668,1): range(N_GAMES_PER_BLOCK),
               (670,0): [0,1,2,3,4,5,7,8,9,10,11],
               (670,1): range(N_GAMES_PER_BLOCK),
            }

for s in BIASBLOCK.keys():
    GAMESPLAYED[(s,0)] = range(N_GAMES_PER_BLOCK)
    GAMESPLAYED[(s,1)] = range(N_GAMES_PER_BLOCK)

#------------------------------ 
# LOAD DATA
#------------------------------ 
def setdatadir(dir):
    global BASEDIR
    BASEDIR = dir

def loadgameboard(subj=None, block=None, game=None):
    spath = '%s/%s.dat' % (BASEDIR,subj)
    if not os.path.exists(spath):
        print "no data file found!"
        return None
    else:
        print "loading gameboard from %s" % spath
        fp = open(spath, 'r')
        lines = filter(lambda l: len(l)>3,[ line.rstrip('\n').split(' ') for line in fp.readlines()])

        lines = filter(lambda s: s[1]==str(block) and s[2]==str(game) and s[3]=='gameboard', lines)
        fp.close()

        return map(int,lines[0][4:])


def loadsamples(subj=None, block=None, game=None):
    spath = '%s/%s.dat' % (BASEDIR,subj)
    if not os.path.exists(spath):
        print "no samples found!"
        return None
    else:
        print "loading samples from %s" % spath
        fp = open(spath, 'r')

        lines = filter(lambda l: len(l)>3,[ line.rstrip('\n').split(' ') for line in fp.readlines()])

        lines = filter(lambda s: s[1]==str(block) and s[2]==str(game) and s[3]=='sample', lines)
        fp.close()

        samples = [[int(s) for s in line[4:7]] for line in lines]
        X = [[toindex(s[0:2],10), s[2]] for s in samples]
        return X

def gamesplayed(subj=None, block=None): return GAMESPLAYED[(subj,block)]

def biastype(subj=None, block=None): return BIASTYPES[ BIASBLOCK[subj][block] ]

def biasblock(subj=None, bias="unbiased"):
    bind = BIASTYPES.index(bias)
    return BIASBLOCK[subj].index(bind)


def topairs(n, ncells):
    """Convert from linear index to coordinate"""
    a = int(n/int(ncells))
    b = n - a*ncells
    return (a,b)

def toindex(pair, ncells):
    (a,b)=pair
    return int((a%ncells)*ncells + b)

def getDataGrid(x,y):
    return [[(j,i) for i in range(0,y)] for j in range(0,x)]

