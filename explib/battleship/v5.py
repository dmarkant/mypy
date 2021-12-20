#!/usr/bin/python2.7
"""
Some general functions for loading data from Battleship experiment

September, 2011
"""
import os
from mypy.datautil import datadir
from numpy import *

BASEDIR = "%s/exp/battleship-v5" % datadir()

BIASTYPES = ["unbiased","thin","long","sameshape"]

BIASBLOCK = {1: [0, 1, 2, 3],
             2: [0, 3, 1, 2],
             3: [0, 1, 2, 3],
             4: [0, 2, 3, 1],
             5: [0, 2, 3, 1],
             6: [0, 1, 3, 2],
             7: [0, 2, 1, 3],
             8: [0, 2, 1, 3],
             9: [0, 2, 3, 1],
             10:[0, 3, 2, 1]}

GAMESPLAYED = {(1,0): range(10),
               (1,1): range(10),
               (1,2): range(10),
               (1,3): range(10),
               (2,0): range(10),
               (2,1): range(10),
               (2,2): range(10),
               (2,3): range(10),
               (3,0): range(10),
               (3,1): range(10),
               (3,2): range(10),
               (3,3): range(10),
               (4,0): range(10),
               (4,1): range(10),
               (4,2): range(10),
               (4,3): range(10),
               (5,0): [0,1,2,3,5,6,7,8,9],
               (5,1): range(10),
               (5,2): range(10),
               (5,3): range(10),
               (6,0): range(10),
               (6,1): range(10),
               (6,2): range(10),
               (6,3): range(10),
               (7,0): range(10),
               (7,1): range(10),
               (7,2): range(10),
               (7,3): range(10),
               (8,0): [0,1,2,3,4,6,7,8,9],
               (8,1): range(10),
               (8,2): range(10),
               (8,3): range(10),
               (10,0): range(10),
               (10,1): range(10),
               (10,2): range(10),
               (10,2): range(10)
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
        
        lines = filter(lambda s: s[0]==str(block) and s[1]==str(game) and s[2]=='board', [ line.rstrip(' \n').split(' ') for line in fp.readlines() ])
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
        lines = filter(lambda s: s[0]==str(block) and s[1]==str(game) and s[2]=='sample', [ line.rstrip(' \n').split(' ') for line in fp.readlines() ])
        fp.close()
        samples = [[int(s) for s in line[5:8]] for line in lines]
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

