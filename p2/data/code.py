#! /usr/bin/python

import pandas as pd
import numpy as np

df = pd.read_csv('data.dat',sep=' ',header=1)
data = df.loc[:,df.columns.to_list()[1:-1]]

levels = data.iloc[range(8),:].copy()
final = data.iloc[range(8,len(df)),:].copy()

def w_sat(e_sat,press,epsilon = 0.622):
    return e_sat*epsilon/(press - e_sat)

def e_sat(T,units = 'K'):
    if units == 'C':
        T = T + 273

    exponent = 5.42 * 1000 * ((1/273) - (1/T))

    return 6.11 * np.exp(exponent)


a1 = levels.loc[range(5),['RP_Press','RP_Temp','RP_DewptTemp','RP_RH']]


a1['e_sat'] = e_sat(a1['RP_Temp'],units='C')
a1['w_sat'] = w_sat(a1['e_sat'],a1['RP_Press'])
a1['w'] = a1['RP_RH']*a1['w_sat']/100

P = a1['RP_Press']
dP = (P - P.shift(-1)).shift()
w_mean = pd.DataFrame(zip(a1.w, a1.w.shift(-1))).mean(1).shift()

water_level = (w_mean * dP).sum() * 100/1000/9.78 * 1000 # milimiters
