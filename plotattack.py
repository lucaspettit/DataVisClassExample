import os

import matplotlib.pyplot as plt
import pandas as pd
import requests
from census import Census


def get_census_info():
  c = Census(os.environ['CENSUS_API_KEY'])
  # Run Census Search to retrieve data on all states
  # Note the addition of "B23025_005E" for unemployment count
  census_data = c.acs5.get(("NAME", "B19013_001E", "B01003_001E", "B01002_001E",
                            "B19301_001E",
                            "B17001_002E",
                            "B23025_005E"), {'for': 'state:*'})

  # Convert to DataFrame
  census_pd = pd.DataFrame(census_data)

  # Column Reordering
  census_pd = census_pd.rename(columns={
    "B01003_001E": "Population",
    "B01002_001E": "Median Age",
    "B19013_001E": "Household Income",
    "B19301_001E": "Per Capita Income",
    "B17001_002E": "Poverty Count",
    "B23025_005E": "Unemployment Count",
    "NAME": "Name", "state": "State"})

  # Add in Poverty Rate (Poverty Count / Population)
  census_pd["Poverty Rate"] = 100 * \
                              census_pd["Poverty Count"].astype(
                                int) / census_pd["Population"].astype(int)

  # Add in Employment Rate (Employment Count / Population)
  census_pd["Unemployment Rate"] = 100 * \
                                   census_pd["Unemployment Count"].astype(
                                     int) / census_pd["Population"].astype(int)

  # Final DataFrame
  census_pd = census_pd[["Name", "Population", "Median Age", "Household Income",
                         "Per Capita Income", "Poverty Count", "Poverty Rate", "Unemployment Rate"]]
  census_pd.set_index('Name', inplace=True)

  return census_pd


def plot_correlation_matrix(df):
  f = plt.figure(figsize=(12, 10))
  plt.matshow(df.corr(), fignum=f.number)
  plt.xticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=10, rotation=45, ha='left')
  plt.yticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=10)
  cb = plt.colorbar()
  cb.ax.tick_params(labelsize=12)
  plt.title('Correlation Matrix', fontsize=14)
  plt.tight_layout()
  plt.show()


if __name__ == '__main__':
  df = get_census_info()
  print('starting to plot stuff')
  plot_correlation_matrix(df)
  print('ok we\'re all finished')
