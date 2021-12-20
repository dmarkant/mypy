"""

Some notes about this experiment:

    1. Only a single opponent per experiment

"""
import requests
import json
import os
import glob
import numpy as np

DATADIR = '/Users/markant/data/CompetitiveSampling/rttb-v0'
KEYFILE = '%s/rttb-v0-KEY.txt' % DATADIR

N_GAMES = 8


def download_data_from_keyfile(force=False, quiet=True):

    with open(KEYFILE, 'r') as fp:
        uids = [l.rstrip('\n') for l in fp.readlines()]
    download_data(uids, force=force, quiet=quiet)


def download_data(uniqueIds, force=False, quiet=True):

    for i, uid in enumerate(uniqueIds):

        fn = '%s/%i.json' % (DATADIR, i)
        if not os.path.exists(fn) or force:

            url = 'http://cog-grpexp.appspot.com/data?uniqueId=%s' % uid
            if not quiet:
                print 'Fetching data %s' % url
            r = requests.get(url)

            data = r.json()['data']

            # save the file
            with open(fn, 'w') as fp:
                fp.write(data)


def load_data(sid):

    pth = '%s/%s.json' % (DATADIR, sid)

    if not os.path.exists(pth):
        print 'No datafile found at %s' % pth
        return None
    else:

        with open(pth, 'r') as fp:
            data = fp.read()
        return json.loads(data)


def subjects():
    """
    Get subject ids based on files in data directory.

    """
    files = glob.glob('%s/*.json' % DATADIR)
    SUBJ = [int(f.split('/')[-1].rstrip('.json')) for f in files]
    SUBJ.sort()
    return SUBJ


def get_chooser(sid0, sid1, gid):
    result = []
    for sid in [sid0, sid1]:
        dat = exp.Subject(sid).data
        start = map(lambda d: d[0]=='game' and d[1]==gid, dat).index(True)
        if gid is 7:
            end = -1
        else:
            end = map(lambda d: d[0]=='game' and d[1]==(gid+1), dat).index(True)
        other = len(filter(lambda d: len(d) > 1 and d[1]=='You both stopped, but the other player was randomly selected to choose first...', dat[start:end]))
        chooser = not other
        result.append(chooser)
    return result


def observed_rare(sid):
    obs = []
    for gid in range(8):
        opt = subjects[sid].options(gid)
        samp = np.array(subjects[sid].samples(gid))
        rare_outcomes = np.array([opt['A'][0], opt['B'][0]])
        if len(np.intersect1d(rare_outcomes, samp[:,1])) > 0:
            obs.append(1)
        else:
            obs.append(0)
    return np.array(obs)


class Subject:

    def __init__(self, sid):
        self.sid = sid
        self.raw = load_data(sid)

        self.data = filter(lambda d: len(d) > 0, [r['data'] for r in self.raw])
        self.pars = {str(p[1]): p[2] for p in filter(lambda d: d[0] == 'par', self.data)}

        self.GENDER = 'noresp'
        self.AGE = 'noresp'

        # get parameters
        for d in self.data:
            if len(d) > 1:
                if d[1] == 'CONDITION':
                    self.CONDITION = int(d[2])
                if d[1] == 'COUNTER':
                    self.COUNTER = int(d[2])
                if d[1] == 'N_OPTIONS':
                    self.N_OPTIONS = map(int, d[2].split(';'))
                if d[1] == 'gender':
                    self.GENDER = d[2]
                if d[1] == 'age':
                    self.AGE = d[2]


    def trainingdata(self):

        td = filter(lambda d: d[0] == 'training', self.data)
        ev = [l[3] for l in filter(lambda d: d[2] == 'ev', td)]

        # this gets rid of a few typos in the data
        ev = [float(''.join(c for c in entry if c.isdigit() or c=='-')) for entry in ev]



        samples = [map(int, l[3].split(';'))
                   for l in filter(lambda d: d[2] == 'samples', td)]
        sample_ev = map(np.mean, samples)
        err = np.array(ev) - np.array(sample_ev)

        #print 'estimated:', ev
        #print 'sample:', sample_ev
        #print 'error:', err

        traindata = []
        for i in range(len(ev)):
            traindata.append({'ev': ev[i],
                              'sample_ev': sample_ev[i],
                              'err': err[i]})

        return traindata

    def avg_training_error(self):
        return np.mean([td['err'] for td in self.trainingdata()])

    def gamedata(self, gid):
        gd = []
        for d in self.data:
            if d[0] == 'game' and int(d[1]) == gid:
                gd.append(d)
        return gd

    def samplesize(self):

        ss = []
        for gid in range(N_GAMES):
            samp = self.samples(gid)
            ss.append(len(samp))
        return ss

    def samples(self, gid):
        gd = self.gamedata(gid)
        samples = []
        for d in filter(lambda d: d[3] == 'sample', gd):
            opt = 0 if d[4] == 'A' else 1
            out = d[5]
            samples.append([opt, out])
        return samples

    def stop_by_trial(self, gid):
        dec_g = filter(lambda d: d[0]=='game' and d[1]==gid and d[3]=='stoppingdecision', self.data)
        return [d[-1] for d in dec_g]

    def stopped(self):
        stopped = []
        for gid in range(8):
            dec_g = filter(lambda d: d[0]=='game' and d[1]==gid and d[3]=='stoppingdecision', self.data)
            stopped.append(dec_g[-1][-1])
        return stopped

    def choice(self, gid, kind='HL'):
        ch = filter(lambda d: d[3]=='received_id', self.gamedata(gid))[0][4]
        if kind is 'AB':
            return ch
        elif kind is 'HL':
            opt = self.options(gid)
            H = 'A' if opt['A'][3] > opt['B'][3] else 'B'
            return 1*(ch==H)

    def options(self, gid):
        gd = self.gamedata(gid)
        options = {}
        for o in filter(lambda d: d[2]=='option', gd):
            options[o[3]] = o[4:]
        return options

    def domain(self, gid):
        options = self.options(gid)
        outcomes = options['A'][:2]
        if outcomes[0] > 0 or outcomes[1] > 0:
            return 1
        else:
            return -1

    def points(self):
        pts = []
        for gid in range(N_GAMES):
            opt = self.options(gid)

            gd = self.gamedata(gid)
            received = filter(lambda d: d[3] == 'received_id', gd)
            if len(received) > 0:
                pts.append(opt[received[0][4]][3])
            else:
                pts.append(np.nan)
        return pts

    def loss(self):
        pts = self.points()
        loss = []
        for gid in range(N_GAMES):
            gd = self.gamedata(gid)
            best = np.max([float(l[7]) for l in filter(lambda d: d[2] == 'option', gd)])
            loss.append(best - pts[gid])
        return loss

    def loss_random(self):
        loss = []
        for gid in range(N_GAMES):
            evs = np.array(self.options(gid).values())[:,-1]
            loss.append(np.mean(np.max(evs) - evs))
        return loss

    def bonusearned(self):
        pass

    def opponent(self):
        # only one opponent per experiment, so just grab
        # from first game
        return filter(lambda d: d[2] == 'opponents', self.gamedata(0))[0][3][0]