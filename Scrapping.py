import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import os



def reformat_gdp():
    df = pd.read_csv('data/GDP/GDP.csv')
    gdp = df['GDPC1'].values
    # separate them into list of 7 values: one per year of non-election and 4 per election year
    gdps = [gdp[i:i + 7] for i in range(0, len(gdp), 7)]
    attributes = ['Year0', 'Year1', 'Year2', 'Electiony1', 'Electiony2', 'Electiony3', 'Electiony4']
    new_df = pd.DataFrame(gdps, columns=attributes)
    return new_df


def reformat_rdi():
    df = pd.read_csv('data/Fundamentals/RDI/RDI.csv')
    rdi = df[df.columns[1]].values
    rdis = [rdi[i:i + 4] for i in range(0, len(rdi), 4)]
    attributes = ['rdi_y0', 'rdi_y1', 'rdi_y2', 'rdi_ey']
    new_df = pd.DataFrame(rdis, columns=attributes)
    return new_df


def reformat_payroll():
    df = pd.read_csv('data/Fundamentals/Payroll/PAYEMS.csv')
    payroll = df['PAYEMS'].values
    payroll_reformated = []
    payroll_per_year = [payroll[i:i + 12] for i in range(0, len(payroll), 12)]
    #  print(payroll_per_year)
    year = 1
    for payroll_year in payroll_per_year:
        if year % 4 == 0:
            payroll_year_reformated = payroll_year[7:10]
        else:
            payroll_year_reformated = [payroll_year[9]]
        payroll_reformated.append(payroll_year_reformated)
        year += 1
    #  now aggregate the data for every election
    payroll_final = [np.hstack(payroll_reformated[i:i + 4]) for i in range(0, len(payroll_reformated), 4)]
    attributes_payroll = ['payroll_y1', 'payroll_y2', 'payroll_y3', 'payroll_ey1', 'payroll_ey2', 'payroll_ey3']
    payroll_df = pd.DataFrame(payroll_final, columns=attributes_payroll)
    return payroll_df


def reformat_dowjones():
    dowjones_yearly = np.hstack(pd.read_csv('data/Fundamentals/Stock_market/Dowjones.csv').values)
    dowjones_yearly = [float(s[:-1]) / 100. for s in dowjones_yearly[::-1]]
    dowjones_per_election = [dowjones_yearly[i:i + 4] for i in range(0, len(dowjones_yearly), 4)]
    dowjones_per_election[-1].append(-0.0371)
    stock_market = pd.DataFrame(dowjones_per_election, columns=['Stock_y1', 'Stock_y2', 'Stock_y3', 'Stock_ey'])
    return stock_market


def dataframe_fundamentals():
    data_directory = 'data/Fundamentals/'
    dfs = []
    columns_name = []
    values = None
    for i, f in enumerate(os.listdir(data_directory)):
        try:
            for j, file in enumerate(os.listdir(os.path.join(data_directory, f))):
                wdirectory = os.path.join(data_directory, f)
                if file.endswith('.csv'):
                    csv_file = os.path.join(wdirectory, file)
                    df = pd.read_csv(csv_file)
                    columns_name.extend(list(df.columns))
                    if values is None:
                        values = df.values
                    else:
                        values = np.concatenate((values, df.values), axis=1)
        except:
            continue
    df_fundamental = pd.DataFrame(values, columns=columns_name)
    df_fundamental.drop(df_fundamental.columns[0], axis=1, inplace=True)
    return df_fundamental



if __name__ == '__main__':
    df_final = dataframe_fundamentals()
    df_final.to_csv('data/Fundamentals/Fundamentals1.csv', index=False)
    df_final.to_excel('data/Fundamentals/Fundamentals1.xlsx', index=False)

