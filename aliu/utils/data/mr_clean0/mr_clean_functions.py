# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from mr_clean_func_utils import coerce,get_colname_gen,get_cutoff,ic_vec,is_num,row_req,rows

def validate(df,coerce_numeric,coerce_dt,coerce_categorical): # validates input
    assert type(df) is pd.DataFrame
    column_dict = {}
    for element in coerce_numeric + coerce_dt + coerce_categorical: # these lists must be mutually exclusive
        assert type(element) is str
        assert not element in column_dict
        column_dict[element] = True

def rename_cols(df, col_names): # renames columns
    if col_names is not None:
        col_list = [*col_names]
        col_gen = get_colname_gen(df)
        for col_name in col_gen():
            if len(col_list) >= len(df.columns):
                break
            else:
                col_list.append(col_name)
    else:
        col_list = [*df.columns]
    for index,col_name in enumerate(col_list):
        col_list[index] = col_name.strip().lower().replace(' ','_')
    df.columns = col_list

def remove_whitespace(df): # removes whitespace from string columns
    for column in (column for column in df if not is_num( df[column] )  ):
        df[column] = df[column].str.strip()
        yield column

def rename_index(df):
    if not (type(df.index) is pd.RangeIndex or type(df.index) is pd.DatetimeIndex):
        df.reset_index() # reset the index
        return True
#%%%
def scrub_str_cols(df,column,char_scrub_cutoff): 
    # Tries to remove common characters from the front and back of the strings in df[column]
    if not is_num(df[column]): # if it's not a numeric
        char_scrub_cutoff = get_cutoff(column, char_scrub_cutoff)
        from_front,from_back = "",""
        flag1, flag2 = True,True
        capture1,capture2 = ic_vec(df),ic_vec(df) # Boolean column vectors
        iteration = 0
        get_colname = get_colname_gen(df)
        while flag1 or flag2:
            valcounts = df.loc[capture1 >= iteration,column].str[0].value_counts()
            flag1 = valcounts[0] >= char_scrub_cutoff * rows(df) if len(valcounts)>0 else False
            if flag1:
                from_front+=valcounts.index[0]
                capture1+=df[column].str.startswith(valcounts.index[0])&(capture1 >= iteration)
                df.loc[capture1 > iteration,column] = df.loc[capture1 > iteration,column].str[1:]
            valcounts = df.loc[capture2 >= iteration,column].str[-1].value_counts()
            flag2 =  valcounts[0] >= char_scrub_cutoff * rows(df) if len(valcounts)>0 else False
            if flag2:
                from_back=valcounts.index[0]+from_back
                capture2+=df[column].str.endswith(valcounts.index[0])&(capture2 >= iteration)
                df.loc[capture2 > iteration,column] = df.loc[capture2 > iteration,column].str[:-1]
            iteration+=1
        if len(from_front + from_back) > 0:
            # Generate unique column names for each appended column
            sieve_col_1 = next(get_colname(column+'_scrubf'))
            sieve_col_2 = next(get_colname(column+'_scrubb'))
            df[sieve_col_1] = capture1 # Add columns
            df[sieve_col_2] = capture2 # Add columns
            return (from_front, from_back, column,sieve_col_1,sieve_col_2)
#%%
def coerce_col(df, column,
               numeric_cutoff, coerce_numeric, 
               dt_cutoff, coerce_dt, dt_format,
               categorical_cutoff,coerce_categorical):
    success = True
    if column in coerce_numeric:
            coerce(df, column, 
                    pd.to_numeric(df[column], errors = 'coerce'))
    elif column in coerce_dt:
        if dt_format is None:
            coerce(df, column, 
                    pd.to_datetime(df[column],errors = 'coerce',infer_datetime_format = True))
        else:
            coerce(df, column, 
                    pd.to_datetime(df[column],errors = 'coerce',format = dt_format))
    elif column in coerce_categorical:
        coerce(df, column, df[column].astype('category'))
    else:
        success = __infer_coerce(df, column,
               get_cutoff( column,numeric_cutoff ),
               get_cutoff( column,dt_cutoff ),
               get_cutoff( column,categorical_cutoff ) )
    return success

def __infer_coerce(df, column,
               numeric_cutoff,dt_cutoff,categorical_cutoff):
    
    cat_coerced = df[column].astype('category')
    num_coerced = pd.to_numeric(df[column], errors = 'coerce')
    dt_coerced = pd.to_datetime(df[column],errors = 'coerce',infer_datetime_format = True)
    
    all_cutoffs = [categorical_cutoff,numeric_cutoff,dt_cutoff]
    all_coerced = [cat_coerced,num_coerced,dt_coerced]
    all_counts = [coerced.count() for coerced in all_coerced]
    all_counts[0] = rows(df)-len(all_coerced[0].value_counts())
    all_scores = [count-row_req(df,cutoff) for count,cutoff in zip(all_counts,all_cutoffs)]
    high_score = max(*all_scores)
    for index in range(3):
        if all_scores[index] == high_score and \
            all_scores[index] >= 0:
            coerce(df, column, all_coerced[index])
            return True
    return False

def preview(df,preview_rows = 5,preview_max_cols = 0):
    """ Returns a preview of a dataframe, which contains both header
    rows and tail rows.
    """
    assert type(df) is pd.DataFrame
    if preview_rows <= 0:
        preview_rows = 1
    initial_max_cols = pd.get_option('display.max_columns')
    pd.set_option('display.max_columns', preview_max_cols)
    data = str(df.iloc[np.r_[0:preview_rows,-preview_rows:0]])
    pd.set_option('display.max_columns', initial_max_cols)
    return data




