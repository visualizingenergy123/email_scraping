#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 13:40:59 2023

@author: hcliffo
"""
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import sys


df = pd.read_csv('Dimensions-Publication-gender_010824.csv',skiprows=1)

count_before = df.groupby('Publisher').count()
df_before = df.copy()
df = df[~df['Authors (Raw Affiliation)'].isna()]
df = df[df['Authors (Raw Affiliation)']!=np.nan]
df = df[df['Authors (Raw Affiliation)'].str.contains('@')==True]

text=[]
emails = []
pubs = []
no_emails = []

for n,row in df.iterrows():
    if '@' in row['Authors (Raw Affiliation)']:
        split1 = row['Authors (Raw Affiliation)'].split(";, ")
        for i1 in split1:
            split2 = i1.split(',')
            for i2 in split2:
                split3 = i2.split(')')
                for i3 in split3:
                    split4 = i3.split(';')
                    for i4 in split4:
                        split5 = i4.split(': ')
                        for i5 in split5:
                            split6 = i5.split(' ')
                            for i6 in split6:
                                if '@' in i6:
                                    if '.' in i6:
                                        if i6.endswith('.'):
                                            i6=i6[:-1]
                                        if i6 not in emails:
                                            emails.append(i6)
                                            pubs.append(row['Publication ID'])

all_emails = pd.DataFrame({'Emails':emails,'Publication ID':pubs})

all_emails = all_emails.merge(df,on='Publication ID',how='left')

test2 = all_emails.drop_duplicates()

count_after = test2.groupby('Publisher').count()

#==================================================================================
#==================================================================================

# springer nature

df2 = df_before[df_before['Publisher']=='Springer Nature']

springer_emails = []
s_id = []
for n,row in df2.iterrows():

    doi = row['DOI']
    link = 'https://doi.org/{}'.format(doi)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    search = str(soup)
    email = search[search.find('mailto'):].split('"')[0][7:]
    springer_emails.append(email)
    s_id.append(row['Publication ID'])

springer = pd.DataFrame({'Emails':springer_emails,'Publication ID':s_id})
springer = springer.merge(df_before,on='Publication ID',how='left')

# frontiers

df3 = df_before[df_before['Publisher']=='Frontiers']

frontier_emails = []
f_id = []
for n,row in df3.iterrows():

    doi = row['DOI']
    link = 'https://doi.org/{}'.format(doi)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    search = str(soup)
    email = search[search.find('mailto'):].split('"')[0][7:]
    frontier_emails.append(email)
    f_id.append(row['Publication ID'])
    
front = pd.DataFrame({'Emails':frontier_emails,'Publication ID':f_id})
front = front.merge(df_before,on='Publication ID',how='left')


combined = pd.concat([all_emails,springer,front])
combined2 = combined.drop_duplicates()
combined2 = combined2[combined2['Emails']!=''] 
combined2.to_excel('Gender_emails_jan24.xlsx')


