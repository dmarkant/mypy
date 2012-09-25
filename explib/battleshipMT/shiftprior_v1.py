#!/usr/bin/python2.7
"""
Some general functions for loading data from MTurk Battleship experiment

March, 2012
"""
import os
from mypy.datautil import datadir
from numpy import *
from pandas import *

BASEDIR = "%s/exp-mturk/shift-prior-v1" % datadir()

SUBJECTS = [523, 524, 525, 526, 527, 528, 529, 532, 533, 534, 538, 541, 542, 544, 545, 547, 548, 549, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 575, 576, 578, 579, 584, 585, 586, 587, 589, 591, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 699, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 716, 717, 718]

N_BLOCKS = 2
N_GAMES_PER_BLOCK = 12
BIASTYPES = ["unbiased","long","thin","sameshape"]

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

def loaddata(subj=None):
    spath = '%s/%s.dat' % (BASEDIR,subj)
    if not os.path.exists(spath):
        print "no data file found!"
        return None
    else:
        #print "loading game data from %s" % spath        
        fp = open(spath, 'r')
        lines = [l.rstrip('\n') for l in fp.readlines()]
        fp.close()
        return lines

def getcondition(subj):
    data = loaddata(subj)
    condition = filter(lambda line: len(line)>=2 and (line[0]=="condition:" or line[1]=="condition"), [l.split(' ') for l in data])[0]
    counter =  filter(lambda line: len(line)>=2 and (line[0]=="countercond:" or line[1]=="countercond"), [l.split(' ') for l in data])[0]

    # fixing a difference in output for some subjects
    if len(condition)==2:   
        condition = int(condition[1])
        counter =   int(counter[1])
    else:                   
        condition = int(condition[2])
        counter =   int(counter[2])

    return [condition, counter]

def loadgameboard(subj=None, block=None, game=None):
    data = loaddata(subj=subj)
    if data==None: return None
    else:
        lines = filter(lambda l: len(l)>3,[ line.rstrip('\n').split(' ') for line in data])
        lines = filter(lambda s: s[1]==str(block) and s[2]==str(game) and s[3]=='gameboard', lines)
        return map(int,lines[0][4:])

def loadsamples(subj=None, block=None, game=None):
    data = loaddata(subj=subj)
    if data==None: return None
    else:
        lines = filter(lambda l: len(l)>3,[ line.rstrip('\n').split(' ') for line in data])
        lines = filter(lambda s: s[1]==str(block) and s[2]==str(game) and s[3]=='sample', lines)

        samples = [[int(s) for s in line[4:7]] for line in lines]
        X = [[toindex(s[0:2],10), s[2]] for s in samples]
        return X

def gamesplayed(subj=None, block=None):
    return list(where([len(loadsamples(subj=subj, block=block, game=g)) for g in range(N_GAMES_PER_BLOCK)])[0])

def biastype(subj=None, block=None):
    cond, counter = getcondition(subj)
    if block==0:
        if counter==0:  return BIASTYPES[0]
        else:           return BIASTYPES[cond+1]
    else:
        if counter==0:  return BIASTYPES[cond+1]
        else:           return BIASTYPES[0]

def biasblock(subj=None, bias="unbiased"):
    biases = [biastype(subj=subj, block=b) for b in [0,1]]
    if bias in biases:
        return biases.index(bias)
    else:
        return None

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

if __name__=="__main__":
    subj = 586
    #print biastype(subj=subj, block=0)
    #print biastype(subj=subj, block=1)
    #print gamesplayed(subj=subj, block=1)
    #print biasblock(subj=subj, bias="unbiased")
    #print biasblock(subj=subj, bias="long")
    #print biasblock(subj=subj, bias="thin")
    #print biasblock(subj=subj, bias="sameshape")
    
    # get a summary of all subjects
    d = []
    for subj in SUBJECTS:
        cond, counter = getcondition(subj)
        skipped0, skipped1 = [N_GAMES_PER_BLOCK-len(gamesplayed(subj=subj, block=b)) for b in [0,1]]

        d.append([subj,cond,counter,skipped0,skipped1])

    df = DataFrame.from_records(d, columns=['subj','cond','counter','skipped0','skipped1'])

    cond = df[df['counter']==1]['cond']
    print [ list(cond).count(i) for i in range(3) ]
    
