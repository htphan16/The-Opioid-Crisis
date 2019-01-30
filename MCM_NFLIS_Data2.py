import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


drugs_df = pd.read_csv('MCM_NFLIS_Data.csv')
groupby_substance = drugs_df.groupby(['SubstanceName'])
groupby_substance_state = drugs_df.groupby(['State', 'YYYY', 'SubstanceName'])
groupby_substance_county = drugs_df.groupby(['State', 'YYYY', 'COUNTY', 'SubstanceName'])

data_substance = groupby_substance.sum()['TotalDrugReportsState'].fillna(0)
data_substance_state = groupby_substance_state.sum()['TotalDrugReportsState'].fillna(0)
data_substance_county = groupby_substance_county.sum()['TotalDrugReportsState'].fillna(0)
print('Top 10 substance', data_substance.sort_values(ascending=False).head(10))

data_substance_state = groupby_substance_state.sum()['TotalDrugReportsState'].fillna(0)
data_substance_county = groupby_substance_county.sum()['TotalDrugReportsCounty'].fillna(0)

heroin_state = data_substance_state.loc[(data_substance_state.index.get_level_values('SubstanceName') == 'Heroin')]
heroin_county = data_substance_county.loc[(data_substance_county.index.get_level_values('SubstanceName') == 'Heroin')]
#heroin_ky = heroin_state.loc[('KY', 2010, 'Heroin')]
print(heroin_county.loc['KY'].sort_values(ascending=False))
#print(heroin_ky)
print(heroin_county.index.values)
