# Written by: QM

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas

#reading in pm and population data
pm = pd.read_csv('pm.csv')
demo = pd.read_csv('2019demo.csv')


#performing join on the pm and data file
pm = pm.merge(demo, on=['state', 'county'], how = 'inner', validate='1:1', indicator=True)
pm = pm.rename(columns = {'area_weighted_pm': 'pm'})


#Pm Map by County

#Kernel Density plots
kd_pm = pm[['total', 'nonhisp_white', 'nonhisp_black', 'nonhisp_NA_alaska','nonhisp_hawai_pacific', 'nonhisp_asian', 'hisp_white', 'hisp_black', 'pm']]

#stacking the data
kd_pm = kd_pm.set_index(['pm'])
kd_pm = kd_pm.stack()
kd_pm = kd_pm.reset_index(level=['pm'])
kd_pm['pop'] = kd_pm[0]
kd_pm = kd_pm.reset_index()
kd_pm = kd_pm.rename(columns = {'index': 'race'})
kd_pm['race'] = kd_pm['race'].astype('str')


#selecting few races, so that the kd plots dont get cluttered

data = kd_pm.query("race == 'nonhisp_white' or race=='nonhisp_black' or race=='nonhisp_asian' or race=='nonhisp_NA_alaska'")
data = data.query("pm <= 25")


fig, ax = plt.subplots(dpi =300)

sns.kdeplot(data=data, x="pm", weights="pop", bw_adjust=.20, legend=True, hue="race")
plt.title('PM 2.5 exposure by Race (with population weights)')
plt.savefig('kernal_density.png')

#Mean Barplots
#Race sum
group = kd_pm.groupby(['race'])
race = group.sum()
race = race[['pop']]
race = race.reset_index()
race = race.rename(columns = {'pop': 'tot_pop'})
race['race'] = race['race'].astype('str')

#weighting pm by race
kd_pm['pm_exp'] = kd_pm['pop']*kd_pm['pm'] 
kd_pm = kd_pm.merge(race, on=['race'], how = 'inner', validate='m:1', indicator=True)
kd_pm['weights'] = kd_pm['pm_exp']/kd_pm['tot_pop']
group = kd_pm.groupby(['race'])
race = group.sum()
race = race.reset_index()

 

fig, ax = plt.subplots(dpi =300, figsize=(8, 6))

sns.barplot(data=race, x="race", y='weights')
ax.set_xticklabels(ax.get_xticklabels(),rotation=30)
plt.title('Mean PM 2.5 exposure by Race (with population weights)')
plt.xticks((0, 1, 2, 3, 4, 5, 6, 7), ('Blacks', 'Whites', 'Native', 'Asian', 'Hispanic Black', 'Islanders', 'Hispanic White', 'Total'))
plt.savefig('bar_plot.png')


# PM Exposure Map
# Loading in the shape files and removing the unwanted states and counties
state = geopandas.read_file("cb_2019_us_state_20m.zip")
county = geopandas.read_file("cb_2019_us_county_20m.zip")
stateToRemove = ['02', '03', '07', '14', '15', '43', '52','60', '66', '69', '72', '78', '84']
state = state[~state['STATEFP'].isin(stateToRemove)]
county = county[~county['STATEFP'].isin(stateToRemove)]



#Add 0 pads, and merging
pm['county'] = pm['county'].astype('str')
pm['state'] = pm['state'].astype('str')
pm['state'] = pm['state'].str.zfill(2)
pm['county'] = pm['county'].str.zfill(3)

merged = county.merge(pm, left_on=['STATEFP', 'COUNTYFP'], right_on=['state', 'county'], validate='1:1')

#Ploting the Map
merged = merged.to_crs(epsg=5070)
state = state.to_crs(epsg=5070)





fig, ax = plt.subplots(dpi = 500)
fig.suptitle('PM 2.5 (µg/m3)')
state.boundary.plot(ax=ax, edgecolor = 'black', linewidth=0.1)
merged.plot(column='pm', cmap='OrRd', legend=True, edgecolor='grey', ax=ax, vmin=0, vmax=20, linewidth=0.1)
plt.axis('off')
plt.savefig('PM_map_1.png')


fig, ax = plt.subplots(dpi = 500)
fig.suptitle('PM 2.5 (µg/m3)')
state.boundary.plot(ax=ax, edgecolor = 'black', linewidth=0.1)
merged.plot(column='pm', cmap='OrRd', legend=True, edgecolor='grey', ax=ax, vmin=0, vmax=10, linewidth=0.1)
plt.axis('off')
plt.savefig('PM_map_2.png')
