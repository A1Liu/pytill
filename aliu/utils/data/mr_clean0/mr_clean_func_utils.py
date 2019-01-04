# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

def coerce(df,column, coerce):
    df[column] = coerce

def row_req(df,cutoff):
    return rows(df) * cutoff

def rows(df):
    return df.shape[0]

def is_num(series):
    if (series.dtype == np.float64 or series.dtype == np.int64):
        return True
    return False

def get_cutoff(column, cutoff):
    __value_or_container(column,cutoff,1)

def get_colname_gen(df):
    def colname_gen(col_name = 'mrClean'):
        assert type(df) is pd.DataFrame
        id_string = col_name
        if id_string not in df.keys():
            yield id_string
        id_number = 0
        while True:
            id_string = col_name + str(id_number)
            if id_string in df.keys():
                id_number+=1
            else:
                yield id_string
    return colname_gen

def bc_vec(df,value = True): # Boolean column vector
    return np.ones(rows(df),dtype=bool) if value else np.zeros(rows(df),dtype=bool)

def ic_vec(df,value = 0): # Boolean column vector
    if value == 0:
        return np.zeros(rows(df),dtype=np.int32)
    elif value == 1:
        return np.ones(rows(df),dtype=np.int32)
    else:
        return np.ones(rows(df),dtype=np.int32) * value

def __value_or_container(key,item,default):
    if type(item) is dict:
        return item[key] if key in item else default
    return item