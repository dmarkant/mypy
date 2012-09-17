
#!/usr/bin/python2.7
"""
Some general functions for loading data from MTurk Battleship experiment

March, 2012
"""
import os
from mypy.datautil import datadir
from numpy import *
from pandas import *

BASEDIR = "%s/exp-mturk/single-shape-v2" % datadir()

SUBJECTS = [85, 89, 90, 92, 93, 94, 96, 102, 105, 106, 107, 108]

HSPACE_NAMES = [ "A", "K", "N", "V", "U", "M", "C", "P" ];

def hspace_file(letter): return "../exp/templates/hspace_%s_9x9.csv" % letter

N_CELLS = 81
N_BLOCKS = 1
N_GAMES_PER_BLOCK = 40 

#------------------------------ 
# LOAD DATA
#------------------------------ 
def setdatadir(dir):
    global BASEDIR
    BASEDIR = dir

def loaddata(subj=None):
    spath = '%s/%s.txt' % (BASEDIR,subj)
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

def loadgameboard(subj=None, block=0, game=None):
    data = loaddata(subj=subj)
    if data==None: return None
    else:
        lines = filter(lambda l: len(l)>3,[ line.rstrip('\n').split(' ') for line in data])
        lines = filter(lambda s: s[1]==str(block) and s[2]==str(game) and s[3]=='gameboard', lines)
        board = map(int,lines[0][4:-1])
        return list(transpose(reshape(board, (sqrt(N_CELLS), sqrt(N_CELLS)))))

def loadsamples(subj=None, block=0, game=None):
    data = loaddata(subj=subj)
    if data==None: return None
    else:
        lines = filter(lambda l: len(l)>3,[ line.rstrip('\n').split(' ') for line in data])
        lines = filter(lambda s: s[1]==str(block) and s[2]==str(game) and s[3]=='sample', lines)

        samples = [[int(s) for s in line[4:7]] for line in lines]
        X = [[toindex([s[1],s[0]],sqrt(N_CELLS)), s[2]] for s in samples]
        return X

def gamesplayed(subj=None, block=0):
    return list(where([len(loadsamples(subj=subj, block=block, game=g)) for g in range(N_GAMES_PER_BLOCK)])[0])

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
    subj = 24
    print loadgameboard(subj=24, game=0)
    print loadsamples(subj=24, game=0)
    print gamesplayed(subj=24)
    print dummy
    
    # get a summary of all subjects
    d = []
    for subj in SUBJECTS:
        cond, counter = getcondition(subj)
        skipped0, skipped1 = [N_GAMES_PER_BLOCK-len(gamesplayed(subj=subj, block=b)) for b in [0,1]]

        d.append([subj,cond,counter,skipped0,skipped1])

    df = DataFrame.from_records(d, columns=['subj','cond','counter','skipped0','skipped1'])

    cond = df[df['counter']==1]['cond']
    print [ list(cond).count(i) for i in range(3) ]
    
