# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 17:33:10 2019

@author: Rully
"""

import numpy as np
import pandas as pd
import random
from timeit import default_timer as timer

data = pd.read_csv('ear-f-83.stu', delimiter=' ', names=list(range(20))).dropna(axis='columns', how='all')

data = data.fillna(-1)

data.iloc[:,:len(data.columns)] = data.iloc[:,:len(data.columns)].values.astype(int)

arr = np.zeros((data.max().max(), data.max().max()))
arr = pd.DataFrame(arr).values.astype(int)

for i in range(0, len(data)):
    k=0
    l=0
    j=1
    while j!=len(data.columns):
        z = j+l
        if data.iloc[i,k]!=-1 and data.iloc[i,z]!=-1:
            arr[data.iloc[i,k]-1][data.iloc[i,z]-1] += 1
            arr[data.iloc[i,z]-1][data.iloc[i,k]-1] += 1
        if z==len(data.columns)-1:
            k += 1
            l += 1
            j = 0
        if k==len(data.columns)-1:
            break
        j += 1

arr = pd.DataFrame(arr)

degree = []

for i in range(len(arr)):
    num = 0
    for j in range(len(arr)):
        if arr.iloc[i,j]!=0 :
            num+=1
    degree.append(num)
        
degree = pd.DataFrame(degree)        

sorting_degree = pd.DataFrame(degree[0].sort_values(ascending=False))
       
arr2 = pd.DataFrame(index = sorting_degree.index)
for i in range(len(arr.columns)):
    arr3 = pd.DataFrame(index = sorting_degree.index, data=arr.iloc[:,sorting_degree.index[i]])
    arr2 = pd.concat([arr2,arr3], axis=1)
    
List = pd.DataFrame([], columns=['ts'])
for i in range(len(arr2)):
    for j in range(len(arr2.columns)):
        if List.index[List['ts']==j].size>0:
            z=0
            for m in List.index[List['ts']==j]:
                if arr2.loc[arr2.index[i],m]!=0:
                    z+=1
            if z==0:
                List = List.append(pd.DataFrame([j], columns=['ts'], index=[arr2.index[i]]))
                break
        elif List.index[List['ts']==j].size==0:
            if List['ts'].size==0:
                List = List.append(pd.DataFrame([0], columns=['ts'], index=[arr2.index[i]]))
                break
            elif List['ts'].size>0:
                List = List.append(pd.DataFrame([max(List['ts'])+1], columns=['ts'], index=[arr2.index[i]]))
                break
    
timeslot = []
for i in range(max(List['ts'])+1):
    timeslot.append(List.index[List['ts']==i].values)    
    
#List['index'] = List.index
#List = List[['index', 'ts']]
#
#List.sort_values(by=['index'], inplace=True)
#List['index'] += 1
#List['ts'] += 1   
#        
#List.to_csv('Carleton92.sol', header=False, index=False, sep=' ') 

# --------------------------------------------------------------------------- #
pinalty_temp = []
for i in range(len(sorting_degree.index)):
    for j in range(i+1, len(sorting_degree.index)):
        student = arr2.loc[sorting_degree.index[i], sorting_degree.index[j]]
        weight = 2**(5-abs(List.loc[sorting_degree.index[i],'ts']-List.loc[sorting_degree.index[j],'ts']))
        pinalty_temp.append(student*weight)

pinalty = sum(pinalty_temp)/len(data)
# --------------------------------------------------------------------------- #
start = timer()

List_temp = List.copy()
hill_climbing_pinalty = pinalty.copy()
for i in range(1000):
    x = random.choice(List_temp.index)
    y = random.choice(List_temp['ts'])
    List_temp.loc[x,'ts'] = y
    z=0
    for k in List_temp.index[List['ts']==y]:
        if arr2.loc[x,k]!=0:
            List_temp.loc[x,'ts'] = List.loc[x,'ts']
            z+=1
            break
    if z==0:
        pinalty_temp = []
        for o in range(len(sorting_degree.index)):
            for p in range(o+1, len(sorting_degree.index)):
                student = arr2.loc[sorting_degree.index[o], sorting_degree.index[p]]
                weight = 2**(5-abs(List_temp.loc[sorting_degree.index[o],'ts']-List_temp.loc[sorting_degree.index[p],'ts'])).astype(float)
                pinalty_temp.append(student*weight)
        new_pinalty = sum(pinalty_temp)/len(data)
        if hill_climbing_pinalty > new_pinalty:
            hill_climbing_pinalty = new_pinalty.copy()
        elif hill_climbing_pinalty < new_pinalty:
            List_temp.loc[x,'ts'] = List.loc[x,'ts']

end = timer()
print(str(end-start))
# --------------------------------------------------------------------------- #

delta = "{:.1%}".format(abs((hill_climbing_pinalty-pinalty)/pinalty))


  