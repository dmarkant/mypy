#!/usr/bin/python2.7
"""
Sampling norms

September 2011
"""
from numpy import *
from random import random

def entropy(dist):
    """Entropy of discrete probability distribution"""
    dist = array([max(d,10e-100) for d in dist])
    return dot(dist,(log(1.0/dist) * (1.0/log(2.0))).T)

def margin(l):
    t = float(sum(l))
    l = [el+1e-10 for el in l]  # avoid log(0)    
    l = sort([el/t for el in l])
    return 1.0-(l[-1]-l[-2])

def confirm(l):
    l = [el+1e-10 for el in l]  # avoid log(0)
    t = float(sum(l))
    l = [el/t for el in l]
    return max(l)

def pairwisemargin(l):
    t = float(sum(l))
    l = [el+1e-10 for el in l] # avoid log(0)
    pwlm = map(lambda pair: sum(pair)*(1-(pair[1]-pair[0])), [sort([l[0]/t, l[1]/t]), sort([l[0]/t, l[2]/t]), sort([l[1]/t, l[2]/t])])
    return pwlm

def probchoice(V, d):
    """Make probabiilistic choice based on array of sampling values V and determinism d
    
       Returns index of choice (not actual sample, which is tied to a sampling set)
    """
    top = [exp(d*v) for v in V]
    bottom = sum(top)
    cp = [t/bottom for t in top]
    return sum(1*(random() < cumsum(cp)))-1

