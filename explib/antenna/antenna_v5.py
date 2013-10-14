#!/usr/bin/python2.7
"""
Some general functions for loading data from Antenna learning experiment

May 2012
"""
from os import listdir
from mypy.datautil import *
from numpy import *
from numpy.linalg import *
from random import sample, shuffle
import gzip
#import matplotlib
#import matplotlib.pyplot as plt


BASEDIR = "%s/exp/antenna-v5" % datadir()

# location of data for each condition
DIR = ["RB/A","RB/P","RB/Y1","RB/Y2","II/A","II/P","II/Y1","II/Y2"]

# experiment settings
N_BLOCKS = 8
N_TRAIN_TRIALS_PER_BLOCK = 16
N_TEST_TRIALS_PER_BLOCK = 32
TEST_TRIALS = [i*N_TRAIN_TRIALS_PER_BLOCK-1 for i in range(1,N_BLOCKS+1)]    # final training trials in each block
PROTOSUBJ = [0,120,0,0,10,122,10,10]

# conditions
RB_A = 0
RB_P = 1
RB_Y1 = 2
RB_Y2 = 3
II_A = 4
II_P = 5
II_Y1 = 6
II_Y2 = 7

CONDITIONS = [RB_A,RB_P,RB_Y1,RB_Y2,II_A,II_P,II_Y1,II_Y2]

# trial types
TRAINTRIAL = 1
TESTTRIAL = 2

# mean accuracy
EXPACC = {  RB_A: array([0.7758,0.8415,0.8760,0.9105,0.9299,0.9364,0.9331,0.9385]),
            RB_P: array([0.7604,0.8385,0.8593,0.8729,0.8604,0.8739,0.8552,0.8604]),
            RB_Y1:array([0.8010,0.8072,0.8468,0.8218,0.8479,0.8312,0.8489,0.8833]),
            II_A: array([0.6427,0.6843,0.6677,0.7,0.725,0.7166,0.7229,0.7281]),
            II_P: array([0.6666,0.7302,0.7072,0.7072,0.7052,0.6947,0.7145,0.725]),
            II_Y1:array([0.6218,0.6416,0.6031,0.6468,0.6479,0.6458,0.6583,0.6802])
         }

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


CACHE_BVNPDF    = {}
CACHE_BVNPDF_X  = {}

def bvnpdf(x, rule, force=False):

    if not force and (rule, tuple(x)) in CACHE_BVNPDF_X:

        return CACHE_BVNPDF_X[(rule,tuple(x))]
    
    else:
    
        mean1, covar1 = rule
        m = array(mean1)
    
        if not force and rule in CACHE_BVNPDF:

            a, b1, covarI = CACHE_BVNPDF[rule]

        else:

            covar   = matrix(covar1)
            D       = sqrt(det(covar))
            covarI  = covar.I

            a       = (1.0/((2.0*pi) * D))
            #a       = (1.0/((2.0*pi)**(len(x)/2.0) * D))
            b1      = float(exp(-0.5*dot(dot((m-m),covarI),m-m)))

            CACHE_BVNPDF[rule] = [a, b1, covarI]
                
        b=float(exp(-0.5*dot(dot((x-m),covarI),x-m)))
        r = (a*b)/(a*b1)
        CACHE_BVNPDF_X[(rule,tuple(x))] = r
        return r

        

    #a= (1.0/((2.0*pi)**(len(x)/2.0) * D))


    #print "new"
    #print "a:\t", a
    #print "b:\t", b
    #print "b1:\t", b1


    #a1= (1.0/((2.0*pi)**(len(x)/2.0) * D))
    #b1=float(exp(-0.5*dot(dot((m-m),covarI),m-m)))

    #a= (1.0/((2.0*pi)**(len(x)/2.0)*sqrt(det(covar))))
    #b=float(exp(-0.5*dot(dot((x-m),covar.I),x-m)))
    #a1= (1.0/((2.0*pi)**(len(x)/2.0)*sqrt(det(covar))))
    #b1=float(exp(-0.5*dot(dot((m-m),covar.I),m-m)))

    #print "old"
    #print "a:\t", a
    #print "b:\t", b
    #print "a1:\t", a1
    #print "b1:\t", b1_set
    
    #print dummy

    #return (a*b)/(a*b1)

def generatetestdata():
    test_order = sample(range(N_BLOCKS), N_BLOCKS)

    # load test items, randomize
    fp = open("%s/testset_pseudo.dat" % BASEDIR,"r")
    testseq = map(lambda s: map(lambda i: int(i), s.rstrip("\n").split("\t")), fp.readlines())
    randomized=[]
    for index in test_order:
        subset = reshape(testseq[index],(32,2))
        order=range(len(subset))
        shuffle(order)
        newsubset=[]
        for i in order:
            newsubset.append(list(subset[i]))
        randomized.append(newsubset)            

    return array(randomized)

def classify_RB( x ):
    if x[0] <= 299: return 0
    else:           return 1

def classify_II( x ):
    if x[1] >= x[0]:    return 0
    else:               return 1


class AntennaData:
    """Imports subject data and gets accuracy curves"""
    def __init__(self, subj=None, cond=None, outfile=None, uniformtest=True):
        self.subj = subj
        self.cond = cond
        self.loaddata()
        #self.accuracy()

        if uniformtest:     self.get_uniform_testset()

        if outfile!=None:   self.writetofile(outfile)

        if self.rule == (((220, 300), ((2000, 0), (0, 9000))), ((380, 300), ((2000, 0), (0, 9000)))):
            self.classify = classify_RB
        elif self.rule == (((250, 350), ((4538, 4463), (4463, 4538))), ((350, 250), ((4538, 4463), (4463, 4538)))):
            self.classify = classify_II

    def loaddata(self):
        fp = open(rawfile(self.subj,self.cond), "r")
        lines = fp.readlines()
        fp.close()

        l = lines[3].lstrip('Rule: ')
        l = l.replace('[','(')
        l = l.replace(']',')')
        self.rule = eval(l)
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

    def get_uniform_testset(self):
        Y = []
        start = 5
        end = 599-start
        d = (end-start)/9

        for i in range(start,end+1,d):
            for j in range(start,end+1,d):
                Y.append([i, j])

        #print Y
        #print len(Y)
        #print dummy
        self.Y = array([Y])
        self.get_test_labels()

    def get_test_labels(self):
        self.Y_labels = []
        for b in range(len(self.Y)):
            Y_b = self.Y[b,:,:2]
            self.Y_labels.append( array([self.classify(y) for y in Y_b]) )

    def classify(self, x):
        """Using category rule, classify item x"""
        pa, pb = [bvnpdf(x, rule, force=False) for rule in self.rule]
        if pa >= pb:    return 0
        else:           return 1

    def plotsamples(self, obs):
        obs = array(obs)

        pos = []
        neg = []
        for x in obs:
            if x[2]==0:
                pos.append(x[:2])
            else:
                neg.append(x[:2])

        pos = array(pos)
        neg = array(neg)

        fig = plt.figure()
        if len(pos)>0: plt.plot(pos[:,0], pos[:,1], 'r+')
        if len(neg)>0: plt.plot(neg[:,0], neg[:,1], 'b+')

        plt.axis([0, 600, 0, 600])
        plt.show()


    def plotrule(self):
        X = arange(0,600,10)
        Y = arange(0,600,10)
        Z = []

        pos = []
        
        neg = []

        for x in X:
            #Z.append([])
            for y in Y:
                label = self.classify([x,y]) 
                if label==0:
                    pos.append( [x,y] )
                else:
                    neg.append( [x,y] )
                #Z[-1].append( round(self.likelihood(array([[x,y,0]]), h)) )

        pos = array(pos)
        neg = array(neg)

        fig = plt.figure()
        if len(pos)>0: plt.plot(pos[:,0], pos[:,1], 'r+')
        if len(neg)>0: plt.plot(neg[:,0], neg[:,1], 'b+')

        plt.axis([0, 600, 0, 600])
        plt.show()



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


