import pandas as pd
import numpy as np
import json
import csv
import os
import zipfile
import sys


def date_to_yearweek(date):
    return date.dt.strftime('%Y-%U')


N = 10000000
separator = '\t'
fsource = sys.argv[1] # données brutes
dsource = pd.read_csv(fsource, nrows = N, sep = separator)
ftarget = sys.argv[2] # données anonymisées
dtarget = pd.read_csv(ftarget, nrows = N, sep = separator)

print("Data loaded")
print(dtarget.shape)
print(dsource.shape)

dtarget.columns = ['id', 'date', 'lat', 'long']
dsource.columns = ['id', 'date', 'lat', 'long']
dtarget.drop(dtarget[dtarget['date'] == "DEL"].index, inplace = True)

dsource['date'] = pd.to_datetime(dsource.date, format = '%Y-%m-%d')
dtarget['date'] = pd.to_datetime(dtarget.date, format = '%Y-%m-%d')

#dsource['week_year'] = dsource.date.apply(lambda x: x.weekofyear)
dsource['week_year'] = dsource['date'].dt.strftime('%Y-%U')
dtarget['week_year'] = dtarget['date'].dt.strftime('%Y-%U')


ids_source = pd.unique(dsource["id"])
ids_target = pd.unique(dtarget["id"])

weeks_years = pd.unique(dsource["week_year"])
print(weeks_years)

res = {}
for wy in weeks_years :
    ids = pd.unique(dtarget[dtarget['week_year'] == wy]['id'])
    ids_source = pd.unique(dsource["id"])
    for i in ids :
        print(f"{ids_source[0]} {wy} {i}")
        key = str(ids_source[0])
        if key not in res:
            res[key] = {}
        res[key][wy] = [i]  
        ids_source = ids_source[1:]
        


print(res)
with open("res.json", "w") as outfile: 
    json.dump(res, outfile,sort_keys=True, indent=4)