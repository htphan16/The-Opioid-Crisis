import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Tentative approach/code to Problem Investigation 1
# Not all results shown here will get into the paper

drugs_df = pd.read_csv('MCM_NFLIS_Data.csv')
groupby_state = drugs_df.groupby(['State'])
groupby_county = drugs_df.groupby(['State', 'COUNTY'])
groupby_year = drugs_df.groupby(['YYYY'])
groupby_year_state = drugs_df.groupby(['YYYY', 'State'])
groupby_year_county = drugs_df.groupby(['YYYY', 'State', 'COUNTY'])

# Over the years
data_year = groupby_year.sum()['TotalDrugReportsState'].fillna(0)
print(data_year)
data_state_by_year = groupby_year_state.sum()['TotalDrugReportsState'].fillna(0)
data_state_by_county = groupby_year_county.sum()['TotalDrugReportsCounty'].fillna(0)

# States in order of decreasing number drug reports in 2010, including all data from 2010 to 2017
def state_by_year():
	state_by_year = pd.DataFrame()
	for year in range(2010, 2018):
		state_by_year[year] = data_state_by_year.sort_values(ascending=False)[year]
		
	return state_by_year

state_by_year = state_by_year()
print(state_by_year)
state_by_year.to_csv('state_by_year.csv')

oh_by_year = state_by_year.transpose()['OH']
pa_by_year = state_by_year.transpose()['PA']
va_by_year = state_by_year.transpose()['VA']
ky_by_year = state_by_year.transpose()['KY']
wv_by_year = state_by_year.transpose()['PA']

# using scatterplot to predict where and when drugs threhold levels will occur
#plt.scatter(x = list(oh_by_year.index), y = list(oh_by_year.values))
#plt.show()
#plt.scatter(x = list(pa_by_year.index), y = list(pa_by_year.values))
#plt.show()
#plt.scatter(x = list(va_by_year.index), y = list(va_by_year.values))
#plt.show()
#plt.scatter(x = list(ky_by_year.index), y = list(ky_by_year.values))
#plt.show()
#plt.scatter(x = list(wv_by_year.index), y = list(wv_by_year.values))
#plt.show()

sum_by_year = state_by_year.sum()
#plt.scatter(x = list(sum_by_year.index), y = list(sum_by_year.values))
#plt.show()
#print(state_by_year.describe())

# Counties in each state in order of decreasing number of drug reports in 2010, including all data from 2010 to 2017
def county_by_state_by_year(state):
	county_by_state_by_year = pd.DataFrame()
	for year in range(2010, 2018):
		county_by_state_by_year[year] = data_state_by_county.sort_values(ascending=False)[year][state]
	return county_by_state_by_year

county_by_oh_by_year = county_by_state_by_year('OH')
county_by_pa_by_year = county_by_state_by_year('PA')
county_by_va_by_year = county_by_state_by_year('VA')
county_by_ky_by_year = county_by_state_by_year('KY')
county_by_wv_by_year = county_by_state_by_year('WV')

#county_by_oh_by_year.to_csv('ohio_counties_sort_by_2010.csv', encoding='utf-8')
#county_by_pa_by_year.to_csv('pennsylvania_counties_sort_by_2010.csv', encoding='utf-8')
#county_by_va_by_year.to_csv('virginia_counties_sort_by_2010.csv', encoding='utf-8')
#county_by_ky_by_year.to_csv('kentucky_counties_sort_by_2010.csv', encoding='utf-8')
#county_by_wv_by_year.to_csv('west-virginia_counties_sort_by_2010.csv', encoding='utf-8')

h_adj_county_ky = county_by_ky_by_year.loc[['BOONE', 'CAMPBELL', 'KENTON']]
h_adj_county_oh = county_by_oh_by_year.loc[['HAMILTON', 'BUTLER', 'CLERMONT', 'WARREN']]
hamiton_neighbors = pd.concat([h_adj_county_ky, h_adj_county_oh]).transpose()
hamiton_neighbors.plot()
plt.savefig("Hamilton's neighboring counties' drugs reports over the years")

'''c_adj_county_oh = county_by_oh_by_year.loc[['CUYAHOGA', 'LAKE', 'GEAUGA', 'LORAIN', 'MEDINA', 'PORTAGE', 'SUMMIT']]
cuyahoga_neighbors = c_adj_county_oh.transpose()
cuyahoga_neighbors.plot()
plt.savefig("Cuyahoga's neighboring counties' drugs reports over the years")'''

m_adj_county_oh = county_by_oh_by_year.loc[['MONTGOMERY', 'BUTLER', 'CLARK', 'DARKE', 'GREENE', 'MIAMI', 'PREBLE', 'WARREN']]
montgomery_neighbors = m_adj_county_oh.transpose()
montgomery_neighbors.plot()
plt.savefig("Montgomery's neighboring counties' drugs reports over the years")

'''s_adj_county_oh = county_by_oh_by_year.loc[['STARK', 'CARROLL', 'COLUMBIANA', 'HOLMES', 'MAHONING', 'PORTAGE', 'SUMMIT', 'TUSCARAWAS', 'WAYNE']]
stark_neighbors = s_adj_county_oh.transpose()
stark_neighbors.plot()
plt.savefig("Stark's neighboring counties' drugs reports over the years")

f_adj_county_oh = county_by_oh_by_year.loc[['FRANKLIN', 'DELAWARE', 'FAIRFIELD', 'LICKING', 'MADISON', 'PICKAWAY', 'UNION']]
franklin_neighbors = f_adj_county_oh.transpose()
franklin_neighbors.plot()
plt.savefig("Franklin's neighboring counties' drugs reports over the years")'''


state_by_year.transpose().plot()
#plt.savefig('Annual drug usage reports of each state from 2010 to 2017')
state_by_year.plot.bar(stacked=True)
#plt.savefig('Total drug usage reports of five states over 7 years')

# Overall across all years
# States in order of decreasing number of drug reports

data_state_overall = groupby_state.sum()['TotalDrugReportsState'].fillna(0)
state_overall = data_state_overall.sort_values(ascending=False)
print(state_overall)

data_county_overall = groupby_county.sum()['TotalDrugReportsCounty'].fillna(0)
county_oh = data_county_overall.sort_values(ascending=False)['OH']
county_pa = data_county_overall.sort_values(ascending=False)['PA']
county_va = data_county_overall.sort_values(ascending=False)['VA']
county_ky = data_county_overall.sort_values(ascending=False)['KY']
county_wv = data_county_overall.sort_values(ascending=False)['WV']
county_allstates = data_county_overall.sort_values(ascending=False)
print("Ohio's top ten counties with the most drug reports in all years", county_oh.head(10))
print("Pennsylvenia's top ten counties with the most drug reports in all years", county_pa.head(10))
print("Virginia's top ten counties with the most drug reports in all years", county_va.head(10))
print("Kentucky's top ten counties with the most drug reports in all years", county_ky.head(10))
print("West Virgnia's top ten counties with the most drug reports in all years", county_wv.head(10))
print("All 5 states's top ten counties with the most drug reports in all years", county_allstates.head(10))
