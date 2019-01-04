# -*- coding: utf-8 -*-

from sas7bdat import SAS7BDAT
import pandas as pd

import numpy as np
import pickle

file_name = ''
nparray = np.loadtxt(file_name, delimiter= ",", skiprows=1, usecols=[0,2])
nparray = np.genfromtxt(file_name, delimiter=',', names=True, dtype=None)
nparray = np.recfromcsv(file_name)

df = pd.read_csv(file_name, sep='\t', comment='#', na_values='Nothing',header = None, nrows = 5)

df = pd.read_stata('disarea.dta')

xlfile = pd.ExcelFile(file_name)
xlfile = pd.read_excel(file_name, sheetname = None)
df = xlfile.parse('sheetname or index',parse_cols=[0], skiprows=1, names=['colname1','colname2'])

file = SAS7BDAT('sales.sas7bdat')
df = file.to_data_frame()
file.close()



file = open(file_name,'rb')
pickle.load(file)
file.close()

