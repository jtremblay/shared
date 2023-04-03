#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 16:59:32 2023

@author: tremblayju
"""

####################################
# First example with plotnine      #
#                                  #
####################################

from plotnine import *
from plotnine.data import mtcars
mtcars

plot = (ggplot(mtcars, aes('disp', 'mpg'))
 + geom_point())
 
#print(plot)

plot0 =(ggplot(mtcars, aes('disp', 'mpg', color='factor(cyl)'))
 + geom_point()
 + facet_wrap('~cyl')
 + theme_xkcd())
 
#print(plot)

####################################
# get data with pandas             #
#                                  #
####################################

import pandas as pd
data = pd.read_csv('./otu_table_final_rarefied_L6.txt', sep="\t")
#row_sums = data.iloc[2:4].sum()

# colSums
row_sums = pd.DataFrame(data.iloc[:, 1:data.shape[1]].sum(1))
row_sums.set_axis(['rowSum'], axis=1, inplace=True)
print(row_sums)
data2 = pd.concat([data, row_sums.set_axis(data.index)], axis=1)
data2.sort_values(by='rowSum', inplace=True, ascending=[False])
print(data2.head())
#here either select first most abundant row
#data3 = data2.iloc[:5]
#Or select by a specific taxon

data3 = data2[data2['Taxon'].str.contains('o__Enterobacteriales')]
data3 = data3.drop('rowSum', axis=1)
print("data3:")
print(data3.head())
data4 = pd.melt(data3, id_vars =['Taxon'])
print(data4.head())

# Then open mapping file and merge metadata with data4 data frame:
mapping = pd.read_csv('./mapping_file.tsv', sep="\t")
data5 = pd.merge(data4, mapping, left_on='variable', right_on='#SampleID')
print(data5)

# We are now ready for ggplot (i.e. plotnine)
plot = (ggplot(data5, aes('variable', 'value', fill='Taxon'))
 + geom_col()
 + facet_grid('. ~ Visit')
 + theme_xkcd())
print(plot)
