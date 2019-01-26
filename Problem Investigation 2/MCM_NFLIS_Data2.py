import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Tentative approach/code to Problem Investigation 1
# Not all results shown here will get into the paper

drugs_df = pd.read_csv('MCM_NFLIS_Data.csv')
groupby_substance = drugs_df.groupby(['SubstanceName'])
groupby_substance_state = drugs_df.groupby(['State', 'SubstanceName'])
groupby_substance_county = drugs_df.groupby(['State', 'COUNTY', 'SubstanceName'])

data_substance = groupby_substance.sum()['TotalDrugReportsState'].fillna(0)
data_substance_state = groupby_substance_state.sum()['TotalDrugReportsState'].fillna(0)
data_substance_county = groupby_substance_county.sum()['TotalDrugReportsState'].fillna(0)
print(data_substance)