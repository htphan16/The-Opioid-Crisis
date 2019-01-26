#!/usr/bin/env python
# coding: utf-8

# In[48]:


import pandas as pd
data_10 = pd.read_csv('ACS_10_5YR_DP02_with_ann.csv')
data_11 = pd.read_csv('ACS_11_5YR_DP02_with_ann.csv')
data_12 = pd.read_csv('ACS_12_5YR_DP02_with_ann.csv')
data_13 = pd.read_csv('ACS_13_5YR_DP02_with_ann.csv')
data_14 = pd.read_csv('ACS_14_5YR_DP02_with_ann.csv')
data_15 = pd.read_csv('ACS_15_5YR_DP02_with_ann.csv')
data_16 = pd.read_csv('ACS_16_5YR_DP02_with_ann.csv')


def info(df):
    # define a d_yy dictionary
    d_yy = {}
    # define lists to store counties and states data
    counties_list = []
    states_list = []
    
    for counties in df['GEO.display-label']:
        counties = counties.split(' ')
        county = counties[0]
        if county != 'Geography':
            counties_list.append(county)
        try:
            state = counties[2]
            if state == 'Kentucky':
                states_list.append('KY')
            elif state == 'Ohio':
                states_list.append('OH')
            elif state == 'Pennsylvania':
                states_list.append('PA')
            elif state == 'Virginia':
                states_list.append('VA')
            else:
                states_list.append('WV')
        except IndexError:
            continue
    # define lists to store total households data
    total_households_list = []
    for household in df['HC01_VC03']:
        if household != 'Estimate; HOUSEHOLDS BY TYPE - Total households':
            total_households_list.append(int(household))
            
    # 1. Identify 10 more indicators of households that you think are important e.g male households with children below 18 years old, female households with children below 18 years old...
    # define lists to store those data like above
    
    # add all data into the dictionary
    d_yy['COUNTY'] = counties_list
    d_yy['State'] = states_list
    d_yy['Total Households'] = total_households_list
    # 2. Add all data of the 10 indicators into the dictionary like above
    #e.g d_yy['Male Households']
    
    return pd.DataFrame.from_dict(d_yy)

d_10 = info(data_10)
groupby_state_10 = d_10.groupby(['State'])
d_11 = info(data_11)
groupby_state_11 = d_11.groupby(['State'])
d_12 = info(data_12)
groupby_state_12 = d_12.groupby(['State'])
d_13 = info(data_13)
groupby_state_13 = d_13.groupby(['State'])
d_14 = info(data_14)
groupby_state_14 = d_14.groupby(['State'])
d_15 = info(data_15)
groupby_state_15 = d_15.groupby(['State'])
d_16 = info(data_16)
groupby_state_16 = d_16.groupby(['State'])

# Total Households in each state over the years
def thh_yy(df, yy):
    total_households_yy = pd.DataFrame(groupby_state.sum().sort_values(by = ['Total Households'], ascending=False))
    return total_households_yy.rename(columns={'Total Households': 'Total Households in {}'.format(yy)})

print(thh_yy(d_10, '2010'))





# # 
