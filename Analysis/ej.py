# QM

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas

#reading in pm and population data
pm = pd.read_csv('pm.csv')
demo = pd.read_csv('2019demo.csv')



pm = pm.merge(demo, on=['state', 'county'], how = 'inner', validate='1:1', indicator=True)
pm['total_black'] = pm['nonhisp_black'].sum()
pm['total_white'] = pm['nonhisp_white'].sum()
pm['black_ratio'] = pm['nonhisp_black']/pm['total_black']
pm['white_ratio'] = pm['nonhisp_white']/pm['total_white']

pm['pm_round']= round(pm['pm']).astype('int')
group = pm.groupby(['pm_round'], as_index=False)
sum_pm = group.sum()


sns.set_style("whitegrid")


fig = sns.barplot(data = sum_pm, x= 'pm_round', y = 'black_ratio')
fig = fig.set(ylim= (0, 0.25))
fig = plt.title("BAU 2030: Black pm Exposure")
plt.savefig('black_pm_weighted.png')

         

                    
fig = sns.barplot(data = sum_pm, x= 'pm_round', y = 'white_ratio')
fig = fig.set(ylim= (0, 0.25))
fig = plt.title("BAU 2030: White pm Exposure")
plt.savefig('white_pm_weighted.png')




sum_pm = sum_pm [['pm_round', 'white_ratio', 'black_ratio']]
scenarios = sum_pm [['pm_round', 'white_ratio', 'black_ratio']]
sum_pm.loc[(sum_pm['pm_round'] >=9), 'flag'] = 1
sum_pm['flag'] = sum_pm['flag'].fillna(0)
sum_pm['flag']= (sum_pm['flag']).astype('int')

group = sum_pm.groupby('flag')
redist = group.sum()
redist['b_move'] = redist['black_ratio'] - redist['white_ratio']



num = redist.loc[1, "b_move"]
redist['b_scale'] = (num + redist['black_ratio'])/redist['black_ratio']
scale = redist.loc[0, "b_scale"]




sum_pm['scaled_b'] = sum_pm['black_ratio'] * scale
sum_pm.loc[sum_pm['flag'] ==1, 'scaled_b'] = sum_pm['white_ratio']




fig = sns.barplot(data = sum_pm, x= 'pm_round', y = 'scaled_b')
fig = fig.set(ylim= (0, 0.25))
fig = plt.title("BAU 2030: Black pm Exposure (Scaled)")
plt.savefig('black_pm_weighted_scaled.png', dpi =300)



pop_sum_pm['da'] = pop_sum_pm['black_ratio'] - pop_sum_pm['white_ratio']
pop_sum_pm['dc'] = pop_sum_pm['scaled_b'] - pop_sum_pm['white_ratio']

pop_sum_pm['exp_da'] = pop_sum_pm['da']*pop_sum_pm['pm_round']
pop_sum_pm['exp_dc'] = pop_sum_pm['dc']*pop_sum_pm['pm_round']
stack = pop_sum_pm[['pm_round', 'exp_da','exp_dc']]
stacky = stack.set_index(['pm_round'])
stacky = stacky.stack()
stacky = stacky.reset_index(level=['pm_round'])
stacky['type'] = stacky.index
stacky['value'] = stacky[0]

fig = sns.barplot(data = stacky, x= 'pm_round', y = 'value', hue="type")
plt.savefig('barplot_exp.png', dpi =300)


print(round((pop_sum_pm['da']*pop_sum_pm['pm_round']).sum(), 2))
print(round((pop_sum_pm['dc']*pop_sum_pm['pm_round']).sum(), 2))

## By race for 3 scenarios
## Scenario 1: Real
scenarios = scenarios[['pm_round', 'white_ratio', 'black_ratio']]
scenario_stack = scenarios.set_index(['pm_round'])
scenario_stack = scenario_stack.stack()
scenario_stack = scenario_stack.reset_index(level=['pm_round'])
scenario_stack['type'] = scenario_stack.index
scenario_stack['ratio'] = scenario_stack[0]
fig, ax = plt.subplots()
ax.set_ylim(0,.3)
sns.barplot(data = scenario_stack, x= 'pm_round', y = 'ratio', hue="type")
plt.title("BAU 2030: Base Scenario")

plt.savefig('base_scenario.png', dpi =300)

## Scenrio 2: Counter-factual 
cf1 = scenarios.copy()

cf1['flag'] = [1 if val == 13 or val == 20 else 0 for val in cf1['pm_round']]



cf1['flag'] = cf1['flag'].fillna(0)
cf1['flag']= (cf1['flag']).astype('int')

group = cf1.groupby('flag')
redist = group.sum()
redist['b_move'] = redist['black_ratio'] - redist['white_ratio']



num = redist.loc[1, "b_move"]
redist['b_scale'] = (num + redist['black_ratio'])/redist['black_ratio']
scale = redist.loc[0, "b_scale"]




cf1['black_ratio'] = cf1['black_ratio'] * scale
cf1.loc[cf1['flag'] ==1, 'black_ratio'] = cf1['white_ratio']
cf1 = cf1[['pm_round', 'white_ratio', 'black_ratio']]


scenario_stack = cf1.set_index(['pm_round'])
scenario_stack = scenario_stack.stack()
scenario_stack = scenario_stack.reset_index(level=['pm_round'])
scenario_stack['type'] = scenario_stack.index
scenario_stack['ratio'] = scenario_stack[0]

fig, ax = plt.subplots()
ax.set_ylim(0,.3)
sns.barplot(data = scenario_stack, x= 'pm_round', y = 'ratio', hue="type")
plt.title("BAU 2030: Shift in PM2.5 '13' and '20' exp")
plt.savefig('base_scenario2.png', dpi =300)

## Scenario 3: Counter-factual 2
cf2 = scenarios.copy()

cf2['flag'] = [1 if val > 9 else 0 for val in cf2['pm_round']]



cf2['flag'] = cf2['flag'].fillna(0)
cf2['flag']= (cf2['flag']).astype('int')

group = cf2.groupby('flag')
redist = group.sum()
redist['b_move'] = redist['black_ratio'] - redist['white_ratio']



num = redist.loc[1, "b_move"]
redist['b_scale'] = (num + redist['black_ratio'])/redist['black_ratio']
scale = redist.loc[0, "b_scale"]




cf2['black_ratio'] = cf2['black_ratio'] * scale
cf2.loc[cf2['flag'] ==1, 'black_ratio'] = cf2['white_ratio']
cf2 = cf2[['pm_round', 'white_ratio', 'black_ratio']]


scenario_stack = cf2.set_index(['pm_round'])
scenario_stack = scenario_stack.stack()
scenario_stack = scenario_stack.reset_index(level=['pm_round'])
scenario_stack['type'] = scenario_stack.index
scenario_stack['ratio'] = scenario_stack[0]

fig, ax = plt.subplots()
ax.set_ylim(0,.3)
sns.barplot(data = scenario_stack, x= 'pm_round', y = 'ratio', hue="type")
plt.title("BAU 2030: Shift in PM2.5 > 9 exp")
plt.savefig('base_scenario3.png', dpi =300)