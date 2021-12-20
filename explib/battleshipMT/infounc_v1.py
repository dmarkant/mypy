import os
import json
from mypy.datautil import datadir

SUBJPATH = '%s/exp-mturk/infounc-v1' % datadir()

SUBJECTS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 17, 18, 19, 20, 21, 22, 23, \
            24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 39, 40, 41, 42, \
            43, 44, 46, 48, 49, 50]

COSTERR = 2

def topairs(n, ncells):
    """Convert from linear index to coordinate"""
    a = int(n/int(ncells))
    b = n - a*ncells
    return (a,b)

def toindex(pair, ncells):
    (a,b)=pair
    return int((a%ncells)*ncells + b)


class Subject:

    def __init__(self, id):

        self.id = id
        self.datafile = '%s/%s.dat' % (SUBJPATH, id)

        if os.path.exists(self.datafile):
            with open(self.datafile,'r') as fp:
                self.data = json.load(fp)


        self.condition = self.data['condition']
        self.trialdata = [l.split(',') for l in self.data['data'].split('\n')]

    def gamedata(self, game=None):
        return [l[5:] for l in self.trialdata if len(l)>4 and l[3]=='GAME' and int(l[4])==game]

    def gameboard(self, game=None):
        return map(int, [l[1:] for l in self.gamedata(game=game) if l[0]=='gameboard'][0])

    def samples(self, game=None):
        X = [map(int, l[1:]) for l in self.gamedata(game=game) if l[0]=='sample']
        X = [[toindex(x[:2], 10), x[2]] for x in X]
        return X

    def gamesplayed(self):

        played = []
        for g in range(30):

            samples = self.samples(game=g)
            if len(samples)>0:
                played.append(g)

        return played 

        

if __name__ == '__main__':

    s = Subject(0)
    print s.samples(game=0)
