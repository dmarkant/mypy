"""

Some notes about this experiment:

    1. Only a single opponent per experiment

"""
import requests
import json
import os
import glob
import numpy as np

DATADIR = '/Users/markant/data/CompetitiveSampling/optionenv-v0'
KEYFILE = '%s/optionenv-v0-KEY.txt' % DATADIR

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


class Subject:

    def __init__(self, sid):
        self.sid = sid
        self.raw = load_data(sid)

        self.data = [r['data'] for r in self.raw]
        self.pars = {str(p[1]): p[2] for p in filter(lambda d: d[0] == 'par', self.data)}

        # get parameters
        for d in self.data:

            if len(d) > 1 and d[1] == 'CONDITION':
                self.CONDITION = int(d[2])
            if len(d) > 1 and d[1] == 'COUNTER':
                self.COUNTER = int(d[2])
            if len(d) > 1 and d[1] == 'N_OPTIONS':
                self.N_OPTIONS = map(int, d[2].split(';'))

    def trainingdata(self):

        td = filter(lambda d: d[0] == 'training', self.data)
        ev = [float(l[3]) for l in filter(lambda d: d[2] == 'ev', td)]

        samples = [map(int, l[3].split(';'))
                   for l in filter(lambda d: d[2] == 'samples', td)]
        sample_ev = map(np.mean, samples)
        err = np.array(ev) - np.array(sample_ev)

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

    def choices(self, gid):
        pass

    def options(self, gid):
        pass

    def points(self):
        pts = []
        for gid in range(N_GAMES):
            gd = self.gamedata(gid)
            pts.append(filter(lambda d: d[3] == 'received_id', gd)[0][5])
        return pts

    def loss(self):
        pts = self.points()
        loss = []
        for gid in range(N_GAMES):
            gd = self.gamedata(gid)
            best = np.max([float(l[7]) for l in filter(lambda d: d[2] == 'option', gd)])
            loss.append(best - pts[gid])
        return loss

    def bonusearned(self):
        pass

    def opponent(self):
        # only one opponent per experiment, so just grab
        # from first game
        return filter(lambda d: d[2] == 'opponents', self.gamedata(0))[0][3][0]
