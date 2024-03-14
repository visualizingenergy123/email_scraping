#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 10:16:26 2024

@author: hcliffo
"""

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import sys



df = pd.read_excel('energy_terms.xlsx')

txt = ''

for i in df['terms']:
    txt = txt + '("' + i +'") OR '

# count_before = df.groupby('Publisher').count()
# df_before = df.copy()
# df = df[~df['Authors (Raw Affiliation)'].isna()]
# # 
# df =df[df['Authors (Raw Affiliation)']!=np.nan]

# df=df[df['Authors (Raw Affiliation)'].str.contains('@')==True]