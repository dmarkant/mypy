import requests, json, os, glob



DATADIR = '/Users/markant/data/CompetitiveSampling/optionenv-v0-pilot'
KEYFILE = '%s/optionenv-v0-pilot-KEY.txt' % DATADIR


N_GAMES = 8


def download_data_from_keyfile():

    with open(KEYFILE, 'r') as fp:
        uids = [l.rstrip('\n') for l in fp.readlines()]
    download_data(uids)



def download_data(uniqueIds):

    for i, uid in enumerate(uniqueIds):

        url = 'http://cog-grpexp.appspot.com/data?uniqueId=%s' % uid
        print 'Fetching data %s' % url
        r = requests.get(url)

        data = r.json()['data']

        # save the file
        with open('%s/%i.json' % (DATADIR, i), 'w') as fp:
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

        # get parameters
        for d in self.data:

            if len(d)>1 and d[1]=='CONDITION':
                self.CONDITION = int(d[2])
            if len(d)>1 and d[1]=='COUNTER':
                self.COUNTER = int(d[2])
            if len(d)>1 and d[1]=='N_OPTIONS':
                self.N_OPTIONS = map(int, d[2].split(';'))


    def gamedata(self, gid):
        gd = []
        for d in self.data:
            if d[0]=='game' and int(d[1])==gid:
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
        for d in filter(lambda d: d[3]=='sample', gd):
            opt = 0 if d[4]=='A' else 1
            out = d[5]
            samples.append([opt, out])
        return samples


    def choices(self, gid):
        pass


    def bonusearned(self):
        pass
