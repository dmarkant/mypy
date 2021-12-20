import numpy as np
import pandas as pd
from scipy.stats import t


def within_normalized_CI(df, x, y, group, conf=.95):
    """Compute within-subjects confidence intervals through
    normalization. Based on method described in Morey (2008)
    and Franz and Loftus (2012).

    df (pandas dataframe) : data
    x  (string)           : column name for within-subjects factor
    y  (string)           : column name for dependent variable
    group (string)        : column name for grouping variable (e.g., subject id)
    conf (float)          : confidence level
    """
    p = 1 - (1 - conf)/2.

    # number of within-subjects conditions
    M = df[x].unique().shape[0]

    # normalize observations
    normalize = lambda grp: grp[y] - grp[y].mean() + df[y].mean()
    df.loc[:,'y_norm'] = df.groupby(group).apply(normalize).reset_index()[y].values

    CI = []
    for i, rep in df.groupby(x):
        z = rep['y_norm'].values
        n = z.shape[0]
        cv = t.ppf(p, n)

        # standard error
        se = np.sqrt((M/float(M - 1)) * (1./(n*(n-1))) * np.sum((z - z.mean()) ** 2))

        # 95% CI
        CI.append([rep[x].values[0], cv * se])

    return pd.DataFrame(np.array(CI), columns=[x, '95-CI(within)'])
