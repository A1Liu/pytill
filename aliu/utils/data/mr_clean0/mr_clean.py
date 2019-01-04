# -*- coding: utf-8 -*-
from mr_clean_functions import coerce_col,preview,remove_whitespace, \
            rename_cols,rename_index,scrub_str_cols,validate
from mr_clean_print_utils import convert_memory,memory_statement,output_to_file,title_line

#This method takes in a DataFrame object, as well as a few parameters,
# and outputs a cleaned DataFrame. It operates under a few basic assumptions,
# so it can't do everything lol
def clean(df, settings = None, col_names = None,handle_na = None,
             char_scrub = True, char_scrub_cutoff = .99, scrub_ignore = [],
             numeric_cutoff = .95, coerce_numeric = [],
             dt_cutoff = .99, coerce_dt = [], dt_format = None,
             categorical_cutoff = .60,coerce_categorical = [],
             display_preview = True, preview_rows = 5, preview_max_cols = 0,
             output_file = None,output_safe = True):

    # Error Trap inputs
    validate(df,coerce_numeric,coerce_dt,coerce_categorical)

    def memory_change(task_name = None): # Returns a memory statement and resets memory
        nonlocal df_memory, df
        savings = df_memory - reset_mem()
        if task_name is not None:
            if savings > 0:
                return memory_statement(savings,task_name,'Saved {} after {}\n')
            else:
                return memory_statement(-savings,task_name,"Size grew by {} after {}\n")

    def memory(column = None):# Returns the memory of the dataframe
        nonlocal df
        if column is None:
            return df.memory_usage(deep=True)
        else:
            return df[column].memory_usage(deep=True)

    def reset_mem():# Resets memory value
        nonlocal df_memory
        df_memory = memory().sum()
        return df_memory

    # Make a copy of the inputted DataFrame
    old_df = df
    df = df.copy()
    begin_df_memory = memory().sum()
    df_memory = begin_df_memory

    # ------TASK 1: Remove Columns-----------
    
    
    # ------TASK 1: CHANGE COLNAMES----------
    print('Renaming columns...')
    rename_cols(df,col_names)

    # ------TASK 2: REMOVE WHITESPACE--------
    print('Checking for extra whitespace...')
    col_mem = memory()
    for savings,column in ((col_mem[column]-memory(column),column)
            for column in remove_whitespace(df) if col_mem[column]-memory(column) > 0):
        print( memory_statement(savings,
                                   "removing extra whitespace from column '{}'" \
                                   .format(column)))
    print(memory_change('removing whitespace'))

    # ------TASK 3: REFORMAT INDEX-----------
    if rename_index(df):
        print('Changing unhelpful index and adding it as column')
        print(memory_change('adding a column'))

    # Try to remove characters from beginning and end of columns
    # ------TASK 3: DEEP CLEAN---------------
    if char_scrub:
        print('Trying character scrub...')
        for result in ( scrub_str_cols( df,column, char_scrub_cutoff )
                                                for column in df if column not in scrub_ignore ):
            print( ("Scrubbed '{}' from the front and '{}' from the back of column '{}', \n\t" \
                    "and stored the scrub depths to columns '{}' and '{}' respectively.") \
                 .format(*result)) if result is not None else None
        print(memory_change('character scrubbing'))

    # ------TASK 4: Coerce data types--------
    col_mem = memory()
    print('Trying to coerce column values...')
    for column in df:
        if coerce_col(df,column,
                    numeric_cutoff, coerce_numeric,
                    dt_cutoff, coerce_dt, dt_format,
                    categorical_cutoff,coerce_categorical):
            print( memory_statement( col_mem[column]-memory(column),
                                    "coercing column '{}' to dtype '{}'" \
                                       .format(column,df[column].dtype) ) )
    print(memory_change('coercing columns to specialized data-types'))
    
    # ------TASK 5: Combine columns that are correlated
        # lossless 'compression' and lossy 'compression'
    
    # ------TASK 4: Fill missing values------
    
    #
    
    
    # ------TASK 6:
    # ------TASK 7:
    # ------TASK 8:
    # ------TASK 9:
    # Handle missing values
    # Do melts and pivots (If necessary)
    # I'll do this when I have a better grasp of the intuition that's used to
    # Determine when a pivot or melt is necessary. For now this is just a comment (and a dream)
    

    # Print what was done
    print(title_line('SUMMARY'))
    # Compare column names
    print("Comparison of Column Names: \n\n{}\n{}\n\n".format(old_df.columns,df.columns))
    # Compare column data types

    # Comare previews of data
    if display_preview:
        print('Visual Comparison of DataFrames:\n')
        print(preview(old_df,preview_rows, preview_max_cols))
        print()
        print(preview(df,preview_rows, preview_max_cols))
        print('\n')
    print('Memory Usage:\n')
    print('Initial data size in memory: {}'.format( convert_memory(begin_df_memory) ))
    print('  Final data size in memory: {}'.format( convert_memory(memory().sum()) ))
    print('                     Change: {}'.format( convert_memory(memory().sum()-begin_df_memory) ))
    if output_file is None:
        return df
    else:
        output_to_file(df,output_file, output_safe)



