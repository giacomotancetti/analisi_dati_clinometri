#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 08:08:28 2019

@author: giacomo tancetti
"""

import pandas as pd

filename = "letture_clinometri.xlsx"

# lettura file excel     
df_excel = pd.read_excel(filename, sheet_name='dati')

# pulizia della colonna date da campo hh:mm:ss    
l_date_clean=[]
    
for data in df_excel.Date:
    day=data.date()
    l_date_clean.append(day)
    
df_excel.Date=l_date_clean

# impostazione della colonna Date come index
df_excel=df_excel.set_index("Date")
    
# creazione della lista date di misura      
l_date=[]

for data in l_date_clean:
    if data not in l_date:
        l_date.append(data)

# creazione della lista travi       
l_columns=df_excel.columns.tolist()

l_travi=[]
for name in l_columns:
    if name[-4:-2] not in l_travi:
        l_travi.append(name[-4:-2])
l_travi.sort()

# creazione della lista campate       
l_campate=[]
for name in l_columns:
    if name[3:6] not in l_campate:
        l_campate.append(name[3:6])

# impostazione limiti per ogni soglia
attenzione={'T2':[-0.32,0.46],'T3':[-0.32,0.35],'T4':[-0.32,0.35],'T5':[-0.32,0.35]}
allerta={'T2':[-0.36,0.51],'T3':[-0.36,0.38],'T4':[-0.36,0.38],'T5':[-0.36,0.51]}
allarme={'T2':[-0.66,0.63],'T3':[-0.66,0.65],'T4':[-0.66,0.63],'T5':[-0.66,0.65]}

db_eventi={"data":[],"campata":[],"trave":[],"n_attenzione":[],"n_allerta":[],"n_allarme":[]}

for campata in l_campate:
    
    for n_trave in l_travi:
        sel_cols = [col for col in df_excel.columns if col[3:6]==campata  and col[7:9]== n_trave]  
        df_sel_cols = df_excel[df_excel.columns.intersection(sel_cols)]    

        d_attenzione={}
        d_allerta={}
        d_allarme={}

        for i in range(0,len(l_date)):
            n_attenzione=0
            n_allerta=0
            n_allarme=0
            for row in df_sel_cols.loc[l_date[i]].values:
                for value in row:
                    if (value <= allarme[n_trave][0]) or (value >= allarme[n_trave][1]):
                        n_allarme=n_allarme+1
                    elif ((value > allarme[n_trave][0]) and (value <= allerta[n_trave][0])) or ((value < allarme[n_trave][1]) and (value >= allerta[n_trave][1])):
                        n_allerta=n_allerta+1
                    elif ((value > allerta[n_trave][0]) and (value <= attenzione[n_trave][0])) or ((value < allerta[n_trave][1]) and (value >= attenzione[n_trave][1])):
                        n_attenzione=n_attenzione+1

            db_eventi["data"].append(l_date[i])
            db_eventi["campata"].append(campata)
            db_eventi["trave"].append(n_trave)
            db_eventi["n_attenzione"].append(n_attenzione)
            db_eventi["n_allerta"].append(n_allerta)
            db_eventi["n_allarme"].append(n_allarme)
                       
df_eventi=pd.DataFrame(db_eventi)
df_eventi=df_eventi.set_index("data")

# creazione grafici
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# grafico superamenti soglia attenzione
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs=list(range(0,len(l_campate)))
zs=[1,2,3,4]

ys=[]
i=0

for trave in l_travi:
    ys.append([])
    
    for campata in l_campate:       
        ys[i].append(df_eventi[(df_eventi["campata"]==campata) & (df_eventi["trave"]==trave)]["n_attenzione"].sum())

    i=i+1
    
i=0
for z in zs:    
    ax.bar(xs, ys[i],zs=z,zdir='y', alpha=0.6)
    i=i+1

plt.title('SUPERAMENTI SOGLIA ATTENZIONE',fontsize=8)

#impostazioni titoli assi    
ax.set_xlabel('campate')
ax.set_ylabel('travi')
ax.set_zlabel('n superamenti soglia')

ax.xaxis.label.set_fontsize(8)
ax.yaxis.label.set_fontsize(8)
ax.zaxis.label.set_fontsize(8)

# impostazioni ticks
ax.yaxis.set_major_locator(plt.MaxNLocator(4))
ax.set_xticklabels(l_campate, fontdict=None, minor=False)
ax.set_yticklabels(l_travi, fontdict=None, minor=False)
ax.tick_params(axis='both', labelsize=8, pad=0.2)

# grafico superamenti soglia allerta
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs=list(range(0,len(l_campate)))
zs=[1,2,3,4]

ys=[]
i=0

for trave in l_travi:
    ys.append([])
    
    for campata in l_campate:       
        ys[i].append(df_eventi[(df_eventi["campata"]==campata) & (df_eventi["trave"]==trave)]["n_allerta"].sum())

    i=i+1
    
i=0
for z in zs:    
    ax.bar(xs, ys[i],zs=z,zdir='y', alpha=0.6)
    i=i+1

plt.title('SUPERAMENTI SOGLIA ALLERTA',fontsize=8)

#impostazioni titoli assi    
ax.set_xlabel('campate')
ax.set_ylabel('travi')
ax.set_zlabel('n superamenti soglia')

ax.xaxis.label.set_fontsize(8)
ax.yaxis.label.set_fontsize(8)
ax.zaxis.label.set_fontsize(8) 

# impostazioni ticks
ax.yaxis.set_major_locator(plt.MaxNLocator(4))
ax.set_xticklabels(l_campate, fontdict=None, minor=False)
ax.set_yticklabels(l_travi, fontdict=None, minor=False)
ax.tick_params(axis='both', labelsize=8, pad=0.2)

# grafico superamenti soglia allarme
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs=list(range(0,len(l_campate)))
zs=[1,2,3,4]

ys=[]
i=0

for trave in l_travi:
    ys.append([])
    
    for campata in l_campate:       
        ys[i].append(df_eventi[(df_eventi["campata"]==campata) & (df_eventi["trave"]==trave)]["n_allarme"].sum())

    i=i+1
    
i=0
for z in zs:    
    ax.bar(xs, ys[i],zs=z,zdir='y', alpha=0.6)
    i=i+1

plt.title('SUPERAMENTI SOGLIA ALLARME',fontsize=8)

#impostazioni titoli assi    
ax.set_xlabel('campate')
ax.set_ylabel('travi')
ax.set_zlabel('n superamenti soglia')

ax.xaxis.label.set_fontsize(8)
ax.yaxis.label.set_fontsize(8)
ax.zaxis.label.set_fontsize(8) 

# impostazioni ticks
ax.yaxis.set_major_locator(plt.MaxNLocator(4))
ax.set_xticklabels(l_campate, fontdict=None, minor=False)
ax.set_yticklabels(l_travi, fontdict=None, minor=False)
ax.tick_params(axis='both', labelsize=8, pad=0.2)