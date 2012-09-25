#!/usr/bin/python2.7
"""
Some general functions for loading data from Ternary Antenna Learning experiments

December, 2011
"""
from mypy.datautil import datadir

BASEDIR = "%s/exp/ternary-v5.1" % datadir()

def setdatadir(expversion):
    global BASEDIR
    BASEDIR = "%s/exp/ternary-v%s" % (datadir(), expversion)

def loadsamples(subj=None):
    if subj==None:
        return None
    else:
        fp = open("%s/%s.dat" % ( BASEDIR, subj ), "r")
        data = fp.readlines()
        fp.close()

        obs = []
        for line in data:
            l = line.split(' ')
            if l[0]==str(subj) and l[1]=='1':
                obs.append( map(int, [l[2], l[3], l[7]]) )

        return obs
