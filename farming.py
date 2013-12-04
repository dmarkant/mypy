#!/usr/bin/python
import sys, multiprocessing
"""
General-purpose interaction with multiprocessing library

"""
#jobdict = {}

def workerfunc(targetfunc, jobqueue):
    """Generic worker function that will get passed to 
    individual processes

    targetfunc:     function to run
    jobqueue:       list of parameter settings
    """
    while True:
        next = jobqueue.get()  # pop a job from the queue

        if next==None: break   # if hit a None, end this process
        else:
            ind, j = next
            print j
            try:
                r = targetfunc(j)       # evaluate the function
            except:
                print 'prob bob'
                r = sys.exc_info()[0]   # catch any error
            
            jobdict[ind] = r     # store the result
    return

def farm(targetfunc, jobs=[], num_workers=1):
    """Distribute jobs to multiple processes

    targetfunc:     function to run
    jobs:           list of arguments for each job
    num_workers:    number of processes to start
    """
    global jobdict

    # create a manager to keep track of completed jobs
    manager = multiprocessing.Manager()
    jobdict = manager.dict()
    for i in range(len(jobs)): jobdict[i] = None

    # number of processes
    num_workers = min(num_workers, len(jobs))
    print "farming %s out to %s workers" % (targetfunc.__name__, num_workers)

    q = multiprocessing.Queue()
    for i in range(len(jobs)):      q.put( [i, jobs[i]] )
    for _ in range(num_workers):    q.put( None ) # sentinel to stop each process
   
    workers = []
    for i in range(num_workers):
        tmp = multiprocessing.Process(target=workerfunc, args=[targetfunc, q])
        tmp.start()
        workers.append(tmp)

    # wait for all workers to finish before returning
    for worker in workers: worker.join()
    q.close()

    # process the result
    return {"targetfunc":targetfunc.__name__,
            "result":[{"args":jobs[i], "value":jobdict[i]} for i in range(len(jobs))]}


def catch_incomplete_jobs(d):
    inc = []
    for job in d["result"]:
        if job["value"]==None: inc.append(job["args"])
    return inc


def farmtest():
    global f, results
    print "testing farming.py"
 
    def f(x): return sum(x)
 
    jobs = []
    for i in range(100):
        for j in range(100):
            jobs.append([i,j])
    r = farm(targetfunc=f, jobs=jobs, num_workers=2)

    print "result: ", r

    # incompleted jobs
    print "incomplete: ", catch_incomplete_jobs(r)



if __name__ == '__main__':
    farmtest()




