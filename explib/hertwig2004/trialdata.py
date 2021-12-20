trialdata = pd.read_csv('/Users/markant/code/py/mypy/explib/hertwig2004/Hertwig04_sampling_122.0.txt', sep=' ', index_col=0)
trialdata['choice'] = -1

choicedata = pd.read_csv('/Users/markant/code/py/mypy/explib/hertwig2004/Hertwig04_choice_122.0.txt', sep=' ', index_col=0)

for i, row in choicedata.iterrows():
    trialdata.loc[(trialdata.subject==row.subject) &
                  (trialdata.problem==row.problem) &
                  (trialdata.lastsample==1),'choice'] = row['choice']

trialdata.drop('lastsample', 1, inplace=True)

trialdata.to_csv('/Users/markant/code/py/mypy/explib/hertwig2004/hertwig2004_trialdata.csv')
