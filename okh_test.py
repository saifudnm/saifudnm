# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 17:33:10 2019

@author: Rully
"""

import numpy as np
import pandas as pd
import time

data = pd.read_csv('car-s-91.stu', delimiter=' ', names=list(range(20))).dropna(axis='columns', how='all')

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
start = time.time()
for i in range(len(arr2)):
    for j in range(len(arr2.columns)):
        if arr2.iloc[i,j]==0:
            if List.index[List['ts']==j].size>0:
                z=0
                for m in List.index[List['ts']==j]:
                    if arr2.iloc[i,m]!=0:
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
end = time.time()
print(end-start)    
    
timeslot = []
for i in range(max(List['ts'])+1):
    timeslot.append(List.index[List['ts']==i].values)    