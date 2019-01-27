import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

with open('MCM_NFLIS_Data.csv', 'r') as file:
    reader = csv.reader(file)
    Data = [{'YYYY':rows[1],
            'State':rows[2],
            'COUNTY':rows[3],
            'SubstanceName':rows[7],
            'DrugReports':rows[8]} for rows in reader]

def DrugReports(Query): # input as a dictionary {YYYY, State, COUNTY, SubstanceName}
    DrugReports = 0
    # Stage: check if inputs are logical before proceeding.
    # Stage: check if inputs match items in data. I mean, you could even use the filter function here, but I'm not good with python.
    for Index in Data:
        Test = {'YYYY':Index['YYYY'], 'State':Index['State'], 'COUNTY':Index['COUNTY'], 'SubstanceName':Index['SubstanceName']}
        if False in [Query[x] == Test[x] for x in Query]:
            pass
        else:
            DrugReports += int(Index['DrugReports'])
    return DrugReports
# The following is adapted from Huong's code.

data_10 = pd.read_csv('ACS_10_5YR_DP02/ACS_10_5YR_DP02_with_ann.csv')
data_11 = pd.read_csv('ACS_11_5YR_DP02/ACS_11_5YR_DP02_with_ann.csv')
data_12 = pd.read_csv('ACS_12_5YR_DP02/ACS_12_5YR_DP02_with_ann.csv')
data_13 = pd.read_csv('ACS_13_5YR_DP02/ACS_13_5YR_DP02_with_ann.csv')
data_14 = pd.read_csv('ACS_14_5YR_DP02/ACS_14_5YR_DP02_with_ann.csv')
data_15 = pd.read_csv('ACS_15_5YR_DP02/ACS_15_5YR_DP02_with_ann.csv')
data_16 = pd.read_csv('ACS_16_5YR_DP02/ACS_16_5YR_DP02_with_ann.csv')

def Census(YYYY, df):
    D = {'YYYY': YYYY}
    CountiesList, StatesList = [], []
    for Counties in df['GEO.display-label']:
        Counties = Counties.split(' ')
        County = Counties[0]
        if County != "Geography":
            CountiesList.append(County.upper())
        try:
            State = Counties[2]
            if State == 'Kentucky':
                StatesList.append('KY')
            elif State == 'Ohio':
                StatesList.append('OH')
            elif State == 'Pennsylvania':
                StatesList.append('PA')
            elif State == 'Virginia':
                StatesList.append('VA')
            else:
                StatesList.append('WV')
        except IndexError:
            continue
    D['COUNTY'], D['State'] = CountiesList, StatesList
    for i in df:
        D[i] = {'Name':df[i][0], 'Data':[]}
        for j in df[i][1:]:
            D[i]['Data'].append(j)
    return D
def ACSCensus():
    D = [Census('2010', data_10),
        Census('2011', data_11),
        Census('2012', data_12),
        Census('2013', data_13),
        Census('2014', data_14),
        Census('2015', data_15),
        Census('2016', data_16)]
    CensusData = []
    for i in D: # i is one of the year's census data
        index = len(i['COUNTY'])
        for j in range(index): # specific data index
            X = {}
            for label in i:
                Data = i[label]
                if type(Data) is dict:
                    X[label] = Data['Data'][j]
                elif type(Data) is str:
                    X[label] = i['YYYY']
                else:
                    X[label] = Data[j]
            CensusData.append(X)
    return CensusData
CensusData = ACSCensus()
def CensusQuery(Query, Data): # Query is dictionary: {'YYYY', 'COUNTY', 'State'}, Data is inquiry
    for Test in CensusData:
        if False in [Test[x] == Query[x] for x in Query]:
            pass
        else:
            return Test[Data]