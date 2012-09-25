

#!/usr/bin/python2.7
"""
Some general functions for loading data from MTurk Battleship experiment

shift-prior-v1

March, 2012
"""
import os
from mypy.datautil import datadir
from numpy import *

BASEDIR = "%s/exp-mturk/shift-prior-v1" % datadir()

BIASTYPES = ["unbiased","long","thin","sameshape"]

BIASBLOCK = {
             524: [0, 2]
            }

GAMESPLAYED = {(524,0): range(12),
               (524,1): range(12)
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
        
        lines = filter(lambda s: s[1]==str(block) and s[2]==str(game) and s[3]=='gameboard', [ line.rstrip(' \n').split(' ') for line in fp.readlines() ])
        fp.close()
        board = eval(' '.join(lines[0][3:]))
        return board

def loadsamples(subj=None, block=None, game=None):
    spath = '%s/%s.dat' % (BASEDIR,subj)
    if not os.path.exists(spath):
        print "no samples found!"
        return None
    else:
        print "loading samples from %s" % spath
        fp = open(spath, 'r')
        lines = filter(lambda s: s[1]==str(block) and s[2]==str(game) and s[3]=='sample', [ line.rstrip(' \n').split(' ') for line in fp.readlines() ])
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

