import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import os

years_election = [1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020]
months_considered = [9, 10, 11]
republicans = ['George Bush', 'Bob Dole', 'George W. Bush', 'John McCain', 'Mitt Romney', 'Donald Trump']

def load_polls():
    df = pd.read_csv('../data/poll_average_1968_2020.csv')
    return df


def find_lowest_year_represented():
    df = load_polls()
    states = list(np.unique(df['state'].values))
    states.remove('ME-1')
    states.remove('ME-2')
    states.remove('NE-1')
    states.remove('NE-2')
    states.remove('NE-3')
    states.remove('District of Columbia')
    running_min = 1948
    for state in states:
        years_availables = np.min(df[df['state'] == state]['cycle'].values)
        running_min = max(years_availables, running_min)
    return running_min


def explore_alaska():
    df = load_polls()
    df = (df[df['state'] == 'Alaska'])
    df = df[df['cycle'] == 1988]
    print(df['modeldate'])


def explore_hawaii():
    df = load_polls()
    df = (df[df['state'] == 'Hawaii'])
    df = df[df['cycle'] == 1988]
    print(df['modeldate'])


def explore_Idaho():
    df = load_polls()
    df = (df[df['state'] == 'Idaho'])
    print(df['modeldate'])


def load_state_polls_2():
    df = load_polls()
    states = list(np.unique(df['state'].astype('str').values))
    states.remove('ME-1')
    states.remove('ME-2')
    states.remove('NE-1')
    states.remove('NE-2')
    states.remove('NE-3')
    states.remove('District of Columbia')
    polls_per_year = pd.DataFrame()
    for state in states:
        df_state = df[df['state'] == state]
        for year in years_election:
            df_state_year_election = df_state[df_state['cycle'] == year]
            mask_interesting_months = df_state_year_election['modeldate'].apply(
                lambda x: True if (
                        int(x.split('/')[0]) > 8) else False)  # select the polls of election year, from June to October
            interesting_months_poll = df_state_year_election[mask_interesting_months]
            try:
                for candidate in np.unique(interesting_months_poll['candidate_name'].values):
                    polls_candidate_3_months = interesting_months_poll[
                        interesting_months_poll['candidate_name'] == candidate]
                    dict_year_candidate = {'cycle': int(year), 'state': state, 'candidate_name': candidate}
                    for month in months_considered:
                        mask_month_considered_candidate = polls_candidate_3_months['modeldate'].apply(
                            lambda x: True if (int(
                                x.split('/')[0])) == month else False)  # get the poll for every month
                        month_considered_candidate = polls_candidate_3_months[mask_month_considered_candidate]
                        stats_polls_candidate = np.mean(month_considered_candidate[
                                                            'pct_trend_adjusted'])  # compute the mean poll for every month considered
                        dict_year_candidate['month_' + str(month)] = stats_polls_candidate
                    polls_per_year = polls_per_year.append(dict_year_candidate, ignore_index=True)
            except KeyError:
                continue
    return polls_per_year


def reformat_dataframe_2(df):
    polls_2 = pd.DataFrame()
    for year in years_election:
        df_year = df[df['cycle'] == year]
        for state in np.unique(df['state'].astype('str').values):
            df_year_state_unm = df_year[df_year['state'] == state]
            mask_df_year_state = df_year_state_unm['candidate_name'].apply(
                lambda x: False if x.split(' ')[0] == 'Convention' else True)
            df_year_state = df_year_state_unm[mask_df_year_state]
            try:
                candidates = np.unique(df_year_state['candidate_name'].astype('str').values)
                scores_candidates = {
                    candidate: np.mean(df_year_state[df_year_state['candidate_name'] == candidate]['month_11'])
                    for
                    candidate in candidates}
                sorted_scores = {name: score for (name, score) in sorted(scores_candidates.items(), key=lambda x: x[1])}
                retained_candidates = list(sorted_scores.keys())[-2:]  # the sort is being made in increasing order
                mask_retained_candidates = df_year_state['candidate_name'].apply(
                    lambda x: True if x in retained_candidates else False)
                retained_candidates_df = df_year_state[mask_retained_candidates]
                polls_2 = polls_2.append(retained_candidates_df, ignore_index=True)
            except KeyError:
                continue
    return polls_2


def Rep_Dem(df):
    # adds the party of a candidate based on his name
    names = df['candidate_name']
    party = []
    for i, name in enumerate(names):
        if name in republicans:
            party.append(1)
        else:
            party.append(0)
    df['republican'] = party
    return df


def merge_dfs():
    for i, file in enumerate(os.listdir('states/')):
        if '_' in file or 'txt' in file:
            continue
        else:
            split = file.split('.')
            file_reps = split[0] + '_House.' + split[1]
            df = pd.read_csv('states/'+file)
            df_reps = pd.read_csv('states/'+file_reps)
            df_reps['republican'] = [1]*len(df_reps)
            for i in range(9):
                df_reps = df_reps.append(df_reps.loc[[i] * 1].assign(**{'republican': 0, 'Rep_House_Prop': 1 - df_reps.loc[i]['Rep_House_Prop']}), ignore_index=True)
            df_reps.sort_values(by='Year', inplace=True, ascending=True)
            df_reps.to_csv('states/'+file_reps)

def join_dfs():
    for i, f in enumerate(os.listdir('states/')):
        if '_' in f or 'txt' in f:
            continue
        else:
            split = f.split('.')
            file_reps = split[0] + '_House.' + split[1]
            df = pd.read_csv('states/'+f)
            df['Year'] = df['cycle']
            columns_df = list(df.columns)
            for column in columns_df:
                if column.startswith('Unnamed'):
                    columns_df.remove(column)
            columns_df = columns_df[1:]
            df = df[columns_df]
            df_reps = pd.read_csv('states/'+file_reps)
            columns_reps = df_reps.columns[2:]
            df_reps = df_reps[columns_reps]
            df_reps['Year'] = df_reps['Year'] + 2
            merged_df = pd.merge(df, df_reps, on=['Year', 'republican'])
            merged_df.to_csv('states/v1_'+f)






if __name__ == '__main__':
    join_dfs()