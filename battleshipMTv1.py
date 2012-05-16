#!/usr/bin/python2.7
"""
Some general functions for loading data from MTurk Battleship experiment

March, 2012
"""
import os
from mypy.datautil import datadir
from numpy import *

BASEDIR = "%s/exp-mturk/shift-prior-v1" % datadir()

SUBJECTS = [523, 524, 525, 526]

N_BLOCKS = 2
N_GAMES_PER_BLOCK = 12
BIASTYPES = ["unbiased","long","thin","sameshape"]

BIASBLOCK = {
             523: [0, 3],
             524: [0, 2],
             525: [1, 0],
             526: [0, 2],
             527: [3, 0], # sampler - usq done, need to copy
             528: [3, 0], # sampler - usq done, need to copy
             529: [0, 1], # sampler - usq done, need to copy
             532: [1, 0], # sampler - usq done, need to copy
             533: [0, 3], # sampler - usq done, need to copy
             534: [0, 2], # sampler - usq done, need to copy
             538: [1, 0], # sampler - usq done, need to copy
             541: [0, 2], # sampler - usq done, need to copy
             542: [1, 0], # sampler - usq dne, need to copy
             544: [3, 0], # sampler - usq Q
             545: [0, 3], # sampler - usq done, need to copy
             547: [0, 3], # sampler - usq done, need to copy
             548: [0, 2], # sampler - usq done, need to copy
             549: [0, 3], # sampler - usq done, need to copy
             551: [2, 0], # sampler - usq done, need to copy
             552: [0, 1], # sampler - usq done, need to copy
             553: [3, 0], 
             554: [3, 0], # done
             555: [1, 0], # done
             556: [0, 2], # done
             557: [2, 0], # done
             558: [1, 0], # done
             559: [0, 3], # done 
             560: [0, 2], # done
             561: [1, 0], # done
             562: [1, 0], # done
             563: [0, 2], # done
             564: [0, 3], # done
             565: [2, 0], # done
             566: [3, 0], # done
             567: [0, 1], # done
             568: [0, 1], # done
             575: [0, 1], # done
             576: [3, 0], # done
             578: [0, 1], # done
             579: [3, 0], # done
             584: [2, 0], # done
             585: [3, 0], # done
             586: [2, 0], # done
             587: [0, 1], # done
             589: [0, 2], # done
             591: [0, 3], # done
            }

GAMESPLAYED = {
               (523,0): range(N_GAMES_PER_BLOCK),
               (523,1): range(N_GAMES_PER_BLOCK),    
               (524,0): range(N_GAMES_PER_BLOCK),
               (524,1): range(N_GAMES_PER_BLOCK),
               (525,0): range(N_GAMES_PER_BLOCK),
               (525,1): range(N_GAMES_PER_BLOCK),    
               (526,0): range(N_GAMES_PER_BLOCK),
               (526,1): range(N_GAMES_PER_BLOCK),  
               (527,0): range(N_GAMES_PER_BLOCK),
               (527,1): range(N_GAMES_PER_BLOCK),    
               (528,0): range(N_GAMES_PER_BLOCK),
               (528,1): range(N_GAMES_PER_BLOCK),    
               (529,0): range(N_GAMES_PER_BLOCK),
               (529,1): range(N_GAMES_PER_BLOCK),    
               (532,0): range(N_GAMES_PER_BLOCK),
               (532,1): range(N_GAMES_PER_BLOCK),    
               (533,0): [0,1,2,3,4,5,7,8,9,10,11],
               (533,1): [0,1,2,3,5,6,7,8,9,10,11],    
               (534,0): range(N_GAMES_PER_BLOCK),
               (534,1): range(N_GAMES_PER_BLOCK),    
               (538,0): [0,1,2,3,4,5,7,8,9,11],
               (538,1): range(N_GAMES_PER_BLOCK),
               (541,0): range(N_GAMES_PER_BLOCK),
               (541,1): range(N_GAMES_PER_BLOCK),
               (542,0): [0,2,3,4,5,6,7,8,9,10,11],
               (542,1): range(N_GAMES_PER_BLOCK),
               (544,0): range(N_GAMES_PER_BLOCK),
               (544,1): range(N_GAMES_PER_BLOCK),
               (545,0): range(N_GAMES_PER_BLOCK),
               (545,1): range(N_GAMES_PER_BLOCK),
               (547,0): range(N_GAMES_PER_BLOCK),
               (547,1): range(N_GAMES_PER_BLOCK),
               (548,0): range(N_GAMES_PER_BLOCK),
               (548,1): range(N_GAMES_PER_BLOCK),
               (549,0): range(N_GAMES_PER_BLOCK),
               (549,1): range(N_GAMES_PER_BLOCK),
               (551,0): range(N_GAMES_PER_BLOCK),
               (551,1): range(N_GAMES_PER_BLOCK),
               (552,0): range(N_GAMES_PER_BLOCK),
               (552,1): range(N_GAMES_PER_BLOCK),
               (553,0): range(N_GAMES_PER_BLOCK),
               (553,1): range(N_GAMES_PER_BLOCK),
               (554,0): range(N_GAMES_PER_BLOCK),
               (554,1): range(N_GAMES_PER_BLOCK),
               (555,0): [0,1,2,3,4,5,6,7,8,11],
               (555,1): range(N_GAMES_PER_BLOCK),
               (556,0): range(N_GAMES_PER_BLOCK),
               (556,1): range(N_GAMES_PER_BLOCK),
               (557,0): [0,1,2,3,4,5,6,7,9,10,11],
               (557,1): range(N_GAMES_PER_BLOCK),
               (558,0): [0,2,3,4,5,6,7,9,10,11],
               (558,1): [0,1,2,3,4,5,7,8,9,10,11],
               (559,0): range(N_GAMES_PER_BLOCK),
               (559,1): range(N_GAMES_PER_BLOCK),
               (560,0): [0,1,2,3,4,5,6,7,9],
               (560,1): [0,1,4,5,7,10,11],
               (561,0): range(N_GAMES_PER_BLOCK),
               (561,1): [0,1,2,3,4,5,6,7,8,9,10],
               (562,0): range(N_GAMES_PER_BLOCK),
               (562,1): range(N_GAMES_PER_BLOCK),
               (563,0): range(N_GAMES_PER_BLOCK),
               (563,1): range(N_GAMES_PER_BLOCK),
               (564,0): range(N_GAMES_PER_BLOCK),
               (564,1): range(N_GAMES_PER_BLOCK),
               (565,0): range(N_GAMES_PER_BLOCK),
               (565,1): [0,1,3,4,5,6,7,8,9,10,11],
               (566,0): [0,1,2,3,5,7,8,9,10,11],
               (566,1): [0,1,3,4,5,6,7,8,9,10,11],
               (567,0): range(N_GAMES_PER_BLOCK),
               (567,1): range(N_GAMES_PER_BLOCK),
               (568,0): range(N_GAMES_PER_BLOCK),
               (568,1): range(N_GAMES_PER_BLOCK),
               (575,0): range(N_GAMES_PER_BLOCK),
               (575,1): range(N_GAMES_PER_BLOCK),
               (576,0): range(N_GAMES_PER_BLOCK),
               (576,1): range(N_GAMES_PER_BLOCK),
               (578,0): range(N_GAMES_PER_BLOCK),
               (578,1): range(N_GAMES_PER_BLOCK),
               (579,0): range(N_GAMES_PER_BLOCK),
               (579,1): range(N_GAMES_PER_BLOCK),
               (584,0): range(N_GAMES_PER_BLOCK),
               (584,1): range(N_GAMES_PER_BLOCK),
               (585,0): range(N_GAMES_PER_BLOCK),
               (585,1): range(N_GAMES_PER_BLOCK),
               (586,0): [0,1,2,3,4,5,6,7,9,10,11],
               (586,1): [0,2,3,4,5,6,7,9,10],
               (587,0): range(N_GAMES_PER_BLOCK),
               (587,1): range(N_GAMES_PER_BLOCK),
               (589,0): range(N_GAMES_PER_BLOCK),
               (589,1): [0,1,3,4,5,6,7,8,9,10,11],
               (591,0): range(N_GAMES_PER_BLOCK),
               (591,1): range(N_GAMES_PER_BLOCK),
              }


UNBIASED_BOARDS = [
    [523,0],
    [524,0],
    [525,1],
    [526,0],
    [527,1],
    [528,1],
    [529,0],
    [532,1],
    [533,0],
    [534,0]
]
LONG_BOARDS = [
    [525,0],
    [529,1],
    [532,0],
    [538,0],
    [542,0],
    [552,1],
    [555,0],
    [558,0],
    [561,0],
    [562,0]
]
THIN_BOARDS = [
    [524,1],
    [526,1],
    [534,1],
    [541,1],
    [548,1],
    [551,0],
    [556,1],
    [557,0],
    [560,1],
    [563,1]
]
SAMESHAPE_BOARDS = [
    [523,1],
    [527,0],
    [528,0],
    [533,1],
    [544,0],
    [545,1],
    [547,1],
    [549,1],
    [553,0],
    [554,0]
]



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

