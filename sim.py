#!/usr/bin/python
"""
General-purpose script for running simulations.

September 2011
"""
import os, gzip, sys
from random import random
from socket import gethostname
from datautil import checkpath, copyclasshier
from datetime import datetime
from multiprocessing import Pool
from copy import copy
from scipy.optimize import fmin

HOST = gethostname()

# status ids
INIT = 0
RUNNING = 1 
COMPLETE = 2
STATUS_STR = ["intializing", "running", "complete"]

       
def data_id_str(ids):
    id = ""
    for pair in ids:
        id += "%s=%s_" % tuple(pair)
    id = id.rstrip("_")
    return id

def sim_id_str(name, fixed, par):
    """Get a model label given fixed and fit parameter lists"""
    id = "%s(" % name
    if par!={}:
        keys = par.keys()
        keys.sort()
        for k in keys:
            id += "%s,"%k
        id = id.rstrip(",")+"|"
                
    if fixed!=None:
        keys = fixed.keys()
        keys.sort()        
        for k in keys:
            id += "%s=%s," % (k, fixed[k])
        id = id.rstrip(",")
    id += ")"
    return id

def read_sim_result(id, file):
    """Load saved result of previous simulation, if it exists"""
    print "reading result from "+file
    fp = open(file,"r")
    data = fp.readlines()
    fp.close()

    for line in data:
        ls = line.rstrip('\n').split(' ')
        if ls[0]==id and ls[3]=="par":
            simstr = ls[4:]

    fit = {}
    for i in range(len(fitstr)/2):
        key, value = fitstr[2*i:(2*i+2)]
        if value=="None":
            fit[key] = None
        else:
            fit[key] = float(value)

    return fit

def write_sim_result(name="", par=None, fixed=None, result=None, col=None, file="results.dat"):  

    id = sim_id_str(name, par, fixed)

    if os.path.exists(file):
        fp = open(file,"r")
        output = fp.readlines()
        fp.close()
    else:
        output = []

    # keep any previous fits that weren't run this time
    newoutput = []
    if len(output)>0:
        for line in output:
            sid = line.split(' ')[0]
            if id != line.split(' ')[0]:
                newoutput.append( line )


    # save new sim result to file
    for k in result:

        if isinstance(result[k], list):

            if isinstance(result[k][0], list):

                res = result[k]

                s = ""
                for trial in range(len(res)):
                    data = res[trial]

                    if col==None:
                        col = range(len(data))

                    for i in range(len(data)):

                        s += "%s %s %s %s" % (id, k, trial, col[i])

                        if isinstance(data[i], list):
                            for entry in data[i]:
                                s += " %s" % entry
                        else:
                            s += " %s" % data[i]

                        s += "\n"

                newoutput.append( s )

            else:

                print "1dim list, not implemented yet"

        else:
            newoutput.append( "%s %s %s\n" % (id, k, result[k]) )

    fp = open(file,"w")
    fp.writelines(newoutput)
    fp.close()

def get_bounds(b, par):
    if b==None: return None
    else:       return [par[k] for k in par]

def outside_bounds(b, par):
    bounds = get_bounds(b, par)

    if bounds==None:
        return False
    else:
        out = 0
        for index, value in enumerate(b):
            bnd = bounds[index]
            if value < bnd[0] or value > bnd[1]:
                out += 1
            
        if out > 0:
            return True
        else:
            return False

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def runsim(index):
    global sims
    sims[index]
    sims[index]()

def simpool(sim, nprocesses=2):
    global sims
    nruns = sim.nruns
    run_indices = sim.run_indices

    # set nruns to one for individual sims
    sim.nruns = 1
    sims = [copy(sim) for _ in range(nruns)]
    for r in range(nruns):
        sims[r].run_indices = run_indices[r] # assign the right run_index

    print "farming sim for %s runs" % nruns
    pool = Pool(processes=nprocesses)

    print nruns

    pool.map(runsim, range(nruns))



class Sim:
    def __init__(self, **args):

        # file for saving log
        self.file = args.get('logfile','sim.log')   # where to log progress of sim

        self.rootdir = args.get('rootdir',"")       # root directory to save results in
        self.name = args.get('name',"test")         # generic name of this simulation
        self.model = args.get('model',None)         # class of model being run
        self.id = args.get('id',[])                 # array of [key, value] pairs that identify data used for this simulation
        self.init = args.get('init',{})             # dict of {param: value} pairs used to initialize the model
        self.fixed = args.get('fixed',{})           # dict of {param: value} pairs that are fixed during simulation
        self.par = args.get('par',{})               # dict of {param: value} pairs that are free parameters to be fit
        
        self.nruns = args.get('nruns',1) 
        self.run_indices = args.get('run_indices',range(self.nruns))

        self.quiet = args.get('quiet',False)

        # create an identifier for the data being used
        self.data_id_str = data_id_str(self.id)

        # create an identifier for this simulation
        self.id_str = sim_id_str(self.name, self.fixed, self.par)

        # create directory structure if needed
        self.outdir = "%s/%s/%s/%s" % (self.rootdir, self.name, self.id_str, self.data_id_str)
        checkpath(self.outdir)

        # copy the file containing the model definition into the output directory
        r = copyclasshier(self.model, "%s/%s" % (self.rootdir, self.name))

    def __call__(self):

        self.log(status=INIT)
        m = self.model(self.init)

        self.log(status=RUNNING)

        # if there are no free parameters to fit, then just call the model
        if self.par=={}:
            if not self.quiet: print "No free parameters, running model for %s runs..." % self.nruns
            
            for r in range(self.nruns):
                rind = self.run_indices[r]

                if "llh" in dir(m):
                    # if model has llh defined, run the model and compute the log-likelihood 
                    # given the fixed parameters
                    m.llh(None, {"fixed":self.fixed, "dir":self.outdir, "runindex":rind}, cache=False)
                else:
                    # otherwise, just run the model without computing likelihood
                    m(self.fixed, output=False)        
                
                sys.stdout.flush()
                self.output( m.output(), rind=rind) # write model output to file

        else:
            if not self.quiet: print "Found free parameters, fitting model %s times..." % self.nruns
            for r in range(self.nruns): self.fit(m, r)

        self.log(status=COMPLETE)

    def fit(self, model, run):
        """Generic function for fitting a model's free parameters"""

        print "| fitting via fmin:"
        init = []

        for i in range(len(self.par)):
            p = self.par.keys()[i]
            bmin, bmax = self.par[p]

            # init value should be randomly chosen in between the min and max values
            init_p = bmin + random()*(bmax-bmin)
            init.append(init_p)
            print "|\t%s: init=%s, min=%s, max=%s" % (p, init_p, bmin, bmax)

        if self.fixed!=None:
            print "| fixing:"
            for p in self.fixed:
                print "|\t%s=%s" % (p, self.fixed[p])


        args = {"par":self.par,
                "fixed":self.fixed,
                "dir":self.outdir,
                "runindex":run
               }
        [f, fopt, iter, funcalls, warnflag] = fmin( model.llh, init, args=[args], xtol=.1, ftol=.1, maxiter=100, full_output=1 )
        print "| %s iterations" % iter

        llh = model.llh(f, args)
        self.outputfit( model, init, f, fopt, iter, run, llh )
    def output(self, data, rind=None):
        if rind is None:
            f = "%s/output.dat.gz" % self.outdir
        else:
            f = "%s/output-run%s.dat.gz" % (self.outdir, rind)

        print "\twriting result"
        fp = gzip.open(f, "w")
        fp.writelines(data)
        fp.flush()
        fp.close()

    def outputfit(self, model, init, f, fopt, iter, run, llh):
        
        if run==0:
            fp = open("%s/fit_output.dat" % self.outdir, "w")
            s = "%s\n" % self.id_str
            #for p in self.init:
            #    s += "init %s %s\n" % (p, self.init[p])
            for p in self.fixed:
                if p not in self.par:
                    s += "fixed %s %s\n" % (p, self.fixed[p])
            for p in self.par:
                s += "par %s %s\n" % (p, self.par[p])
        else:
            fp = open("%s/fit_output.dat" % self.outdir, "aw")
            s = ""

        # write results of fitting
        for i in range(len(self.par)):
            k = self.par.keys()[i]
            s += "%s init %s\n" % (run, init[i])
            s += "%s fit %s %s\n" % (run, k, f[i])
            s += "%s totalllh %s\n" % (run, llh)
            s += "%s niter %s\n" % (run, iter)
        if model.loglh!=None:
            s += "%s llh" % run
            for el in model.loglh:
                s += " %s" % el
            s += "\n"

        if not self.quiet:
            print s

        # any additional output from model given best fit parameters
        s += model.output(outputprefix="%s " % run)
       

        fp.writelines(s)
        fp.close()

    def log(self, status=0):
        
        info = (datetime.now(),
                HOST,
                self.id_str,
                self.data_id_str,
                STATUS_STR[status])
        logstr = ("%s\t"*len(info) % info)
        logstr += "\n"
        if not self.quiet:
            print logstr

        fp = open(self.file,"aw")
        fp.writelines(logstr)
        fp.close()


