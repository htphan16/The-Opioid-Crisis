import pandas as pd
import matplotlib.pyplot as plt

data_10 = pd.read_csv('ACS_10_5YR_DP02/ACS_10_5YR_DP02_with_ann.csv')
data_11 = pd.read_csv('ACS_11_5YR_DP02/ACS_11_5YR_DP02_with_ann.csv')
data_12 = pd.read_csv('ACS_12_5YR_DP02/ACS_12_5YR_DP02_with_ann.csv')
data_13 = pd.read_csv('ACS_13_5YR_DP02/ACS_13_5YR_DP02_with_ann.csv')
data_14 = pd.read_csv('ACS_14_5YR_DP02/ACS_14_5YR_DP02_with_ann.csv')
data_15 = pd.read_csv('ACS_15_5YR_DP02/ACS_15_5YR_DP02_with_ann.csv')
data_16 = pd.read_csv('ACS_16_5YR_DP02/ACS_16_5YR_DP02_with_ann.csv')


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

d_11 = info(data_11)

d_12 = info(data_12)

d_13 = info(data_13)

d_14 = info(data_14)

d_15 = info(data_15)

d_16 = info(data_16)


# Total Households in each state over the years
def thh_yy(df, yy):
    groupby_state = df.groupby(['State'])
    total_households_yy = pd.DataFrame(groupby_state.sum()['Total Households'])
    return total_households_yy.rename(columns={'Total Households': 'Total Households in {}'.format(yy)})

thh = thh_yy(d_10, '2010').merge(thh_yy(d_11, '2011'), left_index=True, right_index=True).merge(thh_yy(d_12, '2012'), left_index=True, right_index=True).merge(thh_yy(d_13, '2013'), left_index=True, right_index=True).merge(thh_yy(d_14, '2014'), left_index=True, right_index=True).merge(thh_yy(d_15, '2015'), left_index=True, right_index=True).merge(thh_yy(d_16, '2016'), left_index=True, right_index=True)
thh.to_csv('total_households.csv')

drugs_overall = pd.read_csv('state_by_year.csv')
households_overall = pd.read_csv('total_households.csv')
drugs_households_state = drugs_overall.merge(households_overall, left_on='State', right_on='State')

def drugs_households():
    drugs_households = pd.DataFrame()
    for y in range(2010,2017):
        drugs_households['State'] = drugs_households_state['State']
        drugs_households[y] = drugs_households_state[str(y)]/drugs_households_state['Total Households in {}'.format(y)]
    return drugs_households
drugs_households = drugs_households()
drugs_households.to_csv('drugs_households.csv')


oh=drugs_households.loc[0]
pa=drugs_households.loc[1]
va=drugs_households.loc[2]
ky=drugs_households.loc[3]
wv=drugs_households.loc[4]
print(oh)
print(pa)
def state_drugs_households(df):
    list_value = []
    for value in df.values[1:]:
        list_value.append(float(value))
    return list_value
plt.ylim(0,25)
line_oh = plt.plot(range(2010,2017), state_drugs_households(oh), marker = 'o', linewidth=2, markersize=8, label = 'OH')
line_pa = plt.plot(range(2010,2017), state_drugs_households(pa), marker = 'o', linewidth=2, markersize=8, label = 'PA')
line_va = plt.plot(range(2010,2017), state_drugs_households(va), marker = 'o', linewidth=2, markersize=8, label = 'VA')
line_ky = plt.plot(range(2010,2017), state_drugs_households(ky), marker = 'o', linewidth=2, markersize=8, label = 'KY')
line_wv = plt.plot(range(2010,2017), state_drugs_households(wv), marker = 'o', linewidth=2, markersize=8, label = 'WV')
plt.legend()
plt.savefig('Number of drug reports per household in every state from 2010 to 2016')

