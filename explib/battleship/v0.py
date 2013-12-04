#!/usr/bin/python2.7
"""
Some general functions for loading data from Battleship experiment

September, 2011
"""
import os
from mypy.datautil import datadir
from numpy import *

BASEDIR = "%s/exp/battleship-v0" % datadir()

TRIALTYPE_FN = "%s/trialtype.csv" % BASEDIR

SUBJECTS = [1, 4, 5, 8, 9, 12, 13, 16, 24, 29, 32, 45, 47, 51, 53, 54, 56, 58, 59, 60, 61, 64, 66, 67, 68, 69, 70, 72, 73, 74]

GAMESPLAYED = {1: range(30),
               4: range(21),
               5: range(30),
               8: range(16),
               9: range(23),
               12: range(21),
               13: range(26),
               16: range(16),
               24: range(22),
               25: [0,1,2,3,4,5,6,7,8,12,13,14,15,16,19,20,21,22,23,28,29],
               29: range(25),
               32: range(30),
               45: range(30),
               47: range(30),
               51: range(28),
               53: range(25),
               54: range(27),
               56: range(23),
               58: range(27),
               59: filter(lambda g: g!=6, range(30)),
               60: range(1,21),
               61: range(30),
               64: range(22),
               66: range(26),
               67: range(30),
               68: range(25),
               69: range(30),
               70: range(30),
               72: range(25),
               73: range(22),
               74: range(30)
              }

#------------------------------ 
# LOAD DATA
#------------------------------ 
def setdatadir(dir):
    global BASEDIR
    BASEDIR = dir

def gamesplayed(subj): return GAMESPLAYED[subj]

def trialtype(subj, game): 

    if not os.path.exists(TRIALTYPE_FN):
        print "missing trial type file"
        return
    else:
        fp = open(TRIALTYPE_FN,"r")
        lines = fp.readlines()
        fp.close()
        
        r = None
        for line in lines:
            l = line.split(',')
            if int(l[0])==subj and int(l[1])==game:
                r = map(int, l[2:])

    return r

def loadgameboard(subj=None, game=None):
    fp = open('%s/subject%s/game%s/gameboard%s.txt' % (BASEDIR,subj,game,game), 'r')
    board = reshape([[int(s) for s in line.rstrip(' \n').split(' ')] for line in fp.readlines()], (1,100))[0]
    fp.close()
    return board

def loadsamples(subj=None, game=None, linear=True):
    if os.path.exists('%s/subject%s/game%s/samples%s_norep.txt' % (BASEDIR,subj,game,game)):
        spath = '%s/subject%s/game%s/samples%s_norep.txt' % (BASEDIR,subj,game,game)
    else:
        spath = '%s/subject%s/game%s/samples%s.txt' % (BASEDIR,subj,game,game)
    print "loading samples from", spath
    
    if not os.path.exists(spath):
        print "no samples found!"
        return None
    else:
        fp = open(spath, 'r')
        samples = [[int(s) for s in line.split(' ')[3:6]] for line in fp.readlines()]
        fp.close()
        if linear:
            X = [[toindex(s[0:2],10), s[2]] for s in samples]
        else:
            X = samples
        return X

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

