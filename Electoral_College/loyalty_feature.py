import pandas as pd
import os
import numpy as np

def create_dirs():
    for i, f in enumerate(os.listdir('states/')):
        if 'txt' not in f:
            state = f[3:-4]
            df = pd.DataFrame({'election':[]})
            df.to_csv('states/'+state+'_loyalty.csv')

def get_loyalty():
    for i, f in enumerate(os.listdir('states/')):
        if 'txt' not in f and 'v1' not in f:
            state = f[:-12]
            corresponding = 'v1_' + state + '.csv'
            previous = pd.read_csv('states/'+f)
            df = pd.read_csv('states/'+corresponding)
            republican_scores = df.loc[df['republican']==1, 'Result'].values
            republican_scores_before = previous['election'].values
            loyalty = np.concatenate((republican_scores_before, republican_scores))
            weights = np.array([1, 2, 3, 4])
            loyalty_score = [np.sum(weights*loyalty[i-4:i])/10 for i in range(4, len(loyalty)) if np.nan not in loyalty[i-4:i]]
            df.loc[df['republican'] == 1, 'rep_loyalty'] = loyalty_score
            df.loc[df['republican'] == 0, 'rep_loyalty'] = loyalty_score
            df.to_csv('states/v2'+state+'.csv')



if __name__ == '__main__':
    for i, f in enumerate(os.listdir('states/')):
        if 'v2' in f:
            df = pd.read_csv('states/'+f)
            state = f[2:]
            df.to_csv('states/'+state+'.csv')