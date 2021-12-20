#!/usr/bin/python2.7
"""
Some general functions for loading data from Rocks experiment

September, 2011
"""
import os
from mypy.datautil import datadir
from numpy import *

BASEDIR = "%s/exp/rocks-v1" % datadir()

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

def loadgameboard(subj=None, game=None):
    data = loaddata(subj=subj)

    for line in data:
        l = line.split(' ')
        if len(l)>3 and l[3]!="":
            if int(l[3])==game and l[4]=="board":
                board = map(int, l[5:-1])

    return board

def loadsamples(subj=None, game=None, linear=True, norepeat=True):
    data = loaddata(subj=subj)

    samples = []
    for line in data:
        l = line.split(' ')
        if len(l)>3 and l[3]!="":
            if int(l[3])==game and l[4]=="sample":
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
    print loadsamples(subj=7, game=1)
    print loadgameboard(subj=7, game=1)
