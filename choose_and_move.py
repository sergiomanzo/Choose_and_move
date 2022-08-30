#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
import itertools
import threading
import time
import sys


# In[2]:


cities = ['Dublin','Amsterdam','Madrid','Paris','Berlin','Milan','London','Barcelona','Frankfurt','Lisbon']
roles_list =['Junior Data Analyst','Junior Web Developer']
#Glassdoor
da_table=pd.read_csv('glassdoor_role_table_unique2roles.csv')
#Numbeo
numbeo_summary_table = pd.read_csv('numbeo_table_summary.csv')
numbeo_item_table =  pd.read_csv('numbeo_table_priceitems.csv')
numbeo_item_table.rename(columns = {'Country':'City'}, inplace = True)
#Nomad list
nomad_list =pd.read_csv('df_nomad_list.csv')
#Columns adjugement
columnsok = []
for x in nomad_list.columns[1:]:
    b = re.findall(r'(?<=\s).*',x)
    columnsok.append(b)
columnsok
col = []

for x in range(0,80):
     col.append(columnsok[x][0])
col.insert(0,"City")
col
nomad_list.set_axis(col,axis=1,inplace=True)
#Functions
def city_validation(city_val):
    #validates city in list
    while  True:
        if city_val not in cities:
            print("Sorry, we dont have information for that city, try again:")
            city_val = input('Introduce city: ').strip().capitalize()
            True
        else:
            break
    return city_val
def role_validation(role_val):
    #validates city in list
    while  True:
        if role_val not in roles_list:
            print("Sorry, we dont have information for that role, try again:")
            role_val = input('Introduce the role exactly as listed above: ').strip()
            True
        else:
            break
    return role_val


# In[3]:


#MAin program

print('\033[1m','....................................Welcome to Choose&Move....................................''\033[0m')
#Scraping proccess simulation
#TBD
done = False
#here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rScraping last updates     ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    print('\rDone:Last update:Updated 7 May 2022      ')

t = threading.Thread(target=animate)
t.start()

#long process here
time.sleep(1)
done = True
print("\n")


#long process here
time.sleep(2)
done = True
#program
print('    ')
print('\033[94m','Information available for:','\033[0m')
[print('\033[0;32m',city,'\033[0m') for city in cities]
print('    ')
#city_orig = input('Introduce current city: ').capitalize().strip()
#city_dest = input('Introduce city to compare: ').capitalize().strip()
city_orig = city_validation(input('Introduce current city: ').strip().capitalize())
city_dest = city_validation(input('Introduce city to compare: ').strip().capitalize())

print('    ')
print('\033[0;34m','Information available for:','\033[0m')
#print('\033[0;32m','Junior Data Analyst''\033[0m')
#print('\033[0;32m','Junior Web Developer''\033[0m')
print('    ')
[print('\033[0;32m',role,'\033[0m') for role in roles_list ]
print('    ')
#role= input('Role position to analyze: ',).strip()
role= role_validation(input('Role position to analyze: ',).strip())
print('    ')
#filter table by position and role
df_1 = da_table[(da_table['city'] == city_orig) | (da_table['city'] == city_dest)]
df_1= df_1[df_1.position.str.contains(f'{role}', flags = re.IGNORECASE, regex = True, na = False)].reset_index()

print('\033[0;34m' ,'Salary reference:','\033[0m')

#Avg salary origin  and to comparecity
avg_org_city = df_1["avgbasepay"][df_1['city'] == city_orig].reset_index()
avg_org_city = avg_org_city['avgbasepay'][0]
avg_org_city
avg_dest_city = df_1["avgbasepay"][df_1['city'] == city_dest].reset_index()
avg_dest_city =avg_dest_city['avgbasepay'][0]
avg_dest_city

print(f'Average salary in {city_orig} : {avg_org_city} | {city_dest} : {avg_dest_city}  ')
print('    ')
print('\033[0;34m' ,'Range Salaries:','\033[0m')
#Range Salaries table
df_1.rename(columns = {'city':'City', 'minpay':'Low','avgpay':'Average', 'maxpay':'High'}, inplace = True)
#Changing colum names
#Ldisplay(df_1[['City','Low','Average','High']])
print(df_1[['City','Low','Average','High']])
#Cost of life part
print('    ')
print('\033[0;34m' ,'Cost of Life:','\033[0m')

#Estimated monthly costs single person without rent
df_2 = numbeo_summary_table[(numbeo_summary_table['City'] == city_orig) | (numbeo_summary_table['City'] == city_dest)].reset_index()
cost_cityorig = df_2["A single person estimated monthly costs are without rent."][df_2['City'] == city_orig].reset_index()
cost_cityorig = cost_cityorig["A single person estimated monthly costs are without rent."][0]
cost_cityorig
#cost_cityorig
cost_citydest = df_2["A single person estimated monthly costs are without rent."][df_2['City'] == city_dest].reset_index()
cost_citydest = cost_citydest["A single person estimated monthly costs are without rent."][0]
cost_citydest
#cost_citydest

#Apartment (1 bedroom) in City Centre
df_3 = numbeo_item_table[(numbeo_item_table['City'] == city_orig) | (numbeo_item_table['City'] == city_dest)].reset_index()
apartment1bed_cityorig = df_3['Apartment (1 bedroom) in City Centre '][df_3['City'] == city_orig].reset_index()
apartment1bed_cityorig = apartment1bed_cityorig['Apartment (1 bedroom) in City Centre '][0]
apartment1bed_cityorig
#apartment1bed_cityorig
apartment1bed_citydest = df_3['Apartment (1 bedroom) in City Centre '][df_3['City'] == city_dest].reset_index()
apartment1bed_citydest =apartment1bed_citydest['Apartment (1 bedroom) in City Centre '][0]
apartment1bed_citydest
#apartment1bed_citydest

#Apartment (1 bedroom) in City Centre
df_4 = numbeo_item_table[(numbeo_item_table['City'] == city_orig) | (numbeo_item_table['City'] == city_dest)].reset_index()
sal_cityorig = df_4['Average Monthly Net Salary (After Tax) '][df_4['City'] == city_orig].reset_index()
sal_cityorig =sal_cityorig['Average Monthly Net Salary (After Tax) '][0]
#sal_cityorig
sal_citydest = df_4['Average Monthly Net Salary (After Tax) '][df_4['City'] == city_dest].reset_index()
sal_citydest = sal_citydest['Average Monthly Net Salary (After Tax) '][0]
sal_citydest
#sal_citydest



print(f'Average Monthly Net Salary (After Tax):  {city_orig}:','€', sal_cityorig,' | ',f'{city_dest}:','€',sal_citydest)
print(f'Estimated monthly costs single person without rent:  {city_orig}:','€', cost_cityorig,' | ',f'{city_dest}:','€',cost_citydest)
print(f'Apartment (1 bedroom) in City Centre:  {city_orig}:','€', apartment1bed_cityorig,' | ',f'{city_dest}:','€',apartment1bed_citydest)
print(' ')

print('\033[0;34m' ,'Quality of life:','\033[0m')

df_5 = nomad_list[(nomad_list['City'] == city_orig) | (nomad_list['City'] == city_dest)].reset_index()
#NightLife
nightlife_dest =df_5['Nightlife'][df_5['City'] == city_dest].reset_index()
nightlife_dest =nightlife_dest['Nightlife'][0]
nightlife_dest

nightlife_org= df_5['Nightlife'][df_5['City'] == city_orig].reset_index()
nightlife_org=nightlife_org['Nightlife'][0]
nightlife_org
#Fun
fun_dest = df_5['Fun'][df_5['City'] == city_dest].reset_index()
fun_dest =fun_dest['Fun'][0]
fun_dest
fun_org= df_5['Fun'][df_5['City'] == city_orig].reset_index()
fun_org=fun_org['Fun'][0]
fun_org

#Fender ratio
gender_dest = df_5['Gender ratio (overall)'][df_5['City'] == city_dest].reset_index()
gender_dest=gender_dest['Gender ratio (overall)'][0]
gender_dest
gender_org= df_5['Gender ratio (overall)'][df_5['City'] == city_orig].reset_index()
gender_org=gender_org['Gender ratio (overall)'][0]


print(f'Night Life in {city_orig}:',nightlife_org,f' in {city_dest}:',nightlife_dest)
print(f'Fun in {city_orig}:',fun_org,f' in {city_dest}:',fun_dest)
print(f'Gender Ratio in {city_orig}:',gender_org,f' in {city_dest}:',gender_dest)


# In[ ]:





# In[ ]:




