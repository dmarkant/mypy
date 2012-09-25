
#!/usr/bin/python2.7
"""
Some general functions for loading data from MTurk Battleship experiment

March, 2012
"""
import os
from mypy.datautil import datadir
from numpy import *

BASEDIR = "%s/exp-mturk/shift-prior-v1.1" % datadir()

N_BLOCKS = 2
N_GAMES_PER_BLOCK = 12
BIASTYPES = ["unbiased","long","thin","sameshape"]

BIASBLOCK = {
             599: [0, 2], # done
             600: [0, 1], # done
             601: [1, 0], # done
             604: [3, 0], # done
             605: [0, 1], # done
             607: [0, 2], # done
             609: [1, 0], # done
             611: [3, 0], # done
             612: [0, 2], # done
             613: [2, 0], # done
             614: [0, 3], # done
             615: [0, 3], # done
             616: [1, 0], # done.... problems??
             617: [0, 3], # done
             618: [3, 0], # done
             619: [0, 1], # done
             620: [],
             621: [1, 0], # done
             622: [0, 2], # done
             623: [3, 0], # done
             625: [1, 0], # done
             626: [2, 0], # done
             627: [1, 0], # done
             628: [2, 0], # done
             629: [0, 3], # done
             630: [3, 0], # done
             631: [0, 3], # done
             633: [0, 1], # done
            }


GAMESPLAYED = {
               (599,0): [0,1,2,3,4,5,8,9,10,11],
               (599,1): [0,1,3,4,5,6,7,8,9,10,11],
               (614,0): [0,1,2,3,4,5,6,8,9,10,11],
               (614,1): [0,1,2,4,5,7,8,9,10,11],
               (616,0): [0,1,2,3,4,6,7,8,9,10,11],
               (616,1): range(N_GAMES_PER_BLOCK),
               (617,0): [0,1,2,4,5,7,8,10,11],
               (617,1): range(N_GAMES_PER_BLOCK),
               (618,0): [0,1,2,3,4,5,6,8,9,10,11],
               (618,1): range(N_GAMES_PER_BLOCK),
               (622,0): [0,1,2,3,5,6,7,8,9,10,11],
               (622,1): [0,1,2,3,4,5,6,7,9,10,11],
               (623,0): [0,1,2,4,5,6,7,8,9,10,11],
               (623,1): range(N_GAMES_PER_BLOCK),
               (625,0): [0,1,2,3,4,5,6,7,8,9,10],
               (625,1): range(N_GAMES_PER_BLOCK),
               (627,0): range(N_GAMES_PER_BLOCK),
               (627,1): [0,1,2,3,4,5,6,7,8,10,11],
               (633,0): range(N_GAMES_PER_BLOCK),
               (633,1): [0,1,2,3,4,5,6,7,9,10,11],
            }

for s in [600,601,604,605,607,609,611,612,613,615,619,621,626,628,629,630,631]:
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

