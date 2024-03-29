#!/usr/bin/python2.7
import string, os
from shutil import copy
from inspect import getfile
from socket import gethostname
from numpy import array, cumsum
from random import random
from sqlalchemy import *
import numpy as np
import pandas as pd
"""
Generic functions for working with data
"""

DATADIR = None

##########################################
# Sys and file management
##########################################
def checkhost():
    host = gethostname().split('.')[0].lower()
    if host in ['crush','bash','fracture','slam','shatter']:
        laptop = False
        #screenres = FULLSCREENRES
    else:
        laptop = True
        #screenres = LAPTOPRES
    return laptop

def setdatadir(dir):
    global DATADIR
    print('setting data directory to %s' % dir)
    DATADIR = dir


def datadir():
    global DATADIR
    if DATADIR!=None:
        return DATADIR
    else:

        host = gethostname().split('.')[0].lower()

        if host=='smash':
            uname = "dmarkant"
            return "/Users/%s/data" % uname

        elif host.count('compute')==1:
            return "/scratch/dbm294/data"

        elif host.count('ARC')==1:
            return "/Users/markant/data"

        else:
            uname = "doug"
            return "/Users/%s/data" % uname



def copyclasshier(cls, dest):
    try:
        f = getfile(cls).rstrip('c')
        copy(f, dest)

        for bcls in cls.__bases__:
            copyclasshier(bcls, dest)
        return 1
    except:
        print("failed to copy class hierarchy")
        return 0

def checkpath(dir):
    head, tail = os.path.split(dir)
    if head!="" and head!="~" and not os.path.exists(head): checkpath(head)
    if not os.path.exists(dir): os.mkdir(dir)

def simplebackup(filename):
    if os.path.exists(filename):
        i = 1
        backup = filename+".bak%s" % i
        while os.path.exists(filename+".bak%s" % i):
            i += 1
        backup = filename+".bak%s" % i
        print("datafile exists... backing up to "+backup)
        os.rename(filename, backup)
    return



##########################################
# Data from mysql database
##########################################
def download_data_from_mysqldb(dburl, tablename, codeversion=None):
    versionname = ''
    engine = create_engine(dburl)
    metadata = MetaData()
    metadata.bind = engine
    table = Table(tablename, metadata, autoload=True)

    # want to add a conditional clause
    if codeversion is None:
        s = table.select()
    else:
        s = table.select().where(table.c.codeversion == codeversion)

    rs = s.execute()
    data = []
    for row in rs:
        data.append(row)

    df = pd.DataFrame(data, columns=table.columns.keys())
    return df


##########################################
# Frequent operations on data
##########################################
def flatten(l): return [item for sublist in l for item in sublist]

def weightedsample(w, n): return [list(random() < cumsum(w)).index(True) for _ in range(n)]

def normalize(l):
    if sum(l)==0.:
        return l
    else:
        return array(l)*(1/float(sum(l)))

##########################################
# I/O
##########################################
def outformat1d(list, name, outputprefix=""):
    s = ""
    for i in range(len(list)):
        s += outputprefix + "%s %s %s\n" % (name, i, list[i])
    return s

def outformat2d(list, name, outputprefix=""):
    s = ""
    for i in range(len(list)):
        s += outputprefix + "%s %s " % (name, i)
        for entry in list[i]:
            s += "%s " % entry
        s += "\n"
    return s

def outformatpar(pairs):
    """Take a dict of {parameter:value} pairs and format for output file"""
    s = ""
    for k in sort(pairs.keys()):
        s += "%s" % k
        if isinstance(pairs[k], list):
            for val in pairs[k]:
                s += " %s" % val
            s += "\n"
        else:
            s += " %s\n" % pairs[k]

    return s

def out2d(list, sep=" "):
    s = ""
    for i in range(len(list)):
        for j in range(len(list[i])):
            if j==0:
                s += "%s" % list[i][j]
            else:
                s += "%s%s" % (sep, list[i][j])
        s += "\n"
    return s

def writeline(fp, data):
    for item in data:
        fp.write(str(item) + ' \n')
    #fp.write('\n')
    fp.flush()

def readmatrix(fn):
    fp = open(fn,'r')
    res = []
    lines = fp.readlines()
    for line in lines:
        res.append(map(float, string.split(line[:-1])))
    fp.close()
    return res

def writematrix(data, filename):
    fp = open(filename,'w')
    for line in data:
        for item in line:
            fp.write(str(item) + ' ')
        fp.write('\n')
    fp.flush()
    fp.close()

def topairs(n, ncells):
    """Convert from linear index to coordinate"""
    a = int(n/int(ncells))
    b = n - a*ncells
    return (a,b)


##########################################
# Logging and communiques
##########################################
def sendemail(message, subject, address):
   command = "echo \""
   + message + "\" | mail -s \"" + subject + "\" " + address
   print(command)
   os.system(command)

def runcount(runindex, totalruns):
    inter = range(0,totalruns, totalruns/10)
    if runindex in inter: print("%s" % (int((100./float(totalruns))*runindex)), "%")#########################
