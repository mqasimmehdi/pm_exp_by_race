# Written by: QM

import pandas as pd
import seaborn as sns

#reading in pm and population data
pm = pd.read_csv('pm.csv')
demo = pd.read_csv('2019demo.csv')


#performing join on the pm and data file
pm = pm.merge(demo, on=['state', 'county'], how = 'inner', validate='1:1', indicator=True)

#Estimating the percentage share of black and whites 
pm['total_black'] = pm['nonhisp_black'].sum()
pm['total_white'] = pm['nonhisp_white'].sum()
pm['black_ratio'] = pm['nonhisp_black']/pm['total_black']
pm['white_ratio'] = pm['nonhisp_white']/pm['total_white']

#Summing by pm value
pm['pm_round']= round(pm['area_weighted_pm']).astype('int')
group = pm.groupby(['pm_round'], as_index=False)
sum_pm = group.sum()
sum_pm = sum_pm [['pm_round', 'white_ratio', 'black_ratio']]
scenarios = sum_pm [['pm_round', 'white_ratio', 'black_ratio']]


#stacking the data
scenario_stack = scenarios.set_index(['pm_round'])
scenario_stack = scenario_stack.stack()
scenario_stack = scenario_stack.reset_index(level=['pm_round'])
scenario_stack['type'] = scenario_stack.index
scenario_stack['ratio'] = scenario_stack[0]

#Creating a barplot
fig, ax = plt.subplots(dpi =300)
ax.set_ylim(0,.3)
sns.barplot(data = scenario_stack, x= 'pm_round', y = 'ratio', hue="type")
plt.title("BAU 2030: Base Scenario")
plt.xlabel('pm')
plt.savefig('base_scenario.png', dpi =300)




