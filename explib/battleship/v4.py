#!/usr/bin/python2.7
"""
Some general functions for loading data from Battleship experiment

September, 2011
"""
import os
from mypy.datautil import datadir
from numpy import *

BASEDIR = "%s/exp/battleship-v4" % datadir()

#------------------------------ 
# LOAD DATA
#------------------------------ 
def setdatadir(dir):
    global BASEDIR
    BASEDIR = dir

def loaddata(subj=None):
    p = "%s/%s.dat" % (BASEDIR, subj)
    if os.path.exists(p):
        print "loading data from", p
        fp = open(p, "r")
        data = fp.readlines()
        fp.close()
        return data
    else:
        print "no data file found"

# THIS IS NOT RIGHT #
def loadgameboard(subj=None, game=None):
    fp = open('%s/subject%s/game%s/gameboard%s.txt' % (BASEDIR,subj,game,game), 'r')
    board = reshape([[int(s) for s in line.rstrip(' \n').split(' ')] for line in fp.readlines()], (1,100))[0]
    fp.close()
    return board

def loadsamples(subj=None, game=None, linear=True, norepeat=True):
    data = loaddata(subj=subj)

    samples = []
    for line in data[1:]:
        l = line.split(' ')
        if l[0]==str(subj) and l[2]==str(game) and l[3]=='1':
            if l[7]!='-1':
                samples.append( map(int, l[7:10]) )


    # check to make sure no samples are duplicated
    if norepeat:
        seen = []       # set of unique samples
        nonrep = []     # indices of non-repeated samples
        for i in range(len(samples)):
            s = samples[i]
            if seen.count(s)==0:
                seen.append(s)
                nonrep.append(i)
        samples = [ samples[i] for i in nonrep ]

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


if __name__=="__main__":
    print loadsamples(subj=11, game=0)
