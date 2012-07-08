#!/usr/bin/python2.7
"""
Some general functions for loading data from Antenna learning experiment

May 2012
"""
from os import listdir
from mypy.datautil import *
from numpy import *

BASEDIR = "%s/exp/antenna-v5" % datadir()

# location of data for each condition
DIR = ["RB/A","RB/P","RB/Y1","RB/Y2","II/A","II/P","II/Y1","II/Y2"]

# experiment settings
N_BLOCKS = 8
N_TRAIN_TRIALS_PER_BLOCK = 16
N_TEST_TRIALS_PER_BLOCK = 32

# conditions
RB_A = 0
RB_P = 1
RB_Y1 = 2
RB_Y2 = 3
II_A = 4
II_P = 5
II_Y1 = 6
II_Y2 = 7

# trial types
TRAINTRIAL = 1
TESTTRIAL = 2


#------------------------------ 
# LOAD DATA
#------------------------------ 
def setdatadir(dir):
    global BASEDIR
    BASEDIR = dir

def getsubjects(condition):
    return [int(s.rstrip('.dat')) for s in listdir("%s/%s" % (BASEDIR, DIR[condition]))]

def rawfile(subj, cond):
    return "%s/%s/%s.dat" % (BASEDIR, DIR[cond], subj)

def parsedfile(subj, cond):
    return "%s/%s/%s_parsed.dat" % (BASEDIR, DIR[cond], subj)


class AntennaData:
    """Imports subject data and gets accuracy curves"""
    def __init__(self, subj=None, cond=None, outfile=None):
        self.subj = subj
        self.cond = cond
        self.loaddata()
        self.accuracy()

        if outfile!=None: self.writetofile(outfile)

    def loaddata(self):
        fp = open(rawfile(self.subj,self.cond), "r")
        lines = fp.readlines()
        fp.close()

        self.rule = eval(lines[3].lstrip('Rule: '))
        self.data = [[int(s) for s in line.rstrip(' \n').split(' ')] for line in lines[12:]]

        self.X = []
        self.Y = []

        if self.cond==RB_A or self.cond==II_A:
            for line in self.data:
                if line[5]==TRAINTRIAL:
                    self.X.append( [line[6], line[7], line[10]] )
                elif line[5]==TESTTRIAL:
                    self.Y.append( [line[6], line[7], line[8]] )
        else:
            for line in self.data:
                if line[5]==TRAINTRIAL:
                    self.X.append( [line[6], line[7], line[8]] )
                elif line[5]==TESTTRIAL:
                    self.Y.append( [line[6], line[7], line[8]] )

        self.X = reshape(array(self.X), (N_BLOCKS, N_TRAIN_TRIALS_PER_BLOCK, 3))
        self.Y = reshape(array(self.Y), (N_BLOCKS, N_TEST_TRIALS_PER_BLOCK, 3))

    def classify(self, x):
        """Using category rule, classify item x"""
        pa, pb = [bvnpdf(x, rule) for rule in self.rule]
        if pa >= pb:
            label = 0
        else:
            label = 1
        return label

    def accuracy(self):
        """Compute accuracy curve given response data and category rule for this subject"""
        self.correct = zeros((N_BLOCKS, N_TEST_TRIALS_PER_BLOCK), int)
        for b in range(N_BLOCKS):
            for trial in range(N_TEST_TRIALS_PER_BLOCK):

                y = self.Y[b][trial][:2]
                response = self.Y[b][trial][2]
                label = self.classify( self.Y[b][trial][:2] )
                if response==label:
                    self.correct[b,trial] = 1

        # average accuracy within each training block
        self.accuracy = map(mean, self.correct)
        
    def writetofile(self, outfile):
        outdata = "subj %s\ncond %s\n" % (self.subj, self.cond)
        outdata += outformat2d(reshape(self.X, (N_BLOCKS*N_TRAIN_TRIALS_PER_BLOCK, 3)), "X")
        outdata += outformat2d(reshape(self.Y, (N_BLOCKS*N_TEST_TRIALS_PER_BLOCK, 3)), "Y")
        outdata += outformat1d(self.accuracy, "acc")
        outdata += outformat2d(self.correct, "correct")

        fp = gzip.open(outfile, "w")
        fp.writelines(outdata)
        fp.close()


