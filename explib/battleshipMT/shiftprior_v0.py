
#!/usr/bin/python2.7
"""
Some general functions for loading data from MTurk Battleship experiment

March, 2012
"""
import os
from mypy.datautil import datadir
from numpy import *

BASEDIR = "%s/exp-mturk/shift-prior-v0" % datadir()

SUBJECTS = [480, 481, 482, 483, 484]

N_BLOCKS = 4
N_GAMES_PER_BLOCK = 6
BIASTYPES = ["unbiased","long","thin","sameshape"]

BIASBLOCK = {
             480: [2, 0, 2, 0],
             481: [1, 0, 1, 0],
             482: [0, 3, 0, 3],
             483: [2, 0, 2, 0],
             484: [0, 1, 0, 1]
            }

GAMESPLAYED = {(480,0): range(6),
               (480,1): range(6),
               (480,2): range(6),
               (480,3): range(6),
               (481,0): range(6),
               (481,1): range(6),
               (481,2): range(1,6),
               (481,3): range(6),
               (482,0): range(6),
               (482,1): range(6),
               (482,2): range(6),
               (482,3): range(6),
               (483,0): range(6),
               (483,1): range(6),
               (483,2): range(6),
               (483,3): range(6),
               (484,0): [0,1,2,3,5],
               (484,1): range(6),
               (484,2): [1,2,3,4,5],
               (484,3): range(6),
              }

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

