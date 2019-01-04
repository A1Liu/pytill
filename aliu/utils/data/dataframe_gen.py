# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def df_gen():
    #dataframe generator function
    pass

def get_df():
    #returns a dataframe with the specified features
    df = pd.DataFrame([])
    return df

def add_column(df, colname,col_length = -1):
    # Adds a column with the specified features to the specified dataframe
    if col_length == -1:
        col_length = df.shape[0]
    df[colname] = np.zeros(col_length)
    pass
