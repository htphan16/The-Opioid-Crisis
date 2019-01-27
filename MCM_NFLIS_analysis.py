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
                    if Data[j] == '(X)':
                        X[label] = 0
                    else:
                        X[label] = Data[j]
            CensusData.append(X)
    return CensusData
CensusData = ACSCensus()
def CensusQuery(Query, Data): # Query is dictionary: {'YYYY', 'COUNTY', 'State'}, Data is inquiry, E.g. 'HC03_VC04'
    for Test in CensusData:
        if False in [Test[x] == Query[x] for x in Query]:
            pass
        elif Test[Data] == None:
            print('WRONGWRONGWRONG')
            break
        else:
            return Test[Data]
def CountyList(State, SQuery, CQuery, YYYY, Keep, Record = 10): # Both Queries are lists of items you want to include. Keep is either a positive integer or 'all'.
    Counties = set()
    for county in CensusData:
        if county['State'] == State:
            Counties.add(county['COUNTY'])
    Counties = list(Counties)
    Counties.sort()
    if Keep == 'All':
        return Counties
    CountySubstance = [sum(int(DrugReports({'State': State, 'COUNTY':county, 'YYYY':YYYY, 'SubstanceName':S})) for S in SQuery) for county in Counties]
    CountyCensus = [sum(int(CensusQuery({'State': State, 'COUNTY': county, 'YYYY':YYYY}, C)) for C in CQuery) for county in Counties]
    Counties = [[Counties[i], CountySubstance[i] / CountyCensus[i]] for i in range(len(Counties))]
    Counties.sort(key = lambda tup:tup[1])
    if Record == 'Most':
        return Counties[len(Counties) - Keep:]
    elif Record == 'Least':
        return Counties[:Keep]
def CountyReports(State, SQuery, CQuery, YYYY, Title, Keep = 10, Record = 'Most'):
    T = range(2010, 2017)
    CL = CountyList(State, SQuery, CQuery, YYYY, Keep, Record)
    for county in CL:
        DR = [sum(int(DrugReports({'State':State, 'COUNTY':county[0], 'YYYY':'%s'%(y), 'SubstanceName': S})) for S in SQuery) for y in range(2010, 2017)]
        HH = [sum(int(CensusQuery({'State':State, 'COUNTY':county[0], 'YYYY':'%s'%(y)}, C)) for C in CQuery) for y in range(2010, 2017)]
        P = [DR[i] / HH[i] for i in range(len(DR))]
        plt.plot(T, P, label = '%s'%(county[0]))
        plt.legend(loc = "upper left", bbox_to_anchor=(1,1))
        plt.title('%s %s Reported Counties in %s (Set %s)'%(str(Keep), Record, State, YYYY))
        plt.suptitle(Title)
    plt.savefig(Title, bbox_inches='tight', dpi = 100)
    plt.show()

# Generate Reports per Household
#CountyReports('OH', ['Morphine'], ['HC03_VC03'], '2010', 'OH Morphine Reports Per Household')
#CountyReports('OH', ['Heroin'], ['HC03_VC03'], '2010', 'OH Heroin Reports Per Household')
#CountyReports('OH', ['Fentanyl'], ['HC03_VC03'], '2010', 'OH Fentanyl Reports Per Household')
#CountyReports('VA', ['Morphine'], ['HC03_VC03'], '2010', 'VA Morphine Reports Per Household')
#CountyReports('VA', ['Heroin'], ['HC03_VC03'], '2010', 'VA Heroin Reports Per Household')
#CountyReports('VA', ['Fentanyl'], ['HC03_VC03'], '2010', 'VA Fentanyl Reports Per Household')
#CountyReports('WV', ['Morphine'], ['HC03_VC03'], '2010', 'WV Morphine Reports Per Household')
#CountyReports('WV', ['Heroin'], ['HC03_VC03'], '2010', 'WV Heroin Reports Per Household')
#CountyReports('WV', ['Fentanyl'], ['HC03_VC03'], '2010', 'WV Fentanyl Reports Per Household')
#CountyReports('KY', ['Morphine'], ['HC03_VC03'], '2010', 'KA Morphine Reports Per Household')
#CountyReports('KY', ['Heroin'], ['HC03_VC03'], '2010', 'KA Heroin Reports Per Household')
#CountyReports('KY', ['Fentanyl'], ['HC03_VC03'], '2010', 'KA Fentanyl Reports Per Household')
#CountyReports('PA', ['Morphine'], ['HC03_VC03'], '2010', 'PA Morphine Reports Per Household')
#CountyReports('PA', ['Heroin'], ['HC03_VC03'], '2010', 'PA Heroin Reports Per Household')
#CountyReports('PA', ['Fentanyl'], ['HC03_VC03'], '2010', 'PA Fentanyl Reports Per Household')

def SCCorrelation(State, SQuery, CQuery, YYYY, Title, Show = True): # YYYY is list of years
    CL = CountyList(State, [], [], '2010', 'All')
    # Generate a list of ordered pairs: Household/DrugReports
    for Year in YYYY:
        SValues, CValues = [], []
        for County in CL:
            SValues.append(sum(int(DrugReports({'State':State, 'COUNTY':County, 'YYYY':Year, 'SubstanceName': S}))for S in SQuery))
            CValues.append(sum(int(CensusQuery({'State':State, 'COUNTY':County, 'YYYY':Year}, C)) for C in CQuery))
        plt.plot(CValues, SValues, 'o', label = '%s'%(Year))
    if [len(SQuery), len(CQuery)] == [1, 1]:
        plt.suptitle('%s-%s Correlation Scatterplot'%(SQuery[0], CQuery[0]))
        plt.xlabel(CQuery[0])
        plt.ylabel(SQuery[0])
    else:
        plt.suptitle('Substance-Census Correlation Scatterplot')
        plt.xlabel('CensusData')
        plt.ylabel('DrugReports')
    plt.legend(loc = "upper left", bbox_to_anchor=(1,1))
    plt.title('%s Counties'%(State))
    plt.savefig('Analysis/SubstanceCensusCorrelations/' + Title, bbox_inches='tight', dpi = 100)
    plt.show()
